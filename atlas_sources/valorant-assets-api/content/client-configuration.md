---
tag: Guides
title: Client configuration
lead: |
  Constructor options and session-level customization points.
breadcrumb: "valorant-assets-api / client configuration"
---

Construct `ValorantAPI` with defaults when you want the standard cached wrapper behavior, or override specific settings when your environment needs tighter control.

:::method
ValorantAPI(*, cache_path: str | None = DEFAULT_CACHE_PATH, default_expiry: int | float = DEFAULT_EXPIRY_SECONDS, request_log_path: str | None = DEFAULT_REQUEST_LOG_PATH, download_directory: str | None = DEFAULT_DOWNLOAD_DIRECTORY, timeout: int | float | None = DEFAULT_TIMEOUT, session: requests.Session | None = None)
:::

:::table
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `cache_path` | `str | None` | temp SQLite path | no | Location for the HTTP response cache |
| `default_expiry` | `int | float` | `86400` | no | Default freshness window in seconds |
| `request_log_path` | `str | None` | `None` | no | Optional request log file path |
| `download_directory` | `str | None` | `None` | no | Root directory for downloaded media assets |
| `timeout` | `int | float | None` | `20` | no | Request timeout in seconds |
| `session` | `requests.Session | None` | `None` | no | Optional custom session |
:::

## Session behavior

If you do not pass a session, the client creates one with:

- `Accept: application/json`
- `User-Agent: valorant-api-wrapper/0.1.0`

Use a custom session when you need shared headers, custom adapters, or request instrumentation beyond the built-in defaults.
