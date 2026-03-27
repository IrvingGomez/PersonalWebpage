# Project Section Improvement Plan

## Context

This plan focuses on `https://irvinggomez.com/project/` and the four legacy project pages under `content/project/`:

- `Happiness`
- `Poverty`
- `RandomForestWithMissing`
- `VAEs`

The goal is to improve this section without treating it like a flagship portfolio area. These pages are older work, but they should still be coherent, lighter, and easier to maintain.

## What We Observed

- The `/project/` landing page itself is simple and lightweight.
- The main issues are in the individual project pages.
- `Happiness` and `Poverty` have very large `index.md` files with a lot of inline HTML and legacy scripting.
- The rendered pages for `Happiness` and `Poverty` are very large:
  - `public/project/happiness/index.html`: about 211 KB
  - `public/project/poverty/index.html`: about 133 KB
- `VAEs` contains very large GIF assets:
  - `original_denoise_vae_latent.gif`: about 3.7 MB
  - `greedy_ae_latent.gif`: about 2.7 MB
  - `original_denoise_vae_recons.gif`: about 2.6 MB
- `RandomForestWithMissing` is much simpler and probably needs mostly editorial cleanup.
- The legacy pages mix Markdown, raw HTML, inline scripts, manual table-of-contents markup, and old formatting conventions.

## Guiding Principles

- Keep the historical value of the projects.
- Reduce unnecessary resource usage.
- Prefer plain content, images, and short explanations over heavy inline interactivity.
- Make the project section feel curated rather than abandoned.
- Avoid rewriting the entire site architecture unless clearly necessary.

## Scope

### In Scope

- The `/project/` section landing page.
- The four legacy project pages in `content/project/`.
- Their local assets.
- Project-specific presentation, copy, and performance improvements.

### Out of Scope

- Redesigning the entire website.
- Reworking unrelated sections such as talks, publications, teaching, or research.
- Rebuilding these projects as live applications.
- Reconstructing missing source code or recovering exact historical interactivity unless it is easy and justified.

## Proposed Work Plan

### Phase 1: Audit and Triage

Checklist:

- [ ] Inventory each project page's purpose, current usefulness, and target level of detail.
- [ ] Classify each project as:
  - keep as a compact archival page
  - keep with moderate cleanup
  - heavily simplify
- [ ] Identify all embedded scripts, inline HTML blocks, large media files, and unusual markup patterns.
- [ ] Confirm whether any page depends on functionality that should be preserved exactly.

Success criteria:

- Every project has a clear treatment decision.
- We know which assets and behaviors are worth keeping versus removing.
- We have a ranked list of the worst performance and maintenance problems.

### Phase 2: Simplify the `/project/` Landing Page

Checklist:

- [ ] Decide whether the section should be framed explicitly as "Selected Earlier Projects", "Archived Projects", or similar.
- [ ] Improve the section intro so visitors understand these are older exploratory works.
- [ ] Standardize the summaries so each project is described in one clear sentence.
- [ ] Review ordering so the strongest or most representative older projects appear first.
- [ ] Check whether project cards/list items should include a clearer distinction between archival work and current work.

Success criteria:

- The landing page sets the right expectations immediately.
- Each project summary is concise, clear, and professionally framed.
- The section feels curated rather than like a dump of old pages.

### Phase 3: Reduce Resource Usage on Heavy Project Pages

Checklist:

- [ ] Replace oversized GIFs in `VAEs` where possible with lighter formats or fewer animations.
- [ ] Review `Happiness` and `Poverty` for interactive blocks that can be converted into static images or simpler content.
- [ ] Remove duplicated or unnecessary inline scripts.
- [ ] Reduce repeated embedded visualization payloads where they do not add much value.
- [ ] Ensure pages load only the assets they truly need.

Success criteria:

- The heaviest project pages are materially smaller and faster to load.
- No legacy page carries large interactive payloads unless they clearly justify themselves.
- Asset usage is proportional to the historical importance of the content.

### Phase 4: Clean Up Content Structure

Checklist:

- [ ] Replace manual HTML structures with Markdown where feasible.
- [ ] Remove hand-written table-of-contents markup if Hugo handles the page well enough without it.
- [ ] Normalize headings and section order across projects.
- [ ] Fix obvious typos, unclear phrasing, and awkward early-career wording while preserving substance.
- [ ] Remove broken-looking markup and old presentation hacks.

Success criteria:

- Project pages are easier to read in source and in the browser.
- The content structure is consistent across projects.
- The pages feel more polished without pretending to be something new.

### Phase 5: Clarify the Role of Each Project

Checklist:

- [ ] Add short framing near the top of each project page explaining what the project is and why it still appears on the site.
- [ ] Clearly link to external repositories when the repo is the real artifact.
- [ ] For projects with outdated methods or rough implementation, present them as exploratory or early research/software work.
- [ ] Decide whether each page should end with a compact "What this project explored" or "What remains interesting here" section.

Success criteria:

- Visitors understand why each project is included.
- Older work reads as credible historical work, not accidental clutter.
- The section supports your current professional identity instead of weakening it.

### Phase 6: Final Quality Pass

Checklist:

- [ ] Rebuild the site and inspect `/project/` plus all four project pages.
- [ ] Check for broken images, broken links, and layout regressions.
- [ ] Compare page weights before and after for the heaviest pages.
- [ ] Run a focused PageSpeed pass on the worst project pages after cleanup.
- [ ] Verify that the result still feels like your site, not a generic modernization pass.

Success criteria:

- All pages render correctly.
- The cleaned pages are clearly lighter and easier to maintain.
- The project section feels intentional, archival, and professionally presented.

## Priority Order

1. `Happiness`
2. `Poverty`
3. `VAEs`
4. `RandomForestWithMissing`
5. `/project/` section framing and ordering

Reasoning:

- `Happiness` and `Poverty` appear to be the most bloated and structurally messy.
- `VAEs` has important large media issues.
- `RandomForestWithMissing` is comparatively small and likely easy to improve.
- The section landing page should be adjusted after we know how each project will be presented.

## Deliverables for the Implementation Phase

- A cleaned and reframed `/project/` landing page.
- Simplified individual project pages with lighter assets and clearer copy.
- Reduced page weight for the heaviest project pages.
- A more maintainable content structure in `content/project/`.

## Definition of Done

This effort is complete when:

- `/project/` clearly presents these pages as older curated work.
- The four project pages are easier to read, easier to maintain, and meaningfully lighter.
- Heavy legacy interactivity is removed or reduced where it is no longer worth the cost.
- The pages still preserve the core intellectual story of the projects.
- The section supports your current website instead of feeling like an unmaintained archive.
