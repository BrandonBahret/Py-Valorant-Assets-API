---
tag: Concepts
title: Caching and freshness
lead: |
  How the wrapper stores and reuses HTTP responses by default.
breadcrumb: "valorant-assets-api / caching and freshness"
---

Caching is part of the package's normal usage model, not an optional afterthought. Most endpoints expose content metadata that changes slowly, so the default client stores responses locally and reuses them across calls.

## Defaults

:::table
| Setting | Default | Meaning |
|---------|---------|---------|
| `cache_path` | temp SQLite path | Stores cached responses on disk |
| `default_expiry` | `60 * 60 * 24` | Freshness window for most endpoints |
| `timeout` | `20` | Request timeout in seconds |
| `request_log_path` | `None` | Logging disabled by default |
:::

## Resource-specific freshness

Some endpoints override the default expiry in the client implementation:

- Competitive tiers use a 12 hour expiry.
- Missions and objectives use a 30 minute expiry.
- Version metadata uses a 1 hour expiry.

## Practical guidance

- Keep the default cache for scripts and exploratory work.
- Set `cache_path` explicitly when you want a reproducible project-local cache file.
- Lower expiry values when you are validating freshness-sensitive behavior.
- Enable request logging when you need to confirm which calls miss cache.

:::callout warn
Cached media files are separate from the HTTP response cache. Resource metadata lives in the API cache, while downloaded images and audio files live under `download_directory`.
:::
