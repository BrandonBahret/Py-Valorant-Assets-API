---
tag: Overview
title: Introduction
lead: |
  A typed, cached Python wrapper for Valorant content data.
breadcrumb: "valorant-assets-api / introduction"
---

`valorant-assets-api` wraps the public Valorant content API in one Python client that returns typed objects instead of raw dictionaries. The package is built for applications, scripts, and notebooks that need stable game metadata without repeating HTTP plumbing, response mapping, and local caching.

The wrapper tracks the same major data classes that the upstream Valorant API exposes, but the experience is SDK-shaped rather than endpoint-shaped. Each resource page in this site shows the client methods you call, the models you receive, and the wrapper behaviors layered on top of the raw API.

:::cards
### Quickstart {link=quickstart}
Construct a client, make a few real calls, and inspect typed fields.

### Resource reference {link=agents}
Jump straight to the resource-oriented reference section.
:::

## What the wrapper gives you

- One `ValorantAPI` client for the main public `/v1` content endpoints.
- Typed `@apimodel` resources and nested helper models.
- Built-in caching through `pypercache`.
- Wrapper helpers for common lookup flows like display-name search, active events, current season lookup, and flattened contract rewards.
- Media URL fields wrapped as `CachedMediaAsset` for optional disk downloads.

## What these docs optimize for

These docs follow the upstream resource-per-page scanning model, but each page is adapted to the Python API surface. You can open a resource page like [doc:weapons] to see the relevant client methods and the schema you get back in the same place.
