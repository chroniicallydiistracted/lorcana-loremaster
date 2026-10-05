"""Read-only supplemental provider snapshots, isolated from official card/rules data."""

import hashlib
import json
import unicodedata
import urllib.request
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo


def catalog(root):
    records = json.loads((root / "sources/providers.json").read_text())["providers"]
    ids = [p["provider_id"] for p in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate provider ID")
    for provider in records:
        endpoints = provider["endpoints"]
        if len({e["endpoint_id"] for e in endpoints}) != len(endpoints):
            raise ValueError("Duplicate endpoint ID")
        for endpoint in endpoints:
            if not endpoint["url"].startswith("https://") or endpoint["cache_hours"] < 24:
                raise ValueError("Provider endpoint must use HTTPS and a 24-hour minimum cache")
    return records


def validate_payload(payload, shape):
    if shape == "results_object":
        if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
            raise ValueError("Provider response must contain a results array")
        if payload.get("success") is False or payload.get("errors"):
            raise ValueError("Provider reported an upstream error")
        rows = payload["results"]
    elif shape == "array":
        if not isinstance(payload, list):
            raise ValueError("Provider response must be an array")
        rows = payload
    else:
        raise ValueError("Unknown endpoint shape")
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("Provider result rows must be objects")
    return rows


def fetch_bytes(url):
    request = urllib.request.Request(url, headers={"User-Agent": "LorcanaLoremaster/1.0 provider research"})
    with urllib.request.urlopen(request, timeout=20) as response:
        content = response.read(20_000_001)
        if len(content) > 20_000_000:
            raise ValueError("Provider response exceeded the 20 MB limit")
        return content, response.url


def snapshot(root, provider_id, endpoint_id, fetch=fetch_bytes, now=None):
    now = now or datetime.now(UTC)
    provider = next((p for p in catalog(root) if p["provider_id"] == provider_id), None)
    if not provider:
        raise ValueError("Unknown provider ID")
    endpoint = next((e for e in provider["endpoints"] if e["endpoint_id"] == endpoint_id), None)
    if not endpoint:
        raise ValueError("Endpoint not approved for public read-only snapshots")
    index_path = root / "sources/provider-snapshots.json"
    index = (
        json.loads(index_path.read_text()) if index_path.exists() else {"schema_version": 1, "records": []}
    )
    record = next(
        (r for r in index["records"] if (r["provider_id"], r["endpoint_id"]) == (provider_id, endpoint_id)),
        None,
    )
    missing_raw = False
    if record:
        path = root / record["path"]
        missing_raw = not path.is_file()
        if not missing_raw:
            if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
                raise ValueError("Provider snapshot bytes changed")
            expires = datetime.fromisoformat(record["retrieved_at"]) + timedelta(
                hours=endpoint["cache_hours"]
            )
            if now < expires:
                return record | {"status": "cached", "expires_at": expires.isoformat()}
    content, resolved_url = fetch(endpoint["url"])
    payload = json.loads(content)
    rows = validate_payload(payload, endpoint["shape"])
    sha = hashlib.sha256(content).hexdigest()
    directory = root / "sources/providers" / provider_id
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (sha + ".json")
    path.write_bytes(content)
    result = {
        "provider_id": provider_id,
        "endpoint_id": endpoint_id,
        "url": endpoint["url"],
        "resolved_url": resolved_url,
        "retrieved_at": now.isoformat(),
        "authority": "supplemental_provider_data",
        "sha256": sha,
        "path": str(path.relative_to(root)),
        "rows": len(rows),
        "upstream_update_time": payload.get("modifiedOn") if isinstance(payload, dict) else None,
        "status": "downloaded",
    }
    if missing_raw:
        result["cache_miss_reason"] = "Raw snapshot absent from this checkout; downloaded a new observation."
    if record:
        result["previous_snapshots"] = record.get("previous_snapshots", []) + [
            {k: record[k] for k in ["path", "sha256", "retrieved_at", "rows"]}
        ]
        index["records"].remove(record)
    index["records"].append(result)
    # Failed transport, JSON or shape validation leaves the previous registry untouched.
    stage = index_path.with_suffix(".tmp")
    stage.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    stage.replace(index_path)
    return result


def inspect_snapshot(root, provider_id, endpoint_id):
    index = json.loads((root / "sources/provider-snapshots.json").read_text())
    record = next(
        r for r in index["records"] if (r["provider_id"], r["endpoint_id"]) == (provider_id, endpoint_id)
    )
    path = root / record["path"]
    if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
        raise ValueError("Provider snapshot bytes changed")
    return record, json.loads(path.read_bytes())


def coverage(root):
    card_record, cards = inspect_snapshot(root, "lorcast", "hyperia-cards")
    product_record, products = inspect_snapshot(root, "tcgcsv", "hyperia-products")
    price_record, prices = inspect_snapshot(root, "tcgcsv", "hyperia-prices")
    products = validate_payload(products, "results_object")
    prices = validate_payload(prices, "results_object")
    printings = [json.loads(line) for line in (root / "data/derived/printings.jsonl").open()]
    local = {str(p["collector_number"]): p for p in printings if p["printed_set_number"] == 14}
    numbers = {str(c["collector_number"]) for c in cards}

    def normalized(value):
        return " ".join(unicodedata.normalize("NFKC", value).replace("’", "'").casefold().split())

    differences, representations = [], []
    matched = 0
    mapping = {
        "name": "name",
        "version": "subtitle",
        "cost": "ink_cost",
        "inkwell": "inkable",
        "strength": "strength",
        "willpower": "willpower",
        "lore": "lore",
        "move_cost": "move_cost",
    }
    for card in cards:
        number = str(card["collector_number"])
        if card.get("lang") != "en" or card.get("set", {}).get("code") != "14":
            raise ValueError("Unexpected language or set in Hyperia endpoint")
        if number not in local:
            continue
        matched += 1
        for upstream, field in mapping.items():
            actual, expected = card.get(upstream), local[number][field]
            compare_actual = normalized(actual) if isinstance(actual, str) else actual
            compare_expected = normalized(expected) if isinstance(expected, str) else expected
            if compare_actual != compare_expected:
                target = (
                    representations
                    if field == "subtitle" and actual is None and expected == ""
                    else differences
                )
                target.append(
                    {
                        "collector_number": number,
                        "field": field,
                        "provider_value": actual,
                        "local_value": expected,
                    }
                )
        if sorted(i.upper() for i in card.get("inks", [])) != sorted(local[number]["ink_colors"]):
            differences.append(
                {
                    "collector_number": number,
                    "field": "ink_colors",
                    "provider_value": card.get("inks"),
                    "local_value": local[number]["ink_colors"],
                }
            )
    product_ids = {p["productId"] for p in products}
    price_ids = {p["productId"] for p in prices}
    singles = [p for p in products if any(x.get("name") == "Number" for x in p.get("extendedData", []))]
    latest = max(
        datetime.fromisoformat(r["retrieved_at"]) for r in [card_record, product_record, price_record]
    )
    return {
        "snapshot_date": latest.astimezone(ZoneInfo("America/Phoenix")).date().isoformat(),
        "report_timezone": "America/Phoenix",
        "scope": "Observed payloads; not a text adjudication, purchase quote or provider-wide completeness claim.",
        "citations": [card_record, product_record, price_record],
        "lorcast": {
            "printing_rows": len(cards),
            "local_printed_set_14_rows": len(local),
            "base_numbers_present": len(numbers & {str(n) for n in range(1, 205)}),
            "base_numbers_missing": [n for n in range(1, 205) if str(n) not in numbers],
            "matched_printings": matched,
            "unmatched_numbers": sorted(numbers - set(local)),
            "local_numbers_absent_from_provider": sorted(set(local) - numbers),
            "name_stat_ink_differences": differences,
            "null_empty_subtitle_representation_differences": representations,
            "rows_with_price_values": sum(
                any(v is not None for v in c.get("prices", {}).values()) for c in cards
            ),
            "text_review": "Not compared semantically; differing symbol/reminder/story-name encoding needs review.",
        },
        "tcgcsv": {
            "category_id": 71,
            "group_id": 24740,
            "product_rows": len(products),
            "price_rows": len(prices),
            "single_card_number_metadata_rows": len(singles),
            "products": [
                {
                    "product_id": p["productId"],
                    "name": p["name"],
                    "presale": p.get("presaleInfo", {}).get("isPresale"),
                }
                for p in products
            ],
            "orphan_price_product_ids": sorted({p["productId"] for p in prices} - product_ids),
            "products_without_price_rows": sorted(product_ids - price_ids),
            "individual_card_prices_available": any(p["productId"] in price_ids for p in singles),
            "upstream_price_update_time": price_record["upstream_update_time"],
            "condition_language_sku_data": False,
        },
    }
