# Visual Details — Craft Principles That Make Interfaces Feel Polished

This reference is the canonical source for the ten visual-detail principles that separate "functional" interfaces from "polished" ones: concentric radii, optical alignment, layered shadows, staggered enters, subtle exits, contextual icon animations, font smoothing, tabular numerals, image outlines on pale surfaces, and first-paint animation suppression. These are small details that compound into overall craft quality.

Adjacent concerns live in their own references:

- Motion strategy (easing, duration, `prefers-reduced-motion`, interruption, press feedback, `transition-property`, `will-change`) → [animations.md](animations.md).
- Typography behavior (font stack, `text-wrap`, `line-height`, `tabular-nums` numeric ruleset) → [typography.md](typography.md).
- Hit area and focus visibility → [accessibility.md](accessibility.md).

## When to use this reference

- Before opening a PR that touches UI, run the ten principles against the component.
- When reviewing a teammate's UI, group feedback by principle using the review-output format at the bottom.
- When making multiple polish changes, batch feedback by principle so authors address one concept at a time.
- When a design looks "close but not quite there", this file usually names the gap.

## Principle 1 — Concentric border radius

When a rounded element contains another rounded element, their radii must be concentric:

```
outer-radius = inner-radius + padding
```

If the outer radius is `16px` and the padding is `8px`, the inner radius is `8px`. This applies to:

- Card → nested image.
- Button → nested icon chip.
- Dialog → nested action bar.

Common mistake: matching the inner radius to the outer radius regardless of padding. The gap at the corners looks visually "off" even when users cannot name why.

## Principle 2 — Optical alignment

Mathematical centering is rarely optically centered. Glyphs with descenders or uneven counter shapes (`▶`, `◀`, triangles, letters like `W`, `J`) need a nudge to feel centered.

- Shift right-pointing triangles `1`–`2` px to the left so the glyph's optical center aligns with the button's geometric center.
- Inside circular avatars, add `1`–`2` px of vertical offset for tall letters.
- In icon buttons, design the icon inside the hit area so its bounding box is slightly offset from the geometric center.

## Principle 3 — Layered shadows

A single `box-shadow` rarely looks right. Polished shadows stack two or three layers:

```css
box-shadow:
  0 1px 2px rgb(0 0 0 / 0.04),
  0 4px 8px rgb(0 0 0 / 0.08),
  0 12px 24px rgb(0 0 0 / 0.12);
```

- Top layer: close to the surface — `1`–`2` px offset, `2`–`4` px blur, `4%` alpha.
- Middle layer: contact shadow — `4`–`8` px offset, `8`–`16` px blur, `8%` alpha.
- Bottom layer: ambient shadow — `12`–`24` px offset, `24`–`48` px blur, `12%` alpha.
- Assume a top-down light source. Prefer positive Y offsets over symmetric blur-only shadows.

Reference table for common light/dark variants:

| Use case | Light mode | Dark mode |
| --- | --- | --- |
| Hairline + lift | `0 0 0 1px rgb(0 0 0 / 0.06), 0 1px 2px -1px rgb(0 0 0 / 0.06), 0 2px 4px 0 rgb(0 0 0 / 0.04)` | `0 0 0 1px rgb(255 255 255 / 0.08), 0 1px 2px -1px rgb(0 0 0 / 0.5), 0 2px 4px 0 rgb(0 0 0 / 0.35)` |
| Hover lift | `0 0 0 1px rgb(0 0 0 / 0.08), 0 1px 2px -1px rgb(0 0 0 / 0.08), 0 2px 4px 0 rgb(0 0 0 / 0.06)` | `0 0 0 1px rgb(255 255 255 / 0.12), 0 2px 6px -2px rgb(0 0 0 / 0.55), 0 6px 14px -4px rgb(0 0 0 / 0.4)` |
| Elevated surface | `0 1px 2px rgb(0 0 0 / 0.04), 0 4px 8px rgb(0 0 0 / 0.08), 0 12px 24px rgb(0 0 0 / 0.12)` | `0 1px 2px rgb(0 0 0 / 0.3), 0 4px 8px rgb(0 0 0 / 0.4), inset 0 1px 0 rgb(255 255 255 / 0.04)` |

