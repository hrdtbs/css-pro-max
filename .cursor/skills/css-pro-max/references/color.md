# Color System

This reference defines practical color rules for hierarchy, palette construction, and theming. The goal is to produce readable, consistent interfaces without relying on ad-hoc color choices.

## When to use this reference

- Building or revising product color palettes.
- Defining text/surface hierarchy with color and weight.
- Converting one-off hex values into a repeatable color system.
- Implementing dark mode color strategy.
- Reviewing whether color alone is carrying meaning.

## Loading boundaries

- **Load this reference first** when the issue is palette quality, hierarchy clarity, or inconsistent color usage.
- **Do not load this reference first** when the issue is contrast policy details (open [accessibility.md](accessibility.md)) or shadow composition (open [visual-details.md](visual-details.md)).

## Core policy

- Color choices must be systematized before component-level styling.
- Hierarchy should use color and weight together, not font size alone.
- Color must not be the sole communication channel.

## Color spaces

Preferred spaces:

- Use `oklch()` for modern, perceptually stable systems.
- Use `hsl()` where OKLCH is unavailable in your pipeline.
- Avoid managing large systems with mixed arbitrary hex values.

Rules:

- Keep the same hue family across related states.
- Adjust chroma/saturation intentionally when changing lightness.
- Use alpha as a separate decision; do not hide hierarchy inside low-contrast base hues.

## Palette structure

Build each primary group with a full shade scale.

- Recommended: 8-10 shades per major group.
- Minimum groups: `surface`, `text`, `brand`, `accent`, semantic states (`success`, `warning`, `danger`).
- Keep neutrals as a real scale, not one gray plus opacity variants.

Example:

```css
:root {
  --color-text-strong: oklch(22% 0.01 260);
  --color-text-default: oklch(32% 0.01 260);
  --color-text-muted: oklch(46% 0.01 260);
}
```

## Hierarchy by color + weight

Use a three-tier text hierarchy by default:

- Primary: dark/high-contrast text.
- Secondary: medium-contrast text.
- Tertiary: lighter support text.

Pair with weight tiers:

- Normal content: `400`-`500`.
- Emphasized content: `600`-`700`.

Do not rely on shrinking font size to express every hierarchy level.

## Colored backgrounds

On colored surfaces:

- Avoid neutral gray text tokens copied from white-background contexts.
- Prefer text color derived from the same hue family as the background, with adjusted lightness/chroma for readability.
- Validate contrast in both default and hover/focus/disabled states.

## Semantics and states

Semantic colors should preserve hierarchy and accessibility.

- Success/warning/error colors are accents, not full typography systems.
- Disabled states should combine color, opacity, and semantics (`disabled`, `aria-disabled`) rather than color alone.
- Charts and statuses need redundant channels (label, icon, pattern, position).

## Dark mode strategy

Dark mode is not a simple inversion.

- Rebuild surface and text ladders for dark backgrounds.
- Reduce excessive chroma in bright accents to avoid glow artifacts.
- Re-tune shadows and borders for dark context (see [visual-details.md](visual-details.md)).

Pattern:

```css
:root {
  --color-surface-1: oklch(99% 0.005 260);
  --color-text-default: oklch(28% 0.01 260);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-surface-1: oklch(20% 0.01 260);
    --color-text-default: oklch(92% 0.01 260);
  }
}
```

## Tokenization

- Define color values as tokens in [tokens.md](tokens.md).
- Components consume semantic color tokens (`--color-text-muted`) rather than hardcoded color literals.
- Keep one token contract across themes; switch values per theme.

## Anti-patterns

- **NEVER** build hierarchy with color-only micro differences that are visually indistinguishable, **because** meaning collapses under real contrast conditions.
- **NEVER** reuse gray-on-white text tokens on saturated backgrounds, **because** readability degrades quickly.
- **NEVER** treat dark mode as inverted light mode, **because** perceptual contrast and saturation behavior differ.
- **NEVER** use color as the only state indicator, **because** non-visual and low-vision users lose information.

## Checklist

- [ ] Major color groups have shade scales, not single ad-hoc values.
- [ ] Text hierarchy is defined by color plus weight.
- [ ] Colored backgrounds use context-appropriate foreground colors.
- [ ] Semantic state colors are not the only information channel.
- [ ] Dark mode has dedicated surface/text ladders.
- [ ] Component styles consume color tokens rather than raw literals.

## Related references

- [accessibility.md](accessibility.md) — contrast thresholds and non-color communication requirements.
- [tokens.md](tokens.md) — token naming and distribution rules.
- [visual-details.md](visual-details.md) — depth, border, and shadow interplay with color.
