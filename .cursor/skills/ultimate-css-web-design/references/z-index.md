# Z-Index

This reference defines deterministic layering rules so stacking order stays predictable as products grow. Treat `z-index` as a constrained system, not an arbitrary numeric field.

## When to use this reference

- Designing layering for fixed/sticky UI (header, drawer, modal, toast, loading overlay).
- Resolving conflicts between component-local overlays and page-level overlays.
- Deciding whether a layer should be absolute (global) or relative (inside a component root).
- Introducing lint or token rules to prevent magic-number `z-index`.
- Reviewing whether `<dialog>` or top-layer primitives can replace custom layering.

## Loading boundaries

- **Load this reference first** when overlap bugs involve headers, modals, drawers, sticky bars, popovers, or third-party CSS collisions.
- **Do not load this reference first** when the issue is layout breakpoints (open [responsive.md](responsive.md)) or naming semantics (open [terminology.md](terminology.md)).

## Core model

`z-index` has two separate responsibilities. Keep them separate:

- **Absolute layering**: app-wide order across independent systems.
- **Relative layering**: local order inside one component root.

Do not mix these into one numeric scale.

## Absolute layering (global stack)

Absolute layering controls page-level and viewport-anchored surfaces:

- Sticky/fixed header.
- Side drawer.
- Modal shell.
- Global notification/toast layer.
- Global loading overlay.

Manage absolute values in one place (for example, `settings/stack.css`) and expose them as custom properties.

```css
:root {
  --z-base: 0;
  --z-header: 10;
  --z-drawer: 20;
  --z-modal: 30;
  --z-toast: 40;
  --z-loading: 50;
}
```

Rules:

- Use step values (`10`, `20`, `30`...) to keep insertion space.
- Never hardcode absolute numbers in components.
- Reserve one strongest layer for emergency front placement:

```css
.global-loading {
  z-index: calc(infinity);
}
```

Use `calc(infinity)` only for exceptional global blockers.

## Relative layering (component-local)

Relative layering exists only inside one component root.

Use only:

- `z-index: 0` for baseline content.
- `z-index: 1` for foreground content.

Example:

```css
.card {
  position: relative;
}

.card__image {
  position: relative;
  z-index: 0;
}

.card__badge {
  position: absolute;
  inset-block-start: 0.5rem;
  inset-inline-end: 0.5rem;
  z-index: 1;
}
```

Rules:

- Relative values never compete with global stack values.
- Do not assign global tokens to internal component parts.
- Prefer creating a local stacking context on the root over inflating child numbers.

## Stacking-context prerequisites

`z-index` only works as expected when stacking context and positioning rules are understood.

- `z-index` does nothing on `position: static` boxes.
- Positioned elements (`relative`, `absolute`, `fixed`, `sticky`) can participate in stacking.
- New stacking contexts isolate descendants from outside comparisons.

Common triggers:

- `position` + non-auto `z-index`.
- `opacity < 1`.
- `transform`, `filter`, `mix-blend-mode`.
- `isolation: isolate`.

If two elements do not share a comparable context, raising numbers will not fix overlap.

## Top layer and native primitives

When available, prefer top-layer primitives over custom `z-index` escalation.

- `<dialog>` with `showModal()` is rendered in top layer.
- Top-layer surfaces do not require project `z-index` values.

Do not assign arbitrary large values to compete with top layer.

## Lint and governance

Enforce policy in lint rules:

- Ban raw numeric `z-index` in component files.
- Allow only `0` and `1` for local layering.
- Require custom-property usage for global layering.

Recommended review rule:

- If a PR adds `z-index: 9999`, reject and map intent to the stack system.

## Anti-patterns

- **NEVER** scatter absolute `z-index` numbers across components, **because** the order becomes untraceable.
- **NEVER** use `z-index` to patch unrelated layout bugs, **because** you hide the real structural problem.
- **NEVER** keep adding larger integers (`100`, `1000`, `10000`), **because** each fix increases future collision risk.
- **NEVER** treat component-local layering and app-wide layering as one scale, **because** they have different responsibilities.

## Checklist

- [ ] Absolute and relative layering are explicitly separated.
- [ ] Absolute layers are managed in one global token file.
- [ ] Relative layers inside components use only `0` and `1` unless a justified exception is documented.
- [ ] No raw large `z-index` values are introduced in component styles.
- [ ] Stacking context was verified before changing numeric values.
- [ ] Native top-layer primitives are used where applicable.

## Related references

- [terminology.md](terminology.md) — naming boundaries for structure and responsibility.
- [responsive.md](responsive.md) — viewport/container responsibilities that interact with fixed overlays.
- [accessibility.md](accessibility.md) — modal/dialog behavior requirements beyond layering.
