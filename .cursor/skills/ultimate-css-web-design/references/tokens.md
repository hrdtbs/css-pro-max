# Design Tokens

This reference defines naming, layering, and usage rules for design tokens implemented as CSS custom properties. The objective is consistent API-like token surfaces across layout, type, motion, color, depth, and state.

## When to use this reference

- Defining or reviewing token naming conventions.
- Adding a new token family (`--color-*`, `--size-*`, `--shadow-*`, `--ease-*`).
- Migrating raw CSS literals into tokenized values.
- Designing token layers for themes and modes.
- Reviewing token compatibility with component APIs.

## Loading boundaries

- **Load this reference first** when the issue is token naming, token scale design, or token usage contracts.
- **Do not load this reference first** when the issue is keyframe choreography (open [keyframes.md](keyframes.md)) or typographic readability (open [typography.md](typography.md)).

## Core policy

- Tokens represent decisions, not implementation accidents.
- Token names must communicate responsibility and scale.
- Token consumers should not infer hidden side effects.
- Families must be internally regular.

## Naming grammar

Base pattern:

```text
--{family}-{role}-{step}
```

Examples:

- `--color-surface-1`
- `--color-text-muted`
- `--size-fluid-3`
- `--shadow-2`
- `--ease-out-3`
- `--duration-quick-2`

Rules:

- Use lowercase kebab-case.
- Keep family names short and stable.
- Prefer semantic role before ordinal index where meaning exists.
- Avoid names tied to one component (`--button-blue`) unless scoped locally.

## Recommended families

### Color

- `--color-{group}-{step}`
- Groups: `surface`, `text`, `brand`, `accent`, `success`, `warning`, `danger`.
- Keep at least 8-10 shades for major color groups.

### Size and space

- `--size-{000..15}` for fixed scale.
- `--size-fluid-{1..10}` for fluid scale.
- `--space-{1..10}` for rhythm spacing when separated from general size.

### Radius and border

- `--radius-{1..6}`
- `--radius-round`
- `--border-width-{1..3}`

### Shadows and depth

- `--shadow-{1..6}`
- `--inner-shadow-{1..4}`

### Motion

- Easing: `--ease-{in,out,in-out}-{1..5}`
- Elastic/spring variants: `--ease-elastic-*`, `--ease-spring-*`
- Duration: `--duration-instant`, `--duration-quick-1`, `--duration-quick-2`, `--duration-standard`, `--duration-slow`
- Animation aliases: `--animation-{fade,slide,scale}-{in,out}`

### Z-axis

- `--z-base`, `--z-header`, `--z-modal`, `--z-toast`, `--z-loading`

Z-axis rules are defined in [z-index.md](z-index.md).

## Token layers and ownership

- Global tokens live in a tokens layer.
- Component tokens are namespaced and local.
- Theme tokens override values, not token identities.

Pattern:

```css
@layer tokens {
  :root {
    --color-surface-1: oklch(99% 0.005 260);
    --shadow-2:
      0 1px 2px rgb(0 0 0 / 0.05),
      0 4px 8px rgb(0 0 0 / 0.08);
  }
}
```

```css
.card {
  --card-padding: var(--size-fluid-3);
  padding: var(--card-padding);
}
```

Rules:

- Global family tokens should not include component names.
- Component-local aliases should map to global tokens rather than hardcoded literals.
- Keep alias chains short (`alias -> global`), avoid deep indirection.

## Token usage contract

- Components consume tokens, they do not redefine system scales.
- Utilities may expose token usage helpers but must not create parallel scale systems.
- Raw literals are acceptable only for one-off corrective values with documented reason.

## Migration strategy

When replacing literals:

1. Group repeating literals by semantic role.
2. Create or reuse token names.
3. Replace literals in components.
4. Verify visual parity.
5. Remove dead literals and duplicate aliases.

Do not tokenise random unique values that appear once without reuse intent.

## Anti-patterns

- **NEVER** encode implementation details in token names, **because** APIs become unstable (`--padding-left-nav-mobile`).
- **NEVER** mix semantic and ordinal systems in one family without a rule, **because** consumers cannot predict usage.
- **NEVER** create component-specific global tokens by default, **because** global namespace pollution grows quickly.
- **NEVER** keep long alias chains, **because** debugging and refactoring slow down.

## Checklist

- [ ] Naming follows one grammar and is kebab-case.
- [ ] Families are explicit and non-overlapping.
- [ ] Token scales are regular (no random numeric jumps without reason).
- [ ] Component aliases map to global tokens, not raw literals.
- [ ] Theme overrides change values, not token contracts.
- [ ] Z-index tokens align with [z-index.md](z-index.md).

## Related references

- [keyframes.md](keyframes.md) — animation naming and API-style custom-property integration.
- [animations.md](animations.md) — duration/easing policies consumed by motion tokens.
- [color.md](color.md) — palette strategy for color token design.
