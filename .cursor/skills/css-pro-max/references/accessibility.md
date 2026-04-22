# Accessibility Baseline

This reference is the canonical source for accessibility baselines across the design system: contrast targets, focus visibility, hit area minimums, reduced-motion policy, keyboard operability, color-only information, ARIA baselines, and hidden-element semantics. Implementation-level CSS for these topics may live elsewhere (e.g. `animations.md` for reduced-motion code patterns), but the policy — *what* must be guaranteed and *why* — lives here.

## When to use this reference

- Deciding whether a color pair, focus style, tap target, or motion policy is acceptable for shipping.
- Reviewing a component for accessibility blockers.
- Setting up `:focus-visible` handling, replacement focus rings, or tokenised focus styles.
- Expanding a small visual element's hit area to the platform minimum.
- Choosing between `display: none`, `visibility: hidden`, and `aria-hidden="true"`.
- Deciding whether an animation must be disabled, simplified, or shortened under `prefers-reduced-motion`.
- Writing an accessibility checklist for a release gate.

## Contrast

### Targets

- Body text: at least `4.5:1` against its background.
- Large text (≥ `18pt` regular or `14pt` bold, roughly `1.5rem`): at least `3:1`.
- Non-text UI (icons conveying meaning, form borders, focus rings): at least `3:1` against adjacent colors.

### Testing rules

- Verify in **both light and dark themes**. Dark-mode fallback often fails when designers tune only the light palette.
- Test against the actual surface color, not the page background. A card on a tinted surface may pass against the page and fail against the card.
- Disabled states are exempt from contrast minimums by WCAG, but keep them distinguishable enough to avoid user confusion.

### Token strategy

- Define semantic color tokens (`--color--text`, `--color--text-muted`, `--color--surface`, `--color--border`) and swap them via `prefers-color-scheme`.
- Do not inline hex values for functional text color.
- Map functional colors (`success`, `warning`, `danger`, `info`) to semantic tokens so dark-mode swaps are consistent.

## Focus visibility

### Must-haves

- Every interactive element has a visible focus indicator at all times for keyboard users.
- Rings are `2`–`4` px, `3:1` contrast against the element's background.
- `:focus-visible` is the primary hook. Avoid bare `:focus` except as a fallback.
- `outline: 0` without a visible replacement is forbidden.

### Pattern

```css
:where(button, a, [role="button"], [tabindex]):focus-visible {
  outline: calc(2 / 16 * 1rem) solid var(--color--focus-ring);
  outline-offset: calc(2 / 16 * 1rem);
}
```

### Anti-patterns

- Removing `outline` in a reset without providing a replacement.
- Styling `:focus` for mouse users in a way that keeps the ring from appearing for keyboard users.
- Hiding the ring "because the design doesn't include one." That is a guideline violation.
- Relying on color change alone. Focus must change *shape* or *outline*, not only color.

## Hit area

### Targets

- Web default: `**40×40*`* px minimum on any interactive element.
- iOS apps: `44×44` pt.
- Android apps: `48×48` dp.

### Expansion pattern

When the visual element is smaller than the minimum, expand the hit area with padding or a pseudo-element:

```css
.icon-button {
  position: relative;
  inline-size: calc(24 / 16 * 1rem);
  block-size: calc(24 / 16 * 1rem);
}

.icon-button::before {
  content: "";
  position: absolute;
  inset: calc(-8 / 16 * 1rem);
}
```

Rules:

- Single-character buttons must still honor the minimum.
- Adjacent hit zones must not overlap; reserve `8` px of separation.
- `@media (pointer: coarse)` is a fine place to enlarge beyond `40×40` for touch-first surfaces.

## Reduced-motion policy

### Principle

`prefers-reduced-motion: reduce` is a user request. Respect it. Never blanket-disable all animation — respond per tier.

### Tier policy


| Tier     | Policy                                                              | Typical motion                                                                      |
| -------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Disable  | Define only inside `@media (prefers-reduced-motion: no-preference)` | Parallax, auto-looping carousels, marquees, large transform-based scroll animations |
| Simplify | Reduce to a crossfade or fade                                       | Page-level View Transitions, large surface enter/exit                               |
| Shorten  | Cut duration aggressively (`≤ 50ms`)                                | Tooltip or popover fade-in                                                          |
| Keep     | No change required                                                  | Spinners, progress bars, focus-ring appearance                                      |


### What counts as "large motion"

If any of the following are true, treat the motion as *large* and at minimum simplify it:

- Translation that affects 1/3 of the screen or more.
- Rotation.
- Scale change ≥ `0.5`.
- Scroll-driven transforms.
- Visible vibration or shake.

### Implementation

Implementation patterns and code (`@media` gating, `animation-play-state` tricks, View Transitions skip) live in [animations.md](animations.md). This file defines the policy; that file defines the code.

## Keyboard operability

