# CLAUDE.md — alpha-site

> Created by the `repo-bootstrap` skill on 15/11/2026.
> This repository is **public**. Everything committed here is world-readable,
> including history. Treat every commit accordingly.

## What this is

The public bilingual page about the personalised neoantigen vaccine project for
Alpha, served at https://alpha.idanck.com. One self-contained HTML file.

The analysis pipeline itself lives in a different, private repository
(`idanck/alpha-genomics-gcp`). **Nothing from there is copied here** except
numbers that are already fit for publication.

## Stack

`static-vite`. Vite is present so CI can prove the page still builds; the page
needs no build step of its own. Deployment publishes `index.html` verbatim —
see "Deploying" below for why.

## Commands

| Goal | Command |
|---|---|
| install | `npm install` |
| dev server | `npm run dev` |
| build (what CI runs) | `npm run build` |
| deploy | `scripts/deploy.sh` (needs `CLOUDFLARE_API_TOKEN`, `CF_ACCOUNT_ID`) |

## Binding rules

1. **No direct push to `main`.** Always `feature/<name>` then a PR. This repo is
   public, so GitHub also enforces it server-side: PR required, force-push and
   deletion blocked. The rule here still governs.
2. **Conventional Commits only:** `<type>(<scope>): <subject>` — `feat` `fix`
   `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`.
3. **No secrets, and no home-infrastructure details.** This is a public repo:
   no LAN addresses, no SSH ports, no `/home/<user>` paths, no internal
   hostnames. Reference paths through environment variables instead. The
   `pre-commit` hook and the `secret-scan` workflow both check, and `secret-scan`
   covers infrastructure patterns, not just token shapes.
4. **Read before you write.** The page is one long file with a deliberate
   structure; match the surrounding style.
5. **Verify before you report.** After a change: `npm run build`, and render the
   page before deploying. Never write "done" without checking.
6. **Every number on the page must be traceable.** Figures quoted on the site
   come from the record in `idanck/alpha-genomics-gcp` (`docs/record/`): the
   dry-run report and the case summary. Never estimate a number onto this page,
   and never round one into something that reads better. If the record changes,
   change the page.
7. **The limitations section stays.** The page states plainly what does not work
   and what is unknown. Do not soften it, and do not drop it for length.
8. **The medical disclaimer stays** in both languages.

## Page conventions

- **Bilingual.** Every piece of visible text exists twice, as sibling elements
  marked `lang="he"` and `lang="en"`. `html[data-lang]` hides one side with
  `display:none !important`. The `!important` is load-bearing: without it, any
  later rule that sets `display` on the same element wins on specificity and
  both languages render at once.
- **SVG figures are pinned to `direction:ltr`.** Their coordinate layout is
  left-to-right. On an RTL page, SVG text anchoring flips and every label runs
  off the canvas. Hebrew still shapes correctly inside each label.
- **Never put a CSS animation that uses `transform` directly on an SVG group
  that carries a `transform` attribute.** The CSS transform replaces the
  attribute and the group jumps to the origin. Wrap it: position on the outer
  `<g>`, animation on an inner `<g>`.
- **Do not reuse page-layout class names inside an SVG.** A CSS rule such as
  `.col { width: ... }` also applies to `<rect class="col">` and overrides its
  width attribute.
- **One measure.** `--measure` is registered with `@property` so 68ch resolves
  once against the body font. `.col`, `figcaption` and `.figtitle` all use it;
  do not give a caption its own `ch` width, or its edges drift off the column.
- **Every figure SVG sits in a `.figscroll`.** It keeps the drawing at a
  readable width on narrow screens. A new figure needs the same wrapper.
- **Tables that hold long machine strings take `.tscroll.wide`.**
- **Hebrew and monospace.** Plex Mono has no Hebrew. Tracked mono labels switch
  to the body face under `html[data-lang="he"]`; machine strings use
  `unicode-bidi:plaintext` so punctuation does not jump sides.
- **Complete at rest.** Animations loop on content that is already visible.
  Nothing waits for a scroll or a click to appear.
- Respect `prefers-reduced-motion`.

## Deploying

`scripts/deploy.sh` embeds `index.html` in a Cloudflare Worker named
`alpha-site`, uploads it through the Cloudflare API, attaches the custom domain,
then fetches the live page and compares it byte for byte with `index.html`.

Deployment uses the source file, not `dist/`. Vite's build minifies whitespace,
saving about 2%, but that would make the live bytes differ from this repository
and remove the ability to verify the two are identical. The 2% is not worth it.

## Do not touch

- `alpha.idanck.com` DNS: the record is managed by the Worker's custom-domain
  binding. Editing it by hand will break the route.
