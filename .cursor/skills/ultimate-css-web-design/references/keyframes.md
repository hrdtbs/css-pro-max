# `@keyframes` Naming and Design Patterns

This reference is the canonical source for `@keyframes` naming, placement (global vs component-local), API-style custom-property design, composable patterns (`--fade-in`, `--scale-from`, `--translate-from`, `--fade-out`), the `paused + both` scroll-linked pattern, and the decision between `@keyframes`, `transition`, and the Web Animations API. Motion strategy at large (easing, duration, interaction-specific guidance, performance, interruption, `prefers-reduced-motion` implementation) lives in [animations.md](animations.md).

## When to use this reference

- Naming a new `@keyframes` rule.
- Deciding whether a keyframes belongs in `base/keyframes.css` (global) or with its component (local).
- Building a composable keyframes with API-style custom properties so callers can inject the starting point.
- Animating from `display: none` or the `[popover]` / `<dialog>` top layer.
- Setting up an `IntersectionObserver` reveal that uses `animation-fill-mode: both` + `animation-play-state: paused` as the single source of truth for the hidden state.
- Choosing between `@keyframes`, `transition` + `@starting-style`, and the Web Animations API.

## 1. Naming basics

### Dashed idents are mandatory

Every `@keyframes` name must start with `--`.

```css
/* OK */
@keyframes --fade-in { /* keyframes content */ }
@keyframes --slide-up { /* keyframes content */ }

/* Not OK — not a dashed ident */
@keyframes fadeIn { /* keyframes content */ }
@keyframes slide-up { /* keyframes content */ }
```

Reasons:

- Modern CSS pushes user-defined identifiers toward the `--` prefix (`anchor-name`, `animation-timeline`, and so on). One rule beats per-property memorisation.
- You no longer need to remember which properties require the prefix.
- Future CSS keywords are less likely to collide with your names.
- You can see at a glance that the name is yours.

### Naming by scope


| Scope           | Form                                   | Location                | Examples                                                     |
| --------------- | -------------------------------------- | ----------------------- | ------------------------------------------------------------ |
| Global          | `--{animation-name}`                   | `base/keyframes.css`    | `--fade-in`, `--scale-from`, `--translate-from`              |
| Component-local | `--{component-name}--{animation-name}` | The component's own CSS | `--shared-dialog--backdrop-fade`, `--shared-toast--slide-in` |


- Global keyframes are reserved for generic animations reused project-wide.
- Component-local keyframes live inside that component's CSS.
- When in doubt, start local. Promote to global only after the third reuse.

## 2. Global keyframes design

### Location and management

All global keyframes are consolidated in `base/keyframes.css`.

```
styles/
├── base/
│   ├── keyframes.css   ← all global keyframes here
│   └── base resets and defaults
├── components/
│   ├── shared-dialog.css   ← component-local keyframes here
│   └── component styles
└── tokens/
    └── animation.css
```

### Treat global keyframes like utility classes

Global keyframes follow the same design philosophy as utility classes. Each keyframes animates exactly one property; complex effects come from composition.

#### Principles

- One keyframes = one property change (`--fade-in` touches `opacity` only; `--scale-from` touches `scale` only).
- When multiple properties must animate together, compose keyframes with comma-separated `animation-name`.
- Each keyframes stands on its own and is meaningful when used alone.
- Composing lets you pick per-property `animation-duration` / `animation-timing-function`, so each property gets the easing and timing that suit it.

#### OK — compose single-responsibility keyframes

```css
/* Caller: combine them */
.dropdown {
  --scale-from--x-value: 0.95;
  --scale-from--y-value: 0.95;

  animation-name: --fade-in, --scale-from;
  animation-duration: 200ms;
  animation-timing-function: var(--ease--out-quint), var(--ease--out-expo);
  animation-fill-mode: both;
}

.toast {
  --translate-from--y-value: 100%;

  animation-name: --fade-in, --translate-from;
  animation-duration: 200ms, 300ms;
  animation-timing-function: var(--ease--out-quint);
  animation-fill-mode: both;
}
```

#### Not OK — cramming multiple properties into one global keyframes

```css
/* Not OK — a global keyframes animates two properties */
@keyframes --fade-in-and-scale {
  from {
    opacity: 0;
    scale: 0.95;
  }
}
```

Problems:

- You cannot tune `opacity` and `scale` easing/timing independently.
- You cannot reuse the pieces when only one property is needed.
- API-style custom-property naming gets awkward (which property does each value refer to?).
- When component variations diverge slightly, the shared global loses its purpose.

### Global keyframes must reduce to `from`/`to`

Global keyframes are limited to two-frame animations. Intermediate frames (`25%`, `50%`, …) belong in component-local keyframes.

