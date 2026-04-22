# Responsive CSS Rules

The goal of this reference is to make responsive decisions deterministic and to minimise the number of breakpoints and the amount of CSS you have to maintain. Treat CSS as a proposal to the browser, not a command: delegate work to the engine when it can do the job on its own.

## When to use this reference

- Choosing between intrinsic sizing, container queries, media queries, and viewport units.
- Deciding whether a component needs a query at all or can rely on layout primitives.
- Naming and scoping `container`-property usage.
- Replacing `vw` / `vh` with logical viewport units (`svi`/`dvi`/`lvi`/`svb`/`dvb`/`lvb`).
- Writing `@container` rules with `inline-size` and range syntax.
- Computing `calc()`-based breakpoints from column counts, gaps, and content widths.
- Building a `clamp(min, slope × unit + intercept, max)` fluid value.
- Reaching for `zoom` as a last-resort responsive escape hatch.

## Loading boundaries

- **Load this reference first** when the issue is about layout breakpoints, component width behavior, container-query design, or fluid sizing math.
- **Do not load this reference first** when the issue is primarily readability/line breaking (open [typography.md](typography.md)) or motion feel/performance (open [animations.md](animations.md)).

## Intrinsic baseline

Responsive rules in this file follow an intrinsic baseline:

- **Contracting and expanding**: layouts must survive both narrower and wider space without manual breakpoint inflation.
- **Flexibility**: allow grid/flex/intrinsic sizing to absorb change before introducing query branches.
- **Viewport awareness**: use viewport units intentionally for page scope, not as a default component sizing mechanism.

Treat responsive work as declaring constraints and intent. Let the browser compute the final arrangement.

## Decision rules before writing queries

Apply these as independent checks. Do not bundle them into a single category.

### Pixel-perfect is not the target

- Do not preserve static comp-perfect geometry at all widths.
- Prioritize legibility, operability, and stable content flow over exact visual lockstep.
- If preserving exact geometry requires extra breakpoints, prefer intrinsic relaxation instead.

### Browser delegation comes first

- Prefer intrinsic sizing, wrap behavior, and auto-placement before writing query branches.
- If the engine can resolve a layout safely, do not force a hard width script in CSS.
- Queries are for unresolved structural decisions, not for replacing native layout behavior.

### Design for change

- Assume copy expansion, localization growth, CMS variability, and optional element injection.
- Validate the same component in narrow columns, sidebars, and full-width placements.
- Keep overflow survivable: `min-width: 0`, wrapping, and bounded measure before hard clipping.

### Split component scope from page scope

- Use `@container` for component adaptation to parent space.
- Use `@media` for viewport-level page structure and environment-level conditions.
- If a rule can be moved with the component between contexts, it belongs to container scope.

### Avoid device-category assumptions

- Never start from `sp`/`tablet`/`desktop` buckets.
- Derive thresholds from content break conditions.
- Name and document thresholds by layout reason, not device labels.

## Escalation order

Try each tier in order. If a tier solves the problem, do not reach for the next one.

### 0. Static

Not every element needs to be responsive. Keep the following static:

- Tags, badges, labels, and other small UI with little content.
- Icons (`width: 1em` is enough; they follow font-size).
- Decorative borders and dividers.
- Fixed-size avatars and logomarks.

Applying `clamp()` or queries to these only adds complexity.

### 1. Intrinsic responsiveness

Use mechanisms that adapt without any query at all:

- `auto` / `fit-content` / `min-content` / `max-content` natural sizing.
- `flex-wrap: wrap` for natural line breaks.
- `grid` with `auto-fit` / `auto-fill` and `minmax()` for column auto-adjustment.
- `clamp()` / `min()` / `max()` for fluid sizing.
- `max-inline-size` as an upper bound rather than a fixed `inline-size`.

For layout primitives, prefer the flexible component-agnostic layout system defined in `@layer composition`.

### 2. Container queries

Use container queries when a component must react to the size of its own parent, not the viewport.

Apply them when:

- A component is placed in multiple contexts (sidebar, modal, card) and must adapt to each.
- Layout depends on placement width, not viewport width.

#### `container-name` is mandatory

When containers nest, a bare `@container` rule becomes ambiguous. Always name the container.

Correct:

```css
:scope {
  container: --cards / inline-size;
}

@container --cards (inline-size >= calc(420 / 16 * 1rem)) { /* component rules */ }
```

Forbidden (no name):

```css
:scope {
  container-type: inline-size;
}

@container (inline-size >= calc(420 / 16 * 1rem)) { /* component rules */ }
```

#### `container-name` must be a dashed ident

