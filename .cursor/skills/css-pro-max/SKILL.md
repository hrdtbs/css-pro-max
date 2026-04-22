---
name: css-pro-max
description: Comprehensive CSS and UI design guidance for responsive layout strategy, spacing rhythm, design-system terminology, animations/keyframes, typography (Japanese/English), visual polish, and accessibility baselines. Use this skill whenever the user asks about CSS architecture, layout behavior, component naming, motion decisions, readability tuning, interaction polish, or accessibility quality checks in web UI work, even if the request is abstract and not asking for CSS code directly.
---

# CSS Pro Max

This skill consolidates production-grade guidance for CSS and UI work on the modern web. It covers layout and responsive strategy, spacing and whitespace rhythm, design-system terminology, motion, typography, visual-detail polish, accessibility baselines, foundation CSS architecture, token systems, color systems, and z-axis layering rules. The guidance is opinionated: when there is a preferred default, it is stated.

Each concept has exactly one canonical reference. Other references link to it rather than restating it — open the canonical file when you need to change or cite a rule.

## When to use

Apply this skill for any task that touches CSS, markup that implies CSS responsibilities, or the look-and-feel quality of a product:

- Writing CSS for a component, page, or design system.
- Choosing padding, gaps, section rhythm, gutters, or spacing scale steps.
- Choosing a layout strategy: intrinsic sizing, flex, grid, container queries, media queries, or viewport units.
- Naming components, tokens, or layers inside a design system.
- Designing animations, transitions, scroll-linked motion, or `@keyframes`.
- Configuring typography (font stack, kerning, line-height, text-wrap, fluid type, Japanese-specific features).
- Polishing interactive UI: border radius, shadows, icon animation, staggered enters, tabular numerals.
- Auditing a UI for accessibility.
- Deciding `px` vs `rem`, physical vs logical properties, shorthand vs longhand, viewport vs container units.

## When not to use

Skip this skill for pure backend logic, database schema work, API design decoupled from UI, non-visual scripts, or infrastructure and DevOps work.

Decision rule: if the change affects how a feature looks, feels, moves, or is interacted with, open this skill.

## Core principles

1. **CSS is a suggestion, not a command.** Let the engine handle what it does well (intrinsic sizing, wrapping, auto-fit grids) before reaching for queries or fixed values.
2. **Keep an intrinsic baseline.** Responsive work starts with contracting/expanding behavior and flexibility; queries are escalation tools, not the default.
3. **Use the escalation order.** Static → intrinsic → container query → media query. Do not jump to media queries before exhausting intrinsic layout.
4. **Prefer logical properties where the layout primitive is logical.** Flex and grid already think in inline/block axes; match them. Stay physical where the spec is physical (transforms, backgrounds, media queries).
5. **Name by responsibility, never by appearance.** A `<button>` is a `Button`, an `<a>` is a `Link`, even if it looks like a button. Structure, behaviour, and HTML element dictate the name.
6. **Motion must earn its place.** Classify each animation as functional or decorative. When in doubt, remove it. The fastest animation is no animation.
7. **Write defensively.** Assume text doubles in length, images fail to load, content is edited by a CMS, and users scale fonts. Build for the 80% that breaks in production.
8. **Accessibility is not optional.** Contrast, focus visibility, touch-target size, keyboard order, `prefers-reduced-motion`, and screen-reader labels are hard requirements, not nice-to-haves.
9. **Progressive enhancement over hard gates.** Ship modern features (View Transitions, `text-wrap: pretty`, `text-box-trim`, `word-break: auto-phrase`, `field-sizing`) when they degrade gracefully; avoid features that silently break layout where unsupported.
10. **Details compound into quality.** Concentric radii, optical alignment, layered shadows, tabular numerals, staggered enters, and a `40×40` minimum hit area add up to what "feels polished".

## Decision flow — which reference should I open?

