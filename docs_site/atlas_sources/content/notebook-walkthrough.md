---
tag: Guides
title: Notebook walkthrough
lead: |
  When to use the repository notebook instead of the static docs.
breadcrumb: "valorant-assets-api / notebook walkthrough"
---

The repository includes a guided notebook at [`notebooks/valorant_assets_api_tutorial.ipynb`](https://github.com/BrandonBahret/Py-Valorant-Assets-API/blob/main/notebooks/valorant_assets_api_tutorial.ipynb).

Use the notebook for an interactive walkthrough of:

- package installation and setup
- client construction
- localization
- UUID lookups
- helper methods
- cache configuration
- typed model inspection

:::callout info
The embedded export below is a read-only preview of the executed notebook. Open the full export in a separate tab when you want native width, your browser's page search, or the original notebook source.
:::

<style>
  .notebook-preview {
    margin: 28px 0 34px;
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
    background:
      linear-gradient(180deg, color-mix(in srgb, var(--surface) 94%, transparent), color-mix(in srgb, var(--bg) 88%, transparent)),
      radial-gradient(circle at top left, color-mix(in srgb, var(--accent2) 12%, transparent), transparent 42%);
    box-shadow: 0 18px 46px color-mix(in srgb, var(--bg) 46%, transparent);
  }
  .notebook-preview__bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    padding: 16px 18px;
    border-bottom: 1px solid var(--border-subtle);
    background: linear-gradient(180deg, color-mix(in srgb, var(--surface) 92%, transparent), transparent);
  }
  .notebook-preview__title {
    font-family: var(--font-display);
    font-size: 22px;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: var(--text);
    margin: 0;
  }
  .notebook-preview__meta {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent2);
  }
  .notebook-preview__actions {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  .notebook-preview__action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 36px;
    padding: 0 13px;
    border-radius: 999px;
    border: 1px solid color-mix(in srgb, var(--accent2) 20%, var(--border));
    background: color-mix(in srgb, var(--surface) 88%, transparent);
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 12px;
    text-decoration: none;
    white-space: nowrap;
  }
  .notebook-preview__action:hover {
    text-decoration: none;
    border-color: color-mix(in srgb, var(--accent) 28%, var(--border));
    background: color-mix(in srgb, var(--accent) 8%, var(--surface));
  }
  .notebook-preview__frame-wrap {
    padding: 18px;
  }
  .notebook-preview__frame {
    display: block;
    width: 100%;
    min-height: 900px;
    border: 1px solid color-mix(in srgb, var(--accent2) 12%, var(--border));
    border-radius: 14px;
    background: #ffffff;
  }
  .notebook-preview__caption {
    padding: 0 18px 18px;
    font-size: 13px;
    color: var(--text-dimmer);
  }
  @media (max-width: 820px) {
    .notebook-preview__bar {
      flex-direction: column;
      align-items: flex-start;
    }
    .notebook-preview__frame {
      min-height: 720px;
    }
  }
</style>

<section class="notebook-preview" aria-labelledby="notebook-preview-title">
  <div class="notebook-preview__bar">
    <div>
      <div class="notebook-preview__meta">Notebook export</div>
      <p class="notebook-preview__title" id="notebook-preview-title">Executed HTML walkthrough</p>
    </div>
    <div class="notebook-preview__actions">
      <a class="notebook-preview__action" href="./notebooks/valorant_assets_api_tutorial.html" target="_blank">Open HTML export</a>
      <a class="notebook-preview__action" href="https://github.com/BrandonBahret/Py-Valorant-Assets-API/blob/main/notebooks/valorant_assets_api_tutorial.ipynb" target="_blank">Open notebook source</a>
    </div>
  </div>
  <div class="notebook-preview__frame-wrap">
    <iframe
      class="notebook-preview__frame"
      src="./notebooks/valorant_assets_api_tutorial.html"
      title="Valorant assets API tutorial notebook export"
      loading="lazy"
      referrerpolicy="no-referrer"
    ></iframe>
  </div>
  <p class="notebook-preview__caption">This is a non-interactive export</p>
</section>