Always start the name with `--`.

Correct:

```css
:scope { container: --cards / inline-size; }
@container --cards (inline-size >= calc(420 / 16 * 1rem)) { /* component rules */ }
```

Forbidden:

```css
:scope { container: cards / inline-size; }
@container cards (inline-size >= calc(420 / 16 * 1rem)) { /* component rules */ }
```

Reasons:

- Modern CSS increasingly requires `--` on user-defined identifiers (`anchor-name`, `animation-timeline`, etc.). A single rule beats per-property memorisation.
- You no longer have to remember which properties demand the prefix.
- Future spec keywords are less likely to collide with your names.
- You can see at a glance that the name is yours.

#### Where to apply `container`

- Apply `container` on the component root or the specific inner element that actually needs it.
- Do not slap `container-type` on every wrapper "just in case". It has side effects (see below).
- Do not create a utility class named `.container`.

#### Use of the `.container` class name

- Because the `container` property exists, `container` is now a meaningful CSS word on par with `grid`.
- `.***-container` may be used only on an element that actually sets the `container` property, and the name must be specific: `.sidebar-container`, not `.container`. `.container` on its own fails to say "container of what".
- Generic wrappers without a `container` property must not use `.container`.

#### Caveats

- An element with `container-type: inline-size` cannot match an `@container` query against its own size (self-reference would loop). Set the container on the parent and query from its children.
- `container-type: inline-size` imposes inline-size containment, which is incompatible with `subgrid` on the same element. When using `subgrid`, set the container on the grid parent and compute breakpoints for the subgrid items with `calc()`.
- `container-type` implicitly applies `contain: inline-size`. Elements whose width depends on their content (`width: fit-content`) can collapse to an unexpectedly small size.
  - Do not set `container-type` on elements that are naturally inline or that have intrinsic widths.
  - Watch out for flex items without `flex-grow`/`flex-basis` and `auto`-sized or intrinsic grid items.
- In engines that still retain the older implicit `contain: layout` behaviour, `position: fixed` descendants of a container can be broken. Avoid placing `position: fixed` content inside a container.
- Do not set `padding`, `border`, or other layout properties on the container element itself. They perturb the container's computed inline size and shift the `@container` thresholds and `cqi` calculations. Keep the container element as a pure size reference and handle layout on its children.
- While you can style `<picture>` below an `@container` rule, the `media` attribute on `<source>` does not understand container queries. Use viewport-based `media` for source switching, and do source selection in markup or a different mechanism for component-width switching.
- `container-type: size` only works if the container has a guaranteed block size. `min-block-size` is not enough, so this value is rarely useful in practice. Avoid it by default.

#### Prohibited

- Do not set `container-type` on `html`, `body`, or any page-level layout root. Page-level responsiveness belongs to media queries.
  - While all core browsers now handle this, older implementations still apply the implicit `contain: layout`, which breaks `position: fixed` descendants.
  - The container-query proposer, Miriam Suzanne, has publicly called this pattern an anti-pattern in her talks.
- Never use `container-type` on its own; always use the `container` shorthand with a dashed-ident `container-name`.
- Outside `:scope`, any element that sets `container-type` must also carry a `.***-container` class name.

### 3. Media queries

Use media queries only when higher tiers cannot solve the problem:

- Swapping page-level macro layout (2-column ↔ 1-column).
- Elements anchored to the viewport (modal, toast, popover content).
- Blocks guaranteed to span 100% of the page and never appear in any other context (e.g., a hero header).

## Viewport and container units

### `vw` is banned

`vw` collapses to large-viewport-based calculation, which is ambiguous and unsafe. For the inline axis, pick the logical unit that matches the intent:

- `svi`: smallest inline size while browser UI is visible; use when the content must fit even with toolbars shown.
- `dvi`: dynamic inline size following the UI's visible area.
- `lvi`: largest inline size when the UI is hidden.

Default to `svi`. This aligns with the fact that `cqi`, when no query container is found, falls back to `svi`.

### `vh` is banned

`vh` resolves to the large-viewport height, which causes overflow or oversize on mobile when browser chrome is present. Use logical block-axis units:

- `svb`: smallest block size while browser UI is visible.
- `dvb`: tracks the currently visible height.
- `lvb`: largest block size when UI is hidden.

Default to `svb`. Avoid `dvb` because it triggers layout shift as the URL bar collapses and reappears. Use `lvb` when you must occupy the full height regardless of UI state (e.g., a `position: fixed` background).

### Viewport units travel with media queries