| Task | Open |
| --- | --- |
| Picking between intrinsic, container query, media query, or viewport units | [responsive](references/responsive.md) |
| Computing a fluid `clamp()` or a breakpoint from `calc()` | [responsive](references/responsive.md) |
| Naming a component, wrapper, navigation, menu, template, pattern, or theme | [terminology](references/terminology.md) |
| Deciding whether an animation is needed at all, or choosing easing/duration | [animations](references/animations.md) |
| Implementing `prefers-reduced-motion` branches in CSS | [animations](references/animations.md) |
| Writing `@keyframes` (naming, scope, API-style custom properties, global vs local) | [keyframes](references/keyframes.md) |
| Setting up a font stack, text-wrap, kerning, measure, or fluid type (especially Japanese) | [typography](references/typography.md) |
| Applying polish details: radii, shadows, staggered enters, icon cross-fade, tabular numerals | [visual-details](references/visual-details.md) |
| Verifying contrast, focus visibility, hit area, `prefers-reduced-motion` policy, ARIA, or keyboard operability | [accessibility](references/accessibility.md) |
| Defining global stack order for overlays, dialogs, and fixed surfaces | [z-index](references/z-index.md) |
| Designing reset policy, cascade layers, and low-specificity base | [foundation](references/foundation.md) |
| Designing token naming, scales, and API-style custom-property contracts | [tokens](references/tokens.md) |
| Building palette scales, text hierarchy color rules, and dark-mode color ladders | [color](references/color.md) |
| Spacing scale, `gap` vs `margin`, grid vs flex for rhythm, gutters, responsive steps, negative margins | [spacing](references/spacing.md) |

## Loading directives (MANDATORY / Do NOT Load)

Use this section to avoid both under-loading and over-loading references.

### Responsive symptoms

- **MANDATORY - READ** [responsive.md](references/responsive.md) when layout breaks by container width, query thresholds are unclear, or `clamp()` math needs recalculation.
- **Do NOT Load** [animations.md](references/animations.md) first for layout collapse issues; motion tuning does not fix structural width/flow bugs.

### Typography symptoms

- **MANDATORY - READ** [typography.md](references/typography.md) when text is hard to read, line breaks are awkward, or Japanese/English mixed text looks uneven.
- **Do NOT Load** [visual-details.md](references/visual-details.md) first for readability issues; shadows/radii cannot recover poor text rhythm.

### Motion symptoms

- **MANDATORY - READ** [animations.md](references/animations.md) when interaction feedback feels slow, distracting, or accessibility complaints mention motion sickness.
- **Do NOT Load** [keyframes.md](references/keyframes.md) first unless `@keyframes` design itself is the problem; many issues are solved by timing/easing policy.

### Layering symptoms

- **MANDATORY - READ** [z-index.md](references/z-index.md) when headers/modals/toasts overlap incorrectly, or fixes start introducing large `z-index` numbers.
- **Do NOT Load** [responsive.md](references/responsive.md) first for pure stacking-order conflicts; width logic does not solve z-axis governance.

### Foundation symptoms

- **MANDATORY - READ** [foundation.md](references/foundation.md) when global CSS precedence, reset side effects, or third-party style collisions appear.
- **Do NOT Load** [visual-details.md](references/visual-details.md) first for cascade-order bugs; polish details do not fix layer architecture.

### Token symptoms

- **MANDATORY - READ** [tokens.md](references/tokens.md) when naming scales drift, literals spread, or component APIs expose inconsistent custom properties.
- **Do NOT Load** [terminology.md](references/terminology.md) first for token-contract issues; naming vocabulary is not token governance.

### Color-system symptoms

- **MANDATORY - READ** [color.md](references/color.md) when text hierarchy is unclear, palettes are ad hoc, or dark mode appears visually unstable.
- **Do NOT Load** [typography.md](references/typography.md) first for palette-architecture issues; type rhythm does not replace color-system design.

### Spacing symptoms

- **MANDATORY - READ** [spacing.md](references/spacing.md) when section rhythm is inconsistent, magic-number `margin` spreads, `gap` vs `margin` choice is unclear, gutters ignore narrow viewports, or negative margins compensate for parent padding.
- **Do NOT Load** [spacing.md](references/spacing.md) first when the issue is purely container-query threshold math with no whitespace policy change (open [responsive.md](references/responsive.md) first).

## Reference map

