# Upstream tooling

`lorcanajson/` is the original supplied LorcanaJSON source directory, moved intact.
Its README, requirements, corrections and LICENSE remain with it. No upstream
version/commit was supplied, so this is a vendored snapshot of unknown commit.

It contains OCR and external enrichment code; it is not the official rules or the
active current card catalog. Its API handler also contains an app authorization
string from upstream. The local workspace tools do not use or expose that string.
Follow upstream setup only when OCR/enrichment is actually needed; ordinary lookup
and catalog rebuilding require no third-party Python packages.
