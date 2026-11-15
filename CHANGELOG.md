# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Hebrew headings are set in Heebo instead of Frank Ruhl Libre. English
  headings are unchanged.

### Fixed
- Narrow screens: prose ran edge to edge with no side margin; every column now
  keeps the page gutter.
- Narrow screens: the section links were hidden outright; they now sit in a
  second header row that scrolls sideways.
- Narrow screens: figure labels shrank to about 6px; each schematic now keeps a
  readable width and scrolls sideways inside its frame.
- The genome-agreement bar chart drew empty tracks (the fill was an inline box
  and ignored its width); bars now render and start at a shared x.
- The two specification tables were clipped inside the prose column on wide
  screens; they now widen up to 980px. Table captions stay inside the visible
  frame while the table scrolls.
- Figure titles and captions now share the prose column's edges, and the hero
  column lines up with the rest of the page.
- Hebrew: tracked monospace labels fell back to a system face with the letters
  pulled apart; they are set in the body face. Machine strings and mixed
  Hebrew/Latin figure labels no longer reorder ("~6.2 µg", "ה-mRNA").
- Hebrew: the accent bar and rounded corners of callouts were on the same side.
- Figure 5: the "ribosome reads" label sat under the moving ribosome.

### Added
- The site itself: a bilingual (Hebrew/English) single-page explainer covering
  the case, the method, the dry-run results and the open limitations, with five
  hand-authored animated SVG figures.
- `scripts/deploy.sh` and `scripts/build_worker.py` — publish the page as a
  Cloudflare Worker at `alpha.idanck.com` and verify the live result.
