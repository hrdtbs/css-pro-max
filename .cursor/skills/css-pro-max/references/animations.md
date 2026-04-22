# Animations

This reference is the canonical source for motion strategy, easing and duration choices, interaction-specific guidance (hover, active, focus, tooltip, popover, accordion, dialog, scroll-linked, View Transitions), performance cost classes, interruption and cancellation behavior, and the implementation of `prefers-reduced-motion`. Policy for when reduced-motion must be honored lives in [accessibility.md](accessibility.md); `@keyframes` naming, placement, and composable patterns live in [keyframes.md](keyframes.md).

## When to use this reference

- Deciding whether a motion is needed at all.
- Choosing property, easing, duration, or `transform-origin` for a motion.
- Improving the feel of hover, popover, tooltip, dropdown, dialog, tab, button, toast, accordion, scroll-linked animation, or View Transitions.
- Picking an enter/exit technique: `@starting-style`, `transition-behavior`, `interpolate-size`.
- Reviewing motion performance (layout vs paint vs composite, `will-change`, `contain`).
- Handling interruption and cancellation (rapid hover reversal, dialog re-trigger).
- Implementing `prefers-reduced-motion` branches in CSS.

## Loading boundaries

- **Load this reference first** when the problem is perceived interaction speed, easing/duration choice, interruption behavior, or reduced-motion implementation.
- **Do not load this reference first** when the issue is layout breakpoints/container logic (open [responsive.md](responsive.md)) or pure text readability/line-breaking quality (open [typography.md](typography.md)).

## Ten foundational principles

1. Animation is a means, not an end.
2. Always classify each animation as functional or decorative.
3. The best animation is sometimes no animation.
4. UI motion should feel fast and responsive. What users want is the perception of "it reacted immediately".
5. Avoid decorative animation on high-frequency UI.
6. Easing is the single most important variable in animation. The same duration feels completely different under different easing curves.
7. Visual changes should convey causality with their trigger.
8. When multiple visual changes must be synchronised, separate `transition` rules may not be enough. Use `@keyframes`, the Web Animations API, or `transition` combined with `transition-behavior` as appropriate.
9. Animation has a real performance cost.
10. For accessibility, always consider what users who honour `prefers-reduced-motion` will see.

## Mandatory evaluation order

### Step 1 — is the animation needed?

Ask:

- What problem does this motion solve?
- Does it reveal a state change, a causal relationship, or feedback?
- Is it functional or decorative?
- How often will users see it?
- Does it block or distract during keyboard use and rapid interaction?

#### Decision matrix


| Purpose                                       | Judgement                            | Examples                                    |
| --------------------------------------------- | ------------------------------------ | ------------------------------------------- |
| Reveal the cause/effect of a state transition | Needed                               | Accordion open/close, tab switch            |
| Direct attention to newly appearing content   | Needed                               | Toast notifications, validation errors      |
| Give feedback for an action                   | Needed                               | Button `:active`, checkbox tick             |
| Preserve spatial continuity                   | Conditional                          | View Transitions on page change, drill-down |
| Brand expression                              | Allowed on low-frequency UI only     | Landing hero, first-time onboarding         |
| Pure visual flair                             | Not appropriate on high-frequency UI | Dashboard cards sliding in                  |


If there is no strong reason, recommend removing the animation.

### Step 2 — what is the right implementation shape?

> When the motion needs `@keyframes` instead of `transition`, open [keyframes.md](keyframes.md) — naming, scope, and composable patterns live there.

#### Step 2A — easing and timing

**Easing**

- `ease-in`-like and `linear` curves feel mechanical. Use `linear` only for continuous motion (marquees, progress bars).
- Enter and exit animations use `ease-out`-family curves.
- Elements already on screen that move use `ease-in-out`-family curves.
- CSS keyword easings (`ease`, `ease-in-out`, etc.) are too weak. Prefer project tokens; when none exist, default to quint- or expo-family curves:

```css
/* ease-out family — use for enter/exit */
--ease--out-quint: cubic-bezier(0.22, 1, 0.36, 1);
--ease--out-expo: cubic-bezier(0.16, 1, 0.3, 1);

/* ease-in-out family — use for on-screen movement */
--ease--in-out-quint: cubic-bezier(0.86, 0, 0.07, 1);
--ease--in-out-expo: cubic-bezier(0.87, 0, 0.13, 1);
```

