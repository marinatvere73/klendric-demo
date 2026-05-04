# Vesara — Live Product Preview

This repo hosts the public preview of the Vesara STR Listing Intelligence platform.

**Live URL:** https://marinatvere73.github.io/vesara-demo/

Source code lives in a separate private repo. This repo only contains static demo output that is safe to share publicly.

## What's here

- `index.html` — landing page with links to all demos
- `marketing.html` — full marketing one-pager
- `runs/2026-05-03/` — pre-rendered portfolio scorecards (5 properties)
- `runs/demo-airbnb-1334271564949136409/` — Airbnb URL demo

## Update cadence

Every push to `main` rebuilds the site via GitHub Pages. To update the demos, copy fresh output from the private repo's `runs/` directory and push.

## Notes

- `noindex,nofollow` set in `<meta>` so the preview won't be indexed by search engines while in private beta
- All property data is internal LussoStay portfolio data shared by the operator (Marina) for product preview purposes