#### Why

- Keyframes with intermediate frames are tied to a specific UI pattern. A "midpoint colour flip" is not generic and belongs to the component that needs it.
- Two-frame keyframes pair naturally with API-style custom properties. Intermediate frames multiply the number of values to inject.
- The utility-class analogy only works for "A to B" motion. Anything more complex is the component's responsibility.

#### OK for global

```css
@keyframes --fade-in {
  from {
    opacity: var(--fade-in--from-value, 0);
  }
}

@keyframes --scale-from {
  from {
    scale: var(--scale-from--x-value, 1) var(--scale-from--y-value, 1);
  }
}
```

#### Not OK for global

```css
/* Move to component-local — intermediate frame */
@keyframes --pulse {
  0% { opacity: 1; }
  50% { opacity: 0.4; }
  100% { opacity: 1; }
}
```

### Omit `from`/`to` when the engine can fill them in

CSS fills in a missing `from` or `to` with the value the element currently carries. Use this: do not spell out the obvious frame.

#### Why

- Omission respects the element's live value and flows with cascade changes naturally.
- Hard-coding `from` or `to` creates jumps when the element's real value differs from the hard-coded one.
- Fewer values are needed in API-style custom properties, keeping the keyframes design simple.

#### Example — omit `to`

```css
/* OK — the animation runs toward the element's current opacity. */
@keyframes --fade-in {
  from {
    opacity: var(--fade-in--from-value, 0);
  }
}
```

On an element with `opacity: 0.8` you get `0 → 0.8`; with `opacity: 1` you get `0 → 1`.

```css
/* Not OK — hard-coded to { opacity: 1 } */
@keyframes --fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

This forces `opacity: 1` at the end. On an `opacity: 0.8` element with `animation-fill-mode: both`, you get a flash to `1` and a jump back to `0.8`; with `forwards`, the natural `0.8` is overridden.

#### Example — omit `from`

```css
/* OK — goes from the element's current opacity to 0. */
@keyframes --fade-out {
  to {
    opacity: var(--fade-out--to-value, 0);
  }
}
```

On `opacity: 0.5` you get `0.5 → 0`; on `opacity: 1` you get `1 → 0`. A hard-coded `from { opacity: 1 }` would jump a semi-transparent element up to `1` and fade it from there.

#### Decision table


| Situation                                           | `from`/`to`                                   |
| --------------------------------------------------- | --------------------------------------------- |
| Enter from "zero / invisible" (fade-in, scale-from) | Keep `from`, drop `to`                        |
| Exit to "zero / invisible" (fade-out)               | Drop `from`, keep `to`                        |
| Both start and end must be strict                   | Keep both (often a local keyframes is better) |
| Infinite loops (rotate, etc.)                       | Keep `to`                                     |


### API-style custom properties

Global keyframes must be generic. When the entry direction or magnitude needs to vary by context, bake a custom-property reference into the keyframes so callers inject values.

#### Naming convention

Keyframes-specific custom properties are `--{keyframes-name}--{value-name}`.

The `--` prefix is already in the keyframes name, so there is no need to start with `--_`.

```
--{keyframes-name}--{value-name}
e.g. --scale-from--x-value, --translate-from--y-value
```

#### Pattern — `--scale-from`

```css
/* base/keyframes.css */
@keyframes --scale-from {
  from {
    scale: var(--scale-from--x-value, 1) var(--scale-from--y-value, 1);
  }
}
```

```css
[popover] {
  --scale-from--x-value: 0.96;
  --scale-from--y-value: 0.96;

  animation-name: --scale-from;
  animation-duration: 200ms;
  animation-timing-function: var(--ease--out-quint);
  animation-fill-mode: both;
}

/* Tweak the origin per placement. */
[popover][data-placement="top"] {
  --scale-from--y-value: 1.04;
}
```

#### Pattern — `--translate-from`

```css
/* base/keyframes.css */
@keyframes --translate-from {
  from {
    translate: var(--translate-from--x-value, 0) var(--translate-from--y-value, 0);
  }
}
```

```css
.toast {
  --translate-from--y-value: 100%;

  animation-name: --translate-from;
  animation-duration: 300ms;
  animation-timing-function: var(--ease--out-quint);
  animation-fill-mode: both;
}

/* Swap direction by position. */
.toast[data-position="top"] {
  --translate-from--y-value: -100%;
}
```

#### Pattern — `--fade-in` / `--fade-out`

```css
/* base/keyframes.css */
@keyframes --fade-in {
  from {
    opacity: var(--fade-in--from-value, 0);
  }
}