- Applying one `transition-duration` and one `transition-timing-function` to every property is lazy. Pick a curve per property.

**Timing**

- Keep functional animations at `300ms` or shorter.
- Large surfaces (dialog, drawer, sheet) may run `300ms`–`500ms`.
- On UIs that users touch dozens of times per day, even 100 ms adds perceptible friction.

#### Step 2B — `transform-origin` and spatial coherence

- Always set `transform-origin` with respect to the trigger's position.
- Popovers should scale from the trigger. The default `center` is usually wrong.
  - When using CSS Anchor Positioning, switch `transform-origin` based on the popover's placement direction.
- A pure `scale: 0` origin feels unnatural. Pick an origin that makes the element "rise from near where it sits":


| Element               | Scale-in start |
| --------------------- | -------------- |
| tooltip, popover      | `0.95`–`0.98`  |
| dropdown menu         | `0.92`–`0.96`  |
| dialog, drawer, sheet | `0.85`–`0.92`  |


#### Step 2C — interaction-specific guidance

**Hover**

- Use `150ms`–`200ms` for hover transitions.
- Hover does not exist on touch devices; gate hover styles with `@media (any-hover: hover)` as appropriate.
  - Anchor links without `href` (e.g., a current page indicator) should not trigger hover. Scope with `:any-link:hover`.
  - Disabled buttons should not hover. Scope with `:enabled:hover`.

**Active — press feedback**

- On press, scale buttons to `0.96`–`0.98` briefly to communicate physical feedback.
- Duration is `100ms`–`150ms`.
- Apply only where "the press registered" truly matters.

**Focus / keyboard**

- Animating movement or highlight during keyboard use makes input and display feel desynchronised, which reads as sluggish.
- Motion on keyboard focus is banned. Scope transitions and animations inside `:not(:focus-visible)` so keyboard focus never triggers them.

**Tooltip**

- Delay the first appearance by `300ms`–`500ms` to avoid accidental triggering.
- During a warm-up window (`0ms`–`50ms` between hovers), show immediately.
- After dismissal, hold the immediate-show window for a cool-down of `300ms`–`500ms`; a fresh hover within the cool-down still shows instantly.

**Enter / exit with `display` changes**

- For animating from `display: none` into a visible state, define the initial styles inside `@starting-style` and opt into animating `display` or `overlay` with `transition-behavior: allow-discrete`.
- Prefer this technique for `[popover]` and `<dialog>` animations.
- `@starting-style` does not add specificity.
- `transition` on `display: none` does not work in Firefox, and `display` inside `@keyframes` does not work in Safari; treat the former as progressive enhancement.

**Height animations (accordion, etc.)**

- Animating to `height: auto` becomes straightforward with `interpolate-size: allow-keywords`.
- When Safari and Firefox support is required, fall back to the CSS grid pattern with `grid-template-rows: 0fr / 1fr`.
- Such animations cause layout; mind the performance cost. Accordions are an acceptable case.

**Scroll-linked animation**

- Implementation priority:
  1. CSS scroll-driven animations (`animation-timeline`, `view-timeline`, …).
  2. `IntersectionObserver` toggling state, combined with CSS transition/animation.
  3. Frame-by-frame JavaScript only when truly needed.
- Always flag implementations that read `scrollTop` on every frame.
- Decision criteria:
  - Continuous value changes tied to scroll position → CSS scroll-driven animations.
  - One-shot "element enters/exits viewport" state change → `IntersectionObserver`.
  - Complex scroll-based branching logic → JavaScript, but gated by `requestAnimationFrame`.
- For `IntersectionObserver` toggling, use the `animation-fill-mode: both` + `animation-play-state: paused` initial-hidden pattern. The element's hidden state is expressed inside the keyframes, and the reveal flips `animation-play-state` to `running`. Full code and rationale live in [keyframes.md](keyframes.md) under "Scroll-linked pattern".
- Under `@media (prefers-reduced-motion: reduce)`, disable the `animation-play-state` toggle entirely or reduce the animation to a fade. Policy for when reduced motion must be honored is in [accessibility.md](accessibility.md).

**View Transitions**