- Every interactive element must be reachable via `Tab` in a meaningful order.
- Custom tab order (via `tabindex > 0`) is forbidden except in exceptional cases. Use source order.
- Skip links (`href="#main"`) must be provided on pages with long navigation.
- No keyboard traps: focus must be able to leave any widget, including dialogs and menus.
- Dialog open must move focus into the dialog; dialog close must restore focus to the trigger.
- Custom controls must honor their ARIA role's keyboard contract (e.g. combobox `↑/↓/Enter/Esc`, radio group `←/→`).

## Color-only information

Color must never be the sole carrier of meaning.

- Error, success, warning, and info states pair color with text, icon, or shape.
- Chart series pair color with pattern, shape, or direct label.
- Required form fields pair color with text (`*` plus label) or `aria-required="true"`.
- Link color difference is supplemented by underline or another affordance for non-nav links inside prose.

## ARIA baseline

- Prefer native elements: `<button>`, `<a href>`, `<input>`, `<select>`, `<dialog>`, `<details>`. The built-in semantics beat any ARIA substitute.
- `role="button"` on `<a>` is worse than using `<button>`. Only accept it when navigation semantics are also required and there is a documented reason.
- Icon-only controls require `aria-label` or visually hidden text.
- Error summaries and async status messages use `role="alert"` or `aria-live="polite"` / `aria-live="assertive"`.
- `aria-hidden="true"` on focusable content is broken; clear focus first or do not hide.
- Form fields must be programmatically associated with their labels (`<label for>`, `aria-labelledby`, or implicit nesting).

## Hidden semantics — pick deliberately


| Technique                 | In accessibility tree? | Takes up space? | Focusable?      | Use case                                                     |
| ------------------------- | ---------------------- | --------------- | --------------- | ------------------------------------------------------------ |
| `display: none`           | No                     | No              | No              | Fully removed from flow and a11y tree                        |
| `visibility: hidden`      | No                     | Yes             | No              | Reserves space; hide visually and from a11y                  |
| `hidden` attribute        | No                     | No              | No              | Semantic "not currently relevant"                            |
| `aria-hidden="true"`      | No                     | Yes             | Yes (dangerous) | Visual-only; hide from AT while visible. Clear focus first.  |
| `.visually-hidden` (clip) | Yes                    | No              | Yes             | Visually hide but keep for screen readers                    |
| `opacity: 0`              | Yes                    | Yes             | Yes             | Visual-only fade; still reachable — usually wrong for hiding |


Rules:

- Do not combine `aria-hidden="true"` with focusable descendants.
- Do not use `transform: scale(0)` to hide: the element remains in the a11y tree.
- `.visually-hidden` is the canonical screen-reader-only pattern:

```css
.visually-hidden {
  position: absolute;
  inline-size: 1px;
  block-size: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
```

## `cursor: pointer` discipline

- `cursor: pointer` is reserved for *actual* interactive controls. Applying it to non-interactive elements lies to sighted users and misleads accessibility tools that probe cursor hints.
- Disabled buttons should drop `cursor: pointer`; use `cursor: not-allowed` or the default cursor.
- Anchor links without `href` are not interactive — do not give them `cursor: pointer`.

## Forms and async feedback (pointers)

Accessibility-specific requirements for labels, `aria-live`/`role="alert"`, keyboard traversal in long forms, and error summaries are covered in this reference.

## Checklist

- Body text contrast `≥ 4.5:1`; large text `≥ 3:1`; non-text UI `≥ 3:1`. Verified in both themes.
- Every interactive element shows a visible focus indicator (`:focus-visible`, `2`–`4` px, `3:1` contrast).
- `outline: 0` is only used alongside a visible replacement ring.
- Hit area meets `40×40` web (`44×44` pt iOS / `48×48` dp Android).
- `prefers-reduced-motion: reduce` is honored per tier (disable / simplify / shorten / keep).
- Large motion (≥ 1/3 screen translation, rotation, `scale ≥ 0.5`, scroll-linked transforms) is at minimum simplified.
- Every interactive element is reachable by keyboard in source order; no `tabindex > 0` without a documented reason.
- No keyboard traps; dialog/menu focus management preserves return focus.
- Color is never the sole channel for error/success/warning/info or chart series.
- Native elements used where available; ARIA only when no native equivalent exists.
- Icon-only controls carry `aria-label` or visually hidden text.
- `aria-hidden="true"` is never applied to focusable content.
- Hidden strategy (`display: none` vs `visibility: hidden` vs `.visually-hidden` vs `aria-hidden`) is chosen deliberately.
- `cursor: pointer` is reserved for real interactive controls.

## Related references

- [animations.md](animations.md) — implementation patterns for `prefers-reduced-motion`, `:focus-visible` interaction with motion, and interruption behavior.
- [visual-details.md](visual-details.md) — hit area implementation snippet cross-link, focus-ring polish details.
- [typography.md](typography.md) — readable type sizes, fluid type rem floors so user zoom is preserved.