Viewport units couple to page-level state. Keep `svi`/`dvi`/`lvi`/`svb`/`dvb`/`lvb` in step with media queries and page-level layout decisions:

- Use them for page-level padding, hero sections, full-bleed backgrounds, or any value that only makes sense against the whole view.
- Do not size a component's own `inline-size`, `block-size`, or `font-size` from viewport units when it may be placed in multiple contexts.
- If a component can be dropped into different contexts, prefer container queries over viewport units.

### `cqi` units travel with container queries

`cqi`, `cqb`, `cqw`, `cqmin`, `cqmax` assume a named query container is present. Do not scatter `cqi` inside a component without thinking.

- `cqi` belongs on descendants. Do not use it for the container's own self-sizing.
- Verify that the same component defines `container: --name / inline-size` and at least one named `@container --name` rule.
- If a valid query container is not guaranteed, do not use `cqi`.
- `cqb`, `cqw`, `cqmin`, `cqmax` require `container-type: size`, and `container-type: size` in turn needs a fixed block size. That rules them out for most real-world cases. Avoid them by default.

If no query container is in scope, container-query length units fall back to small-viewport units. Writing `cqi` in a component's base styles therefore makes the computed value depend on where the component is placed.

### Implementation notes for `sv*` / `dv*` / `lv*`

- Direct use of `svi`/`dvi`/`lvi`/`svb`/`dvb`/`lvb` on Chromium browsers can resist user zoom and hurt accessibility.
- Use `sv*`/`dv*`/`lv*` only when unavoidable. Prefer `%` or intrinsic layout when either works.
- When fluid values from viewport units are used project-wide, centralise them in tokens or utilities rather than writing raw units everywhere.
- Chrome 145 introduced conditional `vw` computation that excludes the scrollbar when `:root` carries `scrollbar-gutter: stable` (the Kiso CSS setup does this, so `vw` excludes the scrollbar on Chrome).
  - Safari and Firefox still include the scrollbar; `inline-size: 100vw` can produce horizontal scroll.
  - `inline-size: 100vw` is often unnecessary or replaceable. Even if all engines converged, it remains a code smell worth flagging.
- For full-screen UIs, prefer `min-block-size` over a fixed `block-size` so that content overflow is survivable.

## Query syntax rules

### Use range syntax

Both media and container queries use comparison operators (`>=`, `<=`, `>`, `<`). The `min-width` / `max-width` prefix syntax is banned.

Correct:

```css
@media (width >= calc(720 / 16 * 1rem)) { /* responsive overrides */ }
@container --card (inline-size >= calc(420 / 16 * 1rem)) { /* responsive overrides */ }
```

Forbidden:

```css
@media (min-width: calc(720 / 16 * 1rem)) { /* responsive overrides */ }
@container --card (min-width: calc(420 / 16 * 1rem)) { /* responsive overrides */ }
```

### Container queries use `inline-size`, not `width`

Container queries are logical by design; match them with logical keywords.

Correct:

```css
@container --card (inline-size >= calc(420 / 16 * 1rem)) { /* responsive overrides */ }
```

Forbidden:

```css
@container --card (width >= calc(420 / 16 * 1rem)) { /* responsive overrides */ }
```

## Strategy by cascade layer

### `@layer pages`

Page-level macro layout follows the viewport. Prefer media queries.

### `@layer components`

Components cannot predict their placement, so they should react to parent size rather than viewport. Prefer container queries.

Exception: components that are anchored to the viewport (modals, toasts) rely on media queries.

## Breakpoints

### No device-named breakpoints

With more than 2,000 device sizes in use, labels like `sp` / `tablet` / `pc` are meaningless. Names that imply device categories are banned.

### Breakpoints follow content

Set the breakpoint where the layout starts to break. Display-swap classes like `.sp-only` / `.pc-only` are not allowed.

### Breakpoint unit

Use `rem` for media-query breakpoints. A user who enlarges the base font has less usable space, and `rem` breakpoints track that correctly. Combine with `calc()` so pixel intent stays legible: `@media (width >= calc(640 / 16 * 1rem))`.

### Use `calc()` to avoid magic numbers

`calc()` is not only for arithmetic. It is how you encode *why* a number exists. Write thresholds and sizes as the sum of their components:

- Column min-width × column count.
- Item width × count + gap × gaps.
- Content width + padding + border.
- Differences between baseline sizes that define a slope.

This turns `48rem` or `960px` from "some number I chose" into "the width at which this layout becomes viable".

#### Principle

Decide thresholds from content, not device categories. Do not pre-bucket into `sp` / `tablet` / `pc` before you know how many things need to fit at what width.