- Separate the snapshot visual animation from the actual layout change.
- In SPA contexts, use `document.startViewTransition()`. In MPA contexts, use the `@view-transition` at-rule.
- `view-transition-name` values follow the CSS custom-property naming convention.

### Step 3 — are performance costs acceptable?

#### Basic rendering cost

Think in these axes:

- Does it cause layout, paint, or compositing?
- Does it involve the main thread or the compositor thread?

#### Property selection


| Priority  | Technique                                                                                                                                               | Note                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| High      | compositor-handled `transform`, `opacity`, some `filter`, some `clip-path`, CSS scroll-driven animations                                                | GPU-only composition                                          |
| Medium    | JS-driven updates to `transform`/`opacity`, FLIP patterns                                                                                               | Main thread involved but layout/paint minimal                 |
| Low       | Paint-triggering properties (`background-color`, `box-shadow`, …)                                                                                       | Cost scales with area; acceptable on hover                    |
| Avoid     | Layout-triggering properties (`width`, `height`, `padding`, `inset`, …)                                                                                 | Except for cases like accordions where they cannot be avoided |
| High risk | Large-radius `blur()` / `backdrop-filter`, huge composited layers, per-frame global custom-property writes, `scrollTop`-polling scroll-linked animation |                                                               |


#### `filter` / `backdrop-filter`

- `filter` may be hardware-accelerated, but the cost is not free.
- `backdrop-filter` is more expensive than `filter` because it repaints the full area behind the element.
- Avoid combinations that backfire:
  - Large blur radii.
  - Large surface areas (especially for `backdrop-filter`).
  - Layers animating while the effect is active.
  - Multiple stacked effects.

#### Custom-property updates

- Do not update globally-applied custom properties on every frame.
- Keep per-frame updates local.
- Turn inheritance off with `@property { inherits: false }` to stop chain reactions.
- Do not inherit values that the whole DOM does not need.

#### `will-change`

- `will-change` should be added just before an animation and removed after.
- Leaving it on permanently wastes GPU memory and creates unnecessary composite layers.
- Default posture: do not use `will-change`. If you must, JS-toggle it on and off around the animation.

#### `contain`

- Use `contain: content` to limit layout, paint, and style-computation scope. Apply it deliberately:
  - `position: fixed` inside a contained ancestor behaves like `position: absolute` (outside the top layer).
  - Overflow gets clipped.
  - A stacking context is created.

#### `transition-property: all` is banned

- It transitions unrelated properties, producing unwanted motion and unnecessary cost.
- Enumerate the exact properties you want to animate.
- **Never use it because** accidental property animations increase jank risk and make regressions hard to isolate.

#### Independent transform properties

- Prefer `translate`, `rotate`, `scale` over `transform` for clearer diffs and readability.
- Use `transform` when:
  - The independent-property order (`translate` → `rotate` → `scale`) is wrong for your case.
  - You need `skew()`.
  - A 3D composite reads better as one `transform`.

### Step 4 — animation interruption and cancellation

Consider what happens if the user acts again before the animation ends.


| Situation                           | Desired behaviour                        | Implementation                                                                                       |
| ----------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Hover → unhover rapidly             | Reverse from the current frame           | CSS `transition`                                                                                     |
| Dialog open → dialog closed rapidly | Exit animation starts from current state | Automatic with `@starting-style` + `transition`; `@keyframes` requires `animation-fill-mode` plus JS |
| Rapid tab clicks                    | Switch instantly, skip animation         | `animation: none` reset, or View Transitions' `skipTransition()`                                     |
| Sudden scroll reversal              | Follow the new direction immediately     | CSS scroll-driven animations handle this automatically                                               |


Rules:

- `transition` automatically reverses mid-animation; prefer it for UIs where interruption is common.
- `@keyframes` is harder to cancel. For interruption-heavy UIs, avoid it or use the Web Animations API (`cancel()`, `reverse()`).
- On rapidly retriggered UIs (tabs, segmented controls), shorten animations (`100ms`–`150ms`) or provide a skip mechanism.

### Step 5 — are you honouring `prefers-reduced-motion`?

Policy — *when* reduced motion must be honored and the tier definitions — lives in [accessibility.md](accessibility.md). This section covers the CSS implementation patterns for each tier.

#### Implementation patterns by tier