@keyframes --fade-out {
  to {
    opacity: var(--fade-out--to-value, 0);
  }
}
```

#### Composite pattern — stacking keyframes

`animation` accepts comma-separated values. Compose global keyframes to cover component needs without creating a component-local keyframes.

```css
/* Fade + scale combined */
.dropdown {
  --scale-from--x-value: 0.95;
  --scale-from--y-value: 0.95;

  animation-name: --fade-in, --scale-from;
  animation-duration: 200ms;
  animation-timing-function: var(--ease--out-quint), var(--ease--out-expo);
  animation-fill-mode: both;
}
```

#### Scroll-linked pattern — `paused` + `both`

For scroll-linked animations driven by `IntersectionObserver`, combine global keyframes with `animation-play-state: paused` to unify initial-hidden state and trigger.

```css
.reveal-item {
  --translate-from--y-value: 20px;

  animation-name: --fade-in, --translate-from;
  animation-duration: 600ms;
  animation-timing-function: var(--ease--out-quint);
  animation-fill-mode: both;
  animation-play-state: paused;

  &[data-revealed] {
    animation-play-state: initial;
  }
}
```

- `animation-fill-mode: both` applies the `from` frame even while paused. The element is drawn at the keyframes' starting position (`opacity: 0`, `translate: 0 20px`).
- Flipping `animation-play-state` to `initial` (= `running`) starts the animation.
- No duplicate `opacity: 0` is required outside the keyframes. The keyframes remain the single source of truth for the initial state.

## 3. Component-local keyframes

### Naming and placement

Local keyframes live with the component that uses them and follow `--{component-name}--{animation-name}`.

```css
/* affordance/arrows.css */
@keyframes --arrows--fill-steps {
  from,
  to {
    fill: var(--color--primary);
  }

  50% {
    fill: transparent;
  }
}

@scope (.arrows) to (:scope > *) {
  :scope {
    fill: none;
    stroke: var(--color--primary);
    animation-name: --arrows--fill-steps;
    animation-duration: 200ms;
    animation-timing-function: steps(1);
    animation-direction: alternate;
    animation-iteration-count: infinite;
  }
}
```

### Global vs local — decision


| Situation                                                      | Choice                                         |
| -------------------------------------------------------------- | ---------------------------------------------- |
| Generic motion (fade, scale, translate) with a variable origin | Global keyframes + API-style custom properties |
| Component-specific motion across multiple properties           | Local keyframes                                |
| Intermediate frames (e.g., `50%`) required                     | Local keyframes                                |
| Backdrop or special pseudo-element animation                   | Local keyframes                                |


## 4. `@keyframes` vs `transition` + `@starting-style`

Criteria for choosing between `@keyframes` and `transition` + `@starting-style`.


| Requirement                                             | Recommended technique                                                    |
| ------------------------------------------------------- | ------------------------------------------------------------------------ |
| Enter from `display: none` and exit should also animate | `transition` + `@starting-style` + `transition-behavior: allow-discrete` |
| Only the enter animates; exit is instant                | `@keyframes` animation                                                   |
| Intermediate frames (`25%`, `50%`, …) required          | `@keyframes` animation                                                   |
| Dynamic JS control (pause, reverse, cancel)             | Web Animations API (`element.animate()`)                                 |
| Frequent interruption and reversal                      | `transition`                                                             |
| Multiple properties on staggered timing                 | `@keyframes` animation, or `transition-delay` composition                |
| Scroll-linked, initial-hidden, toggled activation       | `@keyframes` + `animation-play-state: paused` / `initial`                |


## Checklist

- Every `@keyframes` name starts with `--` (dashed ident).
- Global keyframes live in `base/keyframes.css`; component-local keyframes live with the component as `--{component}--{animation}`.
- Global keyframes touch one property each; multi-property motion is composed via comma-separated `animation-name`.
- Global keyframes reduce to `from`/`to` pairs; intermediate frames (`25%`, `50%`, …) are component-local.
- `from`/`to` is omitted when the absent frame is the element's live value.
- Variable starting points use API-style custom properties (`--{keyframes-name}--{value-name}`).
- `animation-fill-mode: both` is the default fill mode when spelled explicitly.
- Scroll-linked reveals use the `paused` + `both` pattern; no duplicate hidden state lives outside the keyframes.
- Choice between `@keyframes`, `transition` + `@starting-style`, and the Web Animations API matches the decision table in §4.

## Related references

- [animations.md](animations.md) — motion strategy, easing/duration tokens, interaction-specific guidance, performance, interruption, `prefers-reduced-motion` implementation.
- [accessibility.md](accessibility.md) — `prefers-reduced-motion` policy and large-motion definitions.
- [visual-details.md](visual-details.md) — staggered enter and subtle exit patterns that consume these keyframes.
- [responsive.md](responsive.md) — layout-triggering motion boundaries inside containers.