```css
._card-group {
  @container --card-group (calc(160 / 16 * 1rem * 6 + 24 / 16 * 1rem * 5) > inline-size >= calc(160 / 16 * 1rem * 4 + 24 / 16 * 1rem * 3)) {
    & > :nth-child(2n + 1):nth-last-child(1) {
      /* If there's one odd item left over, centre it by starting in column 2. */
      grid-column-start: 2;
    }
  }
}
```

Thresholds express the reason, not a flat number.

#### Recommended

- Expand query thresholds into `calc()` form with the constituent parts visible.
- Use expressions inside `clamp()`, `min()`, `max()` for the same reason.
- Include gaps and padding when they are part of the threshold.
- Use `calc()` for unit conversion (`px` → `rem`).
- When an expression is dense, annotate with a comment describing "N columns × M items × G gaps".

#### Do not reference custom properties from query conditions

`calc()` works in query conditions, but `var()` substitution does not. A query condition is a syntactic construct, not a property value.

AI code generators frequently emit mistakes like this:

```css
/* Forbidden: var() inside a query condition */
:scope {
  --_column-count: 3;
  --_column-min-width: calc(160 / 16 * 1rem);
  --_column-gap: calc(24 / 16 * 1rem);

  container: --article-cards / inline-size;
}

._card {
  @container --article-cards (inline-size >= calc(var(--_column-width) * var(--_column-count) + var(--_column-gap) * (var(--_column-count) - 1))) {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
```

Query conditions must use literal numbers:

```css
._card {
  @container --article-cards (inline-size >= calc(160 / 16 * 1rem * 3 + 24 / 16 * 1rem * 2)) {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
```

`var()` is fine inside property values:

```css
._card {
  --_column-count: 3;

  display: grid;
  grid-template-columns: repeat(var(--_column-count), minmax(0, 1fr));
}
```

#### Note on AI-generated CSS

Generators regularly produce `var()` inside query conditions. Never accept such output; rewrite the condition with literal `calc()` arithmetic. At minimum, check:

- That no `var()` appears inside `@media` or `@container` conditions.
- That the condition expresses a layout break-point reason rather than a device-width convention.
- That gap, column count, and min width are present when required.

#### Avoid

- Wrapping a bare number in `calc()` (`calc(48rem)`) without further reasoning.
- Inlining one-off giant expressions with no comment.
- Forcing a query-plus-`calc()` solution onto a problem that intrinsic layout already solves.
- Using `var()` for condition reuse across queries.

#### When to prefer `calc()`

Prefer `calc()` when either of the following is true:

- Expressing the value as an expression makes the intent clearer.
- The column count, item count, gap, or minimum width might change later.

If the number really is fixed and decomposing it adds no meaning, leave it alone.

## Fluid sizing

Interpolate between a minimum and a maximum with `clamp(min, preferred, max)`. No breakpoints needed.

### Structure

The preferred value is a sum of a fixed `rem` part and a context-appropriate relative unit (`100svi` / `100dvi` / `100lvi` / `100svb` / `100dvb` / `100lvb` / `100cqi`). Page-scale fluid values use viewport units; component-scale fluid values use `cqi` units.

```
clamp(min-value, intercept + slope × relative-unit, max-value)
```

- **min-value**: the `rem` lower bound.
- **max-value**: the `rem` upper bound.
- **slope**: rate of change per unit of the reference width.
- **intercept**: y-intercept — the value the linear function reaches when the reference is 0.
- **relative-unit**: the reference unit (`100svi`, `100dvi`, `100lvi`, `100svb`, `100dvb`, `100lvb`, `100cqi`, …).

### The math

Two anchor points:

- **min-reference**: smallest reference width in pixels (viewport for page scope, container for component scope). Example: 400.
- **max-reference**: largest reference width in pixels. Example: 1280.
- **min-size**: value at min-reference, in pixels. Example: 14.
- **max-size**: value at max-reference, in pixels. Example: 18.
- **base-font-size**: root font size (typically 16).

Step 1 — slope:

```
slope = (max-size − min-size) / (max-reference − min-reference)
```

Example: `(18 − 14) / (1280 − 400) = 4 / 880 ≈ 0.00455`.

Step 2 — intercept:

```
intercept = min-size − slope × min-reference
```

Example: `14 − 0.00455 × 400 = 14 − 1.82 = 12.18`.

Step 3 — assemble the `clamp()`:

```css
clamp(
  min-size / base-font-size * 1rem,
  slope × relative-unit + intercept / base-font-size * 1rem,
  max-size / base-font-size * 1rem
)
```

Applied:

```css
font-size: clamp(
  14 / 16 * 1rem,
  0.00455 * 100svi + 12.18 / 16 * 1rem,
  18 / 16 * 1rem
);
```

### When tokens carry unitless numbers

If the design system holds sizes as unitless numbers, do the math in CSS with custom properties:

```css
--_slope: calc(
  (var(--_max-size) - var(--_min-size)) /
  (var(--_max-reference) - var(--_min-reference))
);
--_intercept: calc(
  var(--_min-size) - var(--_slope) * var(--_min-reference)
);

font-size: clamp(
  var(--_min-size) / 16 * 1rem,
  var(--_slope) * 100svi + var(--_intercept) / 16 * 1rem,
  var(--_max-size) / 16 * 1rem
);
```

### Rules

- `vw` is banned; choose `svi` / `dvi` / `lvi` by context at page scope.
- `vh` is banned; choose `svh` / `dvh` / `lvh` (or logical `svb` / `dvb` / `lvb`) by context.
- Never use `svi` / `dvi` / `lvi` / `svh` / `dvh` / `lvh` / `svb` / `dvb` / `lvb` alone for `font-size`: user font-size settings get ignored.
- When legibility matters, keep the preferred expression as `rem + relative-unit`, and always fix the minimum to a `rem`.
- Use `cqi` only inside a descendant where a named query container is guaranteed.
- Viewport units pair with media queries; `cqi` units pair with container queries.

## Layout patterns

### Avoid fixed sizes

- Prefer `max-inline-size` over a fixed `width`.
- Prefer `min-block-size` or `aspect-ratio` over a fixed `height`.
- If a fixed value is required, guard it with `min(100%, var(--_size))` to prevent overflow.

### `zoom` as the final safety net

- `zoom` is the last resort. Do not make it the primary responsive tool; intrinsic layout, container queries, and media queries come first.
- Use it only on components that have an identified minimum width below which neither reflow nor column reduction can save the design.
- Treat it as progressive enhancement. Where `progress()` is not supported, the component must still be legible and operable.
- Never use it "to preserve the visual exactly". Try column reduction, wrapping, and whitespace compression first.
- Apply `zoom` on the component root only, inside a guaranteed query-container context.

AI heuristic:

- Try intrinsic layout first.
- Try `@container` layout changes next.
- Only when the component still breaks below its minimum width, reach for `zoom`.
- Cap `zoom` at `1`; never enlarge.
- Do not use `zoom` as a substitute for shrinking type via viewport units.

```css
:scope {
  container: --article-cards / inline-size;
}

@container --article-cards (inline-size < calc(200 / 16 * 1rem)) {
  ._card {
    /* Allow shrink below the minimum, but never enlarge. */
    zoom: min(progress(100cqi, 0px, calc(200 / 16 * 1rem)), 1);
  }
}
```

This pattern is an emergency valve for components that do not know where they will land. It is not a default technique.

## Checklist

- [ ] No `vw` or `vh`. Logical viewport units (`svi`/`dvi`/`lvi`/`svb`/`dvb`/`lvb`) are chosen intentionally, with `svi` as the default.
- [ ] Container queries use `container: --name / inline-size` with a dashed-ident name; `container-type` alone is never used.
- [ ] Query conditions use range syntax (`>=`, `<=`) with `calc()` that expresses layout thresholds (column count × min width + gap × gaps), not arbitrary numbers.
- [ ] No `var()` inside `@media` or `@container` conditions.
- [ ] `cqi` is only used inside a descendant of a named container.
- [ ] `width: 100%` and `height: 100%` are justified, not reflexive.
- [ ] `min-width: 0` guards exist where flex/grid items contain long text, `<input>`, or horizontally-scrolling tables.
- [ ] Fluid `clamp()` values keep a `rem` minimum so user zoom scales the floor.
- [ ] `zoom` is used only as an emergency valve, capped at `1`, and inside a named query container.

## Fallback mini-playbook

When responsive work starts oscillating or regressions spread, recover in this order:

1. Remove non-essential queries and return to intrinsic layout (`wrap`, `minmax`, `max-inline-size`).
2. Re-introduce only one named container query with explicit `calc()` thresholds.
3. If still broken, lock a safe single-column baseline, then add complexity back after threshold math is validated.

## Related references

- [terminology.md](terminology.md) — `Container`, `Inner`, `Outer`, `Gutter`, `Gap` definitions that back this file's vocabulary.
- [typography.md](typography.md) — fluid-type `clamp()` math and readable measure (`45ch`–`75ch`).
- [animations.md](animations.md) — interaction between layout-triggering animations and responsive containment.