| Tier     | CSS pattern                                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------ |
| Disable  | Wrap the animation in `@media (prefers-reduced-motion: no-preference) { … }` so the default has no motion          |
| Simplify | Keep an `opacity` transition unconditionally; move `transform`/`scale`/`translate` into the `no-preference` branch |
| Shorten  | Override `animation-duration` / `transition-duration` to `≤ 50ms` inside `@media (prefers-reduced-motion: reduce)` |
| Keep     | No change — the motion is already within the acceptable envelope (spinners, progress bars, focus ring)             |


Example — disable:

```css
@media (prefers-reduced-motion: no-preference) {
  .parallax {
    animation: --translate-from 1s linear;
  }
}
```

Example — simplify:

```css
.sheet {
  transition: opacity 200ms var(--ease--out-quint);

  @media (prefers-reduced-motion: no-preference) {
    transition-property: opacity, translate;
  }
}
```

Example — shorten:

```css
.tooltip {
  animation: --fade-in 150ms var(--ease--out-quint);

  @media (prefers-reduced-motion: reduce) {
    animation-duration: 50ms;
  }
}
```

For the definition of "large motion" (translation affecting ≥ 1/3 of the screen, rotation, `scale ≥ 0.5`, scroll-tracking transforms, visible shake) and the decision of which tier applies, see [accessibility.md](accessibility.md).

## Checklist

Run through this after every other step in the evaluation order:

- Duration is not too long (functional ≤ `300` ms; large surfaces ≤ `500` ms).
- Easing is not weak (no lingering default CSS keywords).
- `transform-origin` aligns with the trigger.
- No physically absurd motion (no `scale: 0`, etc.).
- No motion on keyboard focus.
- Multiple visual changes are synchronised.
- First interaction delays and subsequent immediate shows are correct (tooltip warm-up / cool-down).
- Interruption and cancellation behaviour are accounted for.
- Performance: minimal layout/paint, no `transition-property: all`, `will-change` managed.
- `prefers-reduced-motion` response is appropriate (see [accessibility.md](accessibility.md) for tier policy).
- Scroll-linked animations use `animation-fill-mode: both` + `animation-play-state: paused` (see [keyframes.md](keyframes.md)).
- `@keyframes` names are dashed idents with correct scope and placement (see [keyframes.md](keyframes.md)).

## Fallback mini-playbook

When motion feedback gets inconsistent or too heavy, recover in this order:

1. Remove decorative enters/exits first and keep only functional feedback motion.
2. Normalize duration/easing (`<= 300ms` common UI, strong ease-out or ease-in-out tokens).
3. Reduce to opacity-first transitions and verify reduced-motion branches before reintroducing transform/blur effects.

## Response formats

### Proposing a new animation

1. **Verdict**: needed / not needed (cite the matrix).
2. **Classification**: functional or decorative.
3. **Motion**: easing / duration / property / transform-origin.
4. **Implementation**: CSS only (`transition`, `@keyframes`, or `@starting-style`) / CSS + JS / Web Animations API / FLIP.
5. **Keyframes design** (if applicable): name (dashed ident) / scope (global vs component-local) / API-style custom properties.
6. **Interruption behaviour**: reverse / skip / not required.
7. **Reduced-motion response**: disable / simplify / shorten / keep.
8. **Risks**: accessibility, repeat-friction, visual inconsistency, performance.

### Suggesting a fix to existing code

1. **Verdict**: keep / edit / remove.
2. **Reason**: UX purpose and usage frequency.
3. **Change**: specific locations and code examples.
4. **Risks**: side effects of the edit.

### Performance review

1. **Classification**: layout / paint / composite.
2. **Risk**: low / medium / high.
3. **Reason**: invalidation path and thread involvement.
4. **Safer alternatives**: `transform`, `clip-path`, observers, local variables, `@property`, etc.
5. **Browser notes**: Chrome-specific optimisations, Safari/Firefox differences.

## Related references

- [keyframes.md](keyframes.md) — `@keyframes` naming, global vs component-local placement, composable patterns, `paused + both` scroll-linked pattern.
- [accessibility.md](accessibility.md) — `prefers-reduced-motion` policy (when to honor, tier definitions, large-motion criteria).
- [visual-details.md](visual-details.md) — staggered enters, subtle exits, icon cross-fade, first-paint suppression.
- [typography.md](typography.md) — motion interaction with typographic features (e.g., `text-box-trim` during enter).