| File | Responsibility | Canonical topics |
| --- | --- | --- |
| [responsive.md](references/responsive.md) | Layout escalation | intrinsic → container → media, `vw`/`vh` ban, `cqi`, `calc()` breakpoints, fluid `clamp()` |
| [typography.md](references/typography.md) | Readability and type | font stack, `text-wrap`, Japanese features, `line-height`, measure (`45ch`–`75ch`), `font-variant-numeric`, fluid type |
| [animations.md](references/animations.md) | Motion strategy | easing/duration, `transition-property: all` ban, `will-change`, interruption, `prefers-reduced-motion` implementation |
| [keyframes.md](references/keyframes.md) | `@keyframes` patterns | dashed-ident naming, global vs local, API-style custom properties, `paused + both` scroll reveal |
| [visual-details.md](references/visual-details.md) | Craft polish | concentric radii, optical alignment, layered shadows, staggered enters, exits, icon cross-fade, font smoothing, tabular numerals, image outlines, first-paint suppression |
| [accessibility.md](references/accessibility.md) | A11y baseline | contrast, focus visibility, hit area, reduced-motion policy, keyboard, ARIA, hidden semantics, `cursor: pointer` |
| [terminology.md](references/terminology.md) | Naming contract and architecture | Element, Section, Container, Inner, Outer, layout primitive vocabulary, architecture terms (`Composition` / `Utility` / `Block` / `Exception`) |
| [z-index.md](references/z-index.md) | Z-axis layering governance | absolute vs relative layering, stack tokens, `calc(infinity)`, stacking-context checks, top-layer usage |
| [foundation.md](references/foundation.md) | Base CSS architecture | reset scope, `@layer` order, low-specificity `:where()`, third-party CSS layering, a11y-safe base |
| [tokens.md](references/tokens.md) | Design-token contracts | naming grammar, family scales, global vs component aliasing, motion/depth token sets |
| [color.md](references/color.md) | Color-system strategy | HSL/OKLCH usage, palette scales, hierarchy by color+weight, dark-mode ladders, non-color redundancy |
| [spacing.md](references/spacing.md) | Whitespace rhythm | 8/4 base, scale steps, `gap` first, Grid for 2D rhythm, gutters vs gaps, responsive steps, negative-margin policy |

## Global pre-delivery checklist

Run this before shipping. Each group points at its canonical reference; open that file for the full rule set and detailed checklists.

### Responsive → [responsive.md](references/responsive.md)

- [ ] Escalation order honored (static → intrinsic → container → media).
- [ ] No `vw` or `vh`; logical viewport units chosen intentionally.
- [ ] Container queries use `container: --name / inline-size`.
- [ ] Range syntax with `calc()` thresholds; no `var()` inside `@media`/`@container` conditions.
- [ ] `width: 100%` / `height: 100%` justified; `min-width: 0` guards present where needed.
- [ ] Fluid `clamp()` retains a `rem` minimum.

### Terminology → [terminology.md](references/terminology.md)

- [ ] Canonical vocabulary used (`Inner`, `Outer`, `Gutter`, `Gap`, `Navigation`, `Menu`, `Pattern`, `Component`, `Template`, `Theme`).
- [ ] `Container` reserved for the CSS `container` feature.
- [ ] `Button` vs `Link` follows the HTML element, not appearance.

### Typography → [typography.md](references/typography.md)

- [ ] Body `line-height ≥ 1.5`; headings between `1.1` and `1.3`.
- [ ] Headings use `text-wrap: balance`; Japanese body avoids `text-wrap: pretty`.
- [ ] Japanese headings apply `palt`/`vpal`; `font-kerning` follows the `:lang(en)`/`:lang(ja)` rule.
- [ ] Prose is bounded to `45ch`–`75ch`.
- [ ] Numeric UI uses `font-variant-numeric: tabular-nums`.
- [ ] Fluid type keeps a `rem` floor.

### Animation → [animations.md](references/animations.md)

- [ ] Every animation is classified as functional or decorative.
- [ ] Functional durations ≤ `300` ms; large surfaces ≤ `500` ms.
- [ ] `transition-property: all` is never used.
- [ ] `will-change` is scoped and temporary.
- [ ] `prefers-reduced-motion` branches match the tier policy (policy in [accessibility.md](references/accessibility.md)).

### Keyframes → [keyframes.md](references/keyframes.md)

- [ ] `@keyframes` names are dashed idents.
- [ ] Globals live in `base/keyframes.css`; component-local follow `--{component}--{animation}`.
- [ ] Scroll-linked reveals use `animation-fill-mode: both` + `animation-play-state: paused`.

### Visual details → [visual-details.md](references/visual-details.md)

- [ ] Nested rounded elements satisfy `outer-radius = inner-radius + padding`.
- [ ] Shadows are layered (top / contact / ambient) with dark-mode variants.
- [ ] Lists and menus use staggered enters (~`100` ms step, total ≤ `300` ms).
- [ ] Every enter has a matching exit (`60`–`80%` duration, reversed easing).
- [ ] Icon swaps cross-fade with opacity / scale / blur.
- [ ] Live numerals use tabular numerals.
- [ ] Images on pale surfaces carry a `0.1`-alpha inner outline.
- [ ] Animations do not run on first paint.

### Accessibility → [accessibility.md](references/accessibility.md)

