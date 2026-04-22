# Foundation CSS

This reference defines baseline architecture for reset, cascade layers, and default element behavior. The goal is a stable base that is easy to override, resilient under growth, and safe for accessibility.

## When to use this reference

- Designing a project-wide reset policy.
- Structuring cascade layers for predictable precedence.
- Integrating third-party CSS without specificity wars.
- Auditing base styles that accidentally remove useful UA behavior.
- Setting multilingual defaults before component work starts.

## Loading boundaries

- **Load this reference first** when the issue is global CSS precedence, reset behavior, or base-style conflicts across the app.
- **Do not load this reference first** when the issue is component breakpoints (open [responsive.md](responsive.md)) or component naming (open [terminology.md](terminology.md)).

## Core policy

- Keep reset minimal and intentional.
- Preserve useful browser defaults unless there is a strong reason to override.
- Keep specificity low so app-level customization is easy.
- Make layer order explicit.

## Layer architecture

Declare layers in one ordered line:

```css
@layer reset, tokens, base, components, utilities, overrides;
```

Responsibilities:

- `reset`: browser-normalization and baseline safety rules.
- `tokens`: design tokens only (`--color-*`, `--space-*`, `--z-*`, etc.).
- `base`: element-level defaults (`body`, headings, links, forms, lists).
- `components`: component-specific declarations.
- `utilities`: one-purpose helper classes.
- `overrides`: exceptional local overrides.

Rules:

- Do not skip layer declaration order.
- Keep tokens free of structural selectors.
- Keep `overrides` small; large override usage signals architecture drift.

## Low-specificity baseline with `:where()`

Base selectors should prefer `:where()` to keep specificity at zero.

```css
@layer reset {
  :where(*) {
    box-sizing: border-box;
  }

  :where(img, svg, video) {
    display: block;
    max-inline-size: 100%;
  }
}
```

Benefits:

- Component and utility rules can override without selector inflation.
- Teams avoid `!important` escalation.
- Maintenance remains predictable as files grow.

## Reset scope: what to reset and what to keep

Reset only friction points. Keep defaults that provide semantic value.

Reset candidates:

- Inconsistent box sizing.
- Form-control inheritance mismatches.
- Media max size constraints.
- Margins that cause unstable base rhythm.

Keep by default:

- Heading emphasis (`font-weight`) unless typography policy explicitly redefines it.
- Native button semantics and disabled behavior.
- Table semantics and border behavior unless table design requires a full custom system.

## Accessibility-safe base rules

Global base must not erase essential accessibility affordances.

- Keep focus visibility by default.
- Support forced-color mode.
- Preserve list semantics.
- Preserve control semantics for form and interactive elements.

Example:

```css
@layer base {
  :where(:focus-visible) {
    outline: 2px solid currentColor;
    outline-offset: 2px;
  }

  @media (forced-colors: active) {
    :where(:focus-visible) {
      outline-color: Highlight;
    }
  }
}
```

## Third-party CSS strategy

Third-party packages should not control app precedence.

- Import vendor CSS into a lower-priority layer when possible.
- Keep app components/utilities above vendor defaults.
- Avoid fixing vendor conflicts by increasing selector complexity in random files.

Pattern:

```css
@layer reset, tokens, base, vendor, components, utilities, overrides;
```

If `vendor` is used, keep it between `base` and `components`.

## Language-aware foundation defaults

Foundation may include language-aware defaults when they are low risk and broadly useful.

- Keep language-specific typography rules in [typography.md](typography.md).
- Use foundation only for defaults that should be present everywhere.
- Avoid embedding heavy per-language visual tuning in reset layer.

## Anti-patterns

- **NEVER** reset everything blindly, **because** it removes useful semantics and increases reimplementation cost.
- **NEVER** rely on unlayered global CSS in large systems, **because** precedence becomes implicit and fragile.
- **NEVER** solve precedence conflicts with selector chains, **because** specificity debt compounds.
- **NEVER** hide focus outlines globally, **because** keyboard accessibility breaks immediately.

## Checklist

- Layer order is declared once and consistently used.
- Reset scope is intentional; useful UA defaults are preserved.
- Base selectors use low specificity (`:where()` where appropriate).
- Tokens are isolated from structure/layout declarations.
- Focus visibility and forced-color support are preserved.
- Third-party CSS precedence is controlled by layer, not selector inflation.

## Related references

- [typography.md](typography.md) — detailed language and readability tuning.
- [z-index.md](z-index.md) — layering on the z-axis for overlays and fixed surfaces.
- [accessibility.md](accessibility.md) — interaction-level accessibility requirements.