In dark mode, reduce alpha and add a faint inner highlight so the surface reads as lifted, not flat:

```css
.surface {
  box-shadow:
    0 1px 2px rgb(0 0 0 / 0.3),
    0 4px 8px rgb(0 0 0 / 0.4),
    inset 0 1px 0 rgb(255 255 255 / 0.04);
}
```

## Principle 3.5 — Use fewer borders

When separating surfaces, borders are only one option and often not the best default.

- Prefer layered shadows for subtle separation on variable backgrounds.
- Prefer background contrast and spacing before adding hard border lines.
- If a border is required, keep it low contrast and ensure it does not compete with text hierarchy.

## Principle 4 — Staggered enter transitions

Lists, grids, and menus feel alive when children enter on a slight delay from one another.

- Use around `100ms` between semantic chunks.
- Cap the total sequence at `300ms`; beyond that, users wait.
- `animation-delay: calc(var(--index) * 100ms)` with `--index` computed from the DOM position works well.
- Under `prefers-reduced-motion`, collapse the stagger to a single fade (see [accessibility.md](accessibility.md)).

## Principle 5 — Subtle exits

Exits are the forgotten half of animation. A polished component matches its enter with a corresponding exit:

- Exit duration is `60`–`80%` of the enter duration (fast but not abrupt).
- Exit easing is the reverse of the enter easing (`ease-out` in → `ease-in` out).
- When the destination is `display: none`, pair with `transition-behavior: allow-discrete` and `@starting-style` (see [animations.md](animations.md)).

## Principle 6 — Contextual icon animations

Icons that change meaning on interaction should cross-fade their glyphs rather than swap visibility.

- Cross-fade with opacity `0 → 1`, scale `0.25 → 1`, and blur `4px → 0`.
- Duration `150`–`200` ms.
- If a motion library is available, use a spring transition (`duration: 0.3`, `bounce: 0`) to avoid playful overshoot.
- Without a motion library, keep both icons in the DOM and cross-fade with CSS using `cubic-bezier(0.2, 0, 0, 1)`.
- Examples: check mark on save, reveal/hide on password fields, play/pause on media controls.
- Do not scale tiny glyph assets to large decorative sizes; use icon artwork designed for the target size.

## Principle 7 — Font smoothing

On macOS and iOS WebKit, body text below `400` weight benefits from:

```css
:root {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

Do not apply to all body text unconditionally on Windows; subpixel anti-aliasing is often preferred there.

## Principle 8 — Tabular numerals

Any number that updates in place must use tabular numerals so digits do not shift horizontally.

```css
.counter, .price, .timer {
  font-variant-numeric: tabular-nums;
}
```

Applies to:

- Counters, timers, progress percentages.
- Price ladders and tables of numbers.
- Vote counts, notification badges.

Detailed typographic rules and edge cases (proportional vs tabular for prose, `lining-nums`, ordinal/slash feature combinations) live in [typography.md](typography.md).

## Principle 9 — Image outlines on pale surfaces

Images on pale backgrounds can look like they "float" off the surface. A `1` px inner border at low alpha anchors them:

```css
.card img {
  box-shadow: inset 0 0 0 1px rgb(0 0 0 / 0.1);
}
```

In dark mode, use pure white at the same alpha:

```css
@media (prefers-color-scheme: dark) {
  .card img {
    box-shadow: inset 0 0 0 1px rgb(255 255 255 / 0.1);
  }
}
```

- If the product uses a class-based or `[data-theme]`-based theme switch, mirror the same declaration inside that selector.
- Keep the outline neutral (pure black/pure white), not tinted neutrals that pick up background color.
- Skip for decorative background images that already have strong edges.

## Principle 10 — Skip animation on first paint

Any animation defined on components that render on first paint should be suppressed during load so the page does not "wave in".

- For AnimatePresence-like APIs, set `initial={false}` for default-state elements.
- Add `data-loaded` on `<html>` after `DOMContentLoaded` for CSS-driven flows.
- Scope animations with `html[data-loaded] .component` so they only run after initial paint.
- Alternatively, use `animation-delay: var(--delay-after-load, 0s)` with a short delay.

## Common-mistakes table

Independent-from-other-references polish mistakes. Items owned by other references (transition-property, will-change, press feedback, text-wrap, hit area, line-height) are not re-listed here; see [Related references](#related-references).

| Area | Mistake | Correction |
| --- | --- | --- |
| Border radius | Equal inner and outer radius with padding | `outer-radius = inner-radius + padding` (principle 1) |
| Alignment | Pure mathematical centering of asymmetric glyphs | Optical shift of `1`–`2` px (principle 2) |
| Shadows | Single `box-shadow` | Two-to-three-layer stack with alpha (principle 3) |
| Separation | Heavy borders on every surface | Prefer shadows, spacing, or surface contrast; border only when necessary (principle 3.5) |
| Enters | All children enter at once | Stagger by ~`100` ms, cap total at `300` ms (principle 4) |
| Exits | No matching exit animation | `60`–`80%` of enter, reversed easing (principle 5) |
| Icons | Toggle visibility between two glyphs | Cross-fade with opacity/scale/blur (principle 6) |
| Font smoothing | Unconditional `antialiased` on Windows | Target macOS/iOS WebKit, let Windows keep subpixel (principle 7) |
| Numbers | Proportional numerals on live counters | `font-variant-numeric: tabular-nums` (principle 8) |
| Images | No inner border on pale backgrounds | `inset box-shadow` using `rgb(0 0 0 / 0.1)` (light) and `rgb(255 255 255 / 0.1)` (dark) (principle 9) |
| First paint | Animations run on page load | Gate with `html[data-loaded]` (principle 10) |
| Dark mode | Reuse light-mode shadows | Reduce alpha, add inner highlight (principle 3) |

## Review-output format

When opening a polish review, write feedback as a markdown table grouped by principle. Use the exact structure below so authors can scan changes quickly.

```markdown
## Polish Review — {Component Name}

### Border radius (principle 1)
| | Before | After |
| --- | --- | --- |
| Card image | `border-radius: 16px` inside `8`-px-padded card | `border-radius: 8px` to match `outer − padding` |

### Shadows (principle 3)
| | Before | After |
| --- | --- | --- |
| Card | `box-shadow: 0 2px 8px rgb(0 0 0 / 0.1)` | Three-layer stack (top/contact/ambient) |

### Hit area (→ accessibility.md)
| | Before | After |
| --- | --- | --- |
| Menu icon | `24×24` px without padding | Expand to `40×40` with `::before` (policy in accessibility.md) |
```

Rules:

- One heading per principle so the author can address them in any order.
- `Before | After` columns show the diff at the property level.
- Use file references (`components/card.tsx`, etc.) when a change spans multiple files.

## Checklist

- [ ] Concentric radii verified on every nested rounded element. (1)
- [ ] Optical alignment verified on triangles, chevrons, and tall letters. (2)
- [ ] Shadows are layered; dark-mode variant reviewed. (3)
- [ ] Surface separation uses shadows/spacing/contrast before hard borders. (3.5)
- [ ] Lists and menus have staggered enters with ~`100` ms delay; total cap `300` ms. (4)
- [ ] Every enter has a matching exit (`60`–`80%` duration, reversed easing). (5)
- [ ] Icon swaps cross-fade with opacity/scale/blur, not visibility toggling. (6)
- [ ] Font smoothing applied on WebKit body text where appropriate. (7)
- [ ] Live counters, prices, and timers use tabular numerals. (8)
- [ ] Images on pale backgrounds carry `0.1`-alpha inner outlines (black in light, white in dark). (9)
- [ ] Page load does not trigger component animations. (10)

## Related references

- [animations.md](animations.md) — motion strategy, easing/duration tokens, interruption, `prefers-reduced-motion` implementation, press feedback (`scale(0.96)`), `transition-property: all` ban, `will-change` discipline.
- [typography.md](typography.md) — `text-wrap: balance`/`pretty`, fluid type, Japanese typography, detailed `font-variant-numeric` ruleset.
- [accessibility.md](accessibility.md) — contrast, focus visibility, hit area minimums, reduced-motion policy.
- [keyframes.md](keyframes.md) — `@keyframes` naming and composable patterns for staggered enters and exits.