- [ ] Contrast `≥ 4.5:1` body / `≥ 3:1` large, in both themes.
- [ ] Every interactive element has a visible focus ring via `:focus-visible`.
- [ ] Hit area `≥ 40×40` web (`44×44` pt iOS / `48×48` dp Android).
- [ ] Reduced-motion honored per tier.
- [ ] Keyboard reachable in source order; no traps.
- [ ] Color is never the sole channel for error / success / warning / chart series.
- [ ] ARIA: native elements preferred; icon-only controls carry accessible names.
- [ ] Hidden strategy (`display: none` / `visibility: hidden` / `.visually-hidden` / `aria-hidden`) chosen deliberately.

### Z-index → [z-index.md](references/z-index.md)

- [ ] Global absolute layers are tokenized and centrally managed.
- [ ] Component-local layering uses relative rules (`0`/`1`) unless exception is justified.
- [ ] No large magic-number `z-index` values are introduced.
- [ ] Stacking-context prerequisites are verified before numeric changes.

### Foundation → [foundation.md](references/foundation.md)

- [ ] Layer order is explicit and stable (`reset` → `tokens` → `base` → `components` → `utilities` → `overrides`).
- [ ] Base selectors stay low-specificity (`:where()` where appropriate).
- [ ] Reset strategy preserves useful UA defaults and focus visibility.
- [ ] Third-party CSS precedence is controlled by layers, not selector inflation.

### Tokens → [tokens.md](references/tokens.md)

- [ ] Token names follow one grammar and family taxonomy.
- [ ] Component aliases map to global tokens; deep alias chains are avoided.
- [ ] New literals are justified; reusable values are tokenized.
- [ ] Motion/depth/z-axis token families stay aligned with their canonical references.

### Color system → [color.md](references/color.md)

- [ ] Palette groups have shade scales instead of single ad hoc values.
- [ ] Text hierarchy uses color plus weight, not size alone.
- [ ] Colored backgrounds use context-aware foreground choices.
- [ ] Dark mode uses dedicated ladders; color is not the sole communication channel.

### Spacing → [spacing.md](references/spacing.md)

- [ ] Rhythm uses the canonical scale; 8-based layout, 4 only for micro internals.
- [ ] Narrow and wide viewports use appropriate gutter/step choices, not one fixed literal everywhere.
- [ ] Sibling/cell spacing uses `gap` on Flex/Grid where possible; Grid for 2D rhythm, Flex for single-axis stacks.
- [ ] `Gutter` and `Gap` are not conflated ([terminology.md](references/terminology.md)).
- [ ] No habitual negative margins to undo parent padding; full-bleed uses layout structure.

## Anti-patterns with why

- **NEVER** jump straight to media queries for component-level breakage, **because** it locks components to viewport assumptions and increases regression risk when placement changes.
- **NEVER** use `transition-property: all`, **because** unrelated properties animate unintentionally and create avoidable paint/layout work.
- **NEVER** name by appearance (`PrimaryButtonLikeLink`), **because** semantics drift and the same component becomes unmaintainable across contexts.
- **NEVER** ship decorative high-frequency motion by default, **because** repeated exposure adds interaction friction and raises reduced-motion accessibility risk.
- **NEVER** treat typography as visual garnish, **because** readability defects cannot be compensated later by spacing, color, or motion polish.
- **NEVER** use chained child `margin` for rhythmic lists when a Flex/Grid parent could own `gap`, **because** collapsing, wrapping, and last-item hacks multiply.
- **NEVER** use negative margins routinely to cancel parent `padding`, **because** structure becomes opaque and `overflow` clipping breaks layouts silently.

## Fallback mini-playbook

Use this when quality drops late in implementation and you need a deterministic recovery path.

### Responsive fallback

1. Revert to intrinsic layout first (`wrap`, `minmax`, `max-inline-size`) and remove non-essential queries.
2. Re-introduce one named container query at a time with explicit `calc()` thresholds.
3. If still unstable, temporarily freeze to a safe single-column variant and re-expand after thresholds are recalculated.

### Typography fallback

1. Restore body baseline (`line-height >= 1.5`, measure around `45ch`-`75ch`, `rem` floor in fluid type).
2. Disable aggressive features (`text-wrap: pretty` on Japanese body, over-tight kerning) and validate readability first.
3. Re-apply advanced features (`palt`/`vpal`, `auto-phrase`) only where they improve headings without harming body text.

### Animation fallback

1. Keep only functional motion (feedback/state continuity); remove decorative enters first.
2. Cap duration (`<= 300ms` common UI, `<= 500ms` large surfaces) and switch to strong ease-out/ease-in-out curves.
3. If instability remains, reduce to opacity-only transitions and enforce reduced-motion branches before reintroducing transform effects.
