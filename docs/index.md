# Valorant API Wrapper Docs

These docs are for Python developers who want a typed, cached client for the public [Valorant API](https://dash.valorant-api.com/). Start here if you want the reader path; use the reference pages when you already know what you want to look up.

## Start Here

- New to the wrapper: read [Getting Started](getting-started.md).
- Looking for common workflows and tradeoffs: read [Usage Patterns](usage-patterns.md).
- Want the notebook walkthrough: open [Tutorials](tutorials.md).
- Need signatures, fields, or enum values: use the [Reference](reference/index.md).

## What This Wrapper Gives You

- A single `ValorantAPI` client for the main public `/v1` endpoints.
- Typed Python models instead of raw response dictionaries.
- Built-in caching through `pypercache`, which is useful for mostly-static game metadata.
- Convenience helpers for common lookup patterns such as playable agents, name-based search, active events, and current season data.

## Documentation Contract

Narrative pages explain when to use the wrapper, how to move through the API, and what tradeoffs matter in normal use. Reference pages are generated from source and are for fast lookup, not onboarding. If a generated summary is too thin for an important API, improve the code docstring or the narrative guide instead of editing generated reference by hand.
