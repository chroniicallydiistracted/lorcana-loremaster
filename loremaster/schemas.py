"""Strict boundaries for curated data; unknown upstream fields stay in raw sources."""

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Citation(StrictModel):
    source_id: str
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    page: int | None = Field(default=None, ge=1)
    section: str | None = None
    url: str
    path: str


class CardMechanics(StrictModel):
    name: str
    subtitle: str
    card_type: Literal["character", "action", "item", "location"]
    ink_cost: int = Field(ge=0, strict=True)
    inkable: bool = Field(strict=True)
    ink_colors: list[Literal["AMBER", "AMETHYST", "EMERALD", "RUBY", "SAPPHIRE", "STEEL"]]
    strength: int | None
    willpower: int | None
    lore: int | None
    move_cost: int | None
    classifications: list[str]
    rules_text: str
    copy_limit: int | None = Field(ge=1)
    extra_character_classification: str | None


class Review(StrictModel):
    identity_id: str
    full_name: str
    catalog_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    reviewed_at: date
    effective_from: date
    effective_until: date | None = None
    official_effective_date: date | None = None
    status: Literal["resolved", "unresolved"]
    categories: list[Literal["cosmetic", "reminder", "naming", "classification", "functional", "data_error"]]
    selected_printing_id: int
    fields: list[str]
    resolved_values: dict[str, Any]
    rationale: str
    evidence: list[Citation] = Field(min_length=1)

    @model_validator(mode="after")
    def coherent(self):
        if not set(self.fields) <= set(CardMechanics.model_fields):
            raise ValueError("Review includes an unknown mechanics field")
        if self.status == "resolved" and set(self.fields) != set(self.resolved_values):
            raise ValueError("Every resolved conflict field requires an explicit value")
        if self.status == "unresolved" and self.resolved_values:
            raise ValueError("Unresolved records cannot supply an oracle override")
        if self.effective_until and self.effective_until <= self.effective_from:
            raise ValueError("Empty review effective-date interval")
        return self


class ReviewLedger(StrictModel):
    schema_version: Literal[2]
    coverage: str
    records: list[Review]

    @model_validator(mode="after")
    def unique(self):
        intervals = {}
        for record in self.records:
            for other in intervals.get(record.identity_id, []):
                if (record.effective_until or date.max) > other.effective_from and (
                    other.effective_until or date.max
                ) > record.effective_from:
                    raise ValueError("Overlapping review intervals for " + record.identity_id)
            intervals.setdefault(record.identity_id, []).append(record)
        return self


class Fact(StrictModel):
    fact_id: str
    domain: str
    questions: list[str] = Field(min_length=1)
    answer: str
    classification: Literal["official_fact", "calculation", "project_method", "insufficient_evidence"]
    effective_from: date
    checked_at: date
    region: str = "rules apply globally; source language English"
    citations: list[Citation] = Field(min_length=1)


class Source(BaseModel):
    model_config = ConfigDict(extra="allow")
    source_id: str
    url: str
    authority: str
    language: str
    path: str | None = None
    sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    checked_at: date | None = None
    effective_date: date | None = None


class SourceRegistry(BaseModel):
    model_config = ConfigDict(extra="allow")
    sources: list[Source]

    @model_validator(mode="after")
    def unique(self):
        if len({s.source_id for s in self.sources}) != len(self.sources):
            raise ValueError("Duplicate source ID")
        return self
