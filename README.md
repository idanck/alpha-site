# alpha-site

The public, bilingual (Hebrew/English) page explaining the personalised
neoantigen vaccine project for Alpha — a dog with a liver carcinoma.

**Live:** https://alpha.idanck.com

## What this repository is

One self-contained HTML page. All CSS, all JavaScript and all five animated SVG
figures are inline; the only external request the page makes is to Google Fonts.
There is no framework and no client-side routing.

```
index.html              the site — the source of truth
scripts/deploy.sh       publish to the Cloudflare Worker, then verify
scripts/build_worker.py builds and uploads the Worker
```

## Requirements

- Node 22+ (only to run the CI build locally)
- Python 3.9+ (deployment)
- A Cloudflare API token with Workers Scripts:Edit, plus Zone:Read and
  Workers Routes:Edit to attach the custom domain

## Running it

```bash
npm install
npm run dev      # local dev server
npm run build    # what CI runs; output in dist/
```

`npm run build` exists so CI proves the page still parses and builds. **It is
not what gets deployed.** Vite minifies whitespace, which saves about 2% and
makes the deployed bytes differ from the file in this repo. Deployment publishes
`index.html` as it is, so the live page can be compared byte for byte against
this repository — which `scripts/deploy.sh` does on every run.

## Deploying

```bash
set -a; source "$CREDENTIALS_FILE"; set +a   # CLOUDFLARE_API_TOKEN, CF_ACCOUNT_ID
scripts/deploy.sh
```

The script embeds `index.html` in a Cloudflare Worker named `alpha-site`,
uploads it, attaches `alpha.idanck.com` as a custom domain, then fetches the
live page and compares it with `index.html`.

## Environment

See `.env.example` — names only. Values never enter this repository.

## After a fresh clone

```bash
git config core.hooksPath .githooks
```

Without it the pre-commit and pre-push hooks are inactive in that clone.
