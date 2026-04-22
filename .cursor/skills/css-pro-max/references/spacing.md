# Spacing — Rhythm, Intent, and Layout Structure

This reference is the canonical source for **whitespace rhythm**: base units, discrete scales, how spacing expresses hierarchy and density, when to prefer `gap` over `margin`, when to choose Grid vs Flex, how spacing adapts across viewport widths, and why negative margins are not a default tool. Padding, margin between siblings, gutters, and section separation all tie back to one scale and one vocabulary aligned with [terminology.md](terminology.md).

Adjacent concerns live in their own references:

- Token naming and alias contracts → [tokens.md](tokens.md).
- Edge vocabulary (`Gutter` vs `Gap`, layout primitives) → [terminology.md](terminology.md).
- Readable measure, `rem` usage for type-adjacent spacing → [typography.md](typography.md).
- Intrinsic layout, container queries, `calc()` thresholds → [responsive.md](responsive.md).
- Touch targets and hit-area expansion → [accessibility.md](accessibility.md).

## When to use this reference

- Choosing spacing values for padding, gaps, section separation, or page gutters.
- Deciding between `margin` and `gap`, or whether to introduce Flex/Grid primarily to get `gap`.
- Tuning vertical rhythm between components without ad hoc pixel values.
- Defining or auditing a spacing scale and mapping it to design tokens.
- Handling full-bleed or breakout layouts without habitual negative margins.
- Adjusting spacing across breakpoints (step changes, gutter tokens) while keeping one global scale.
- Reviewing a layout that relies on `margin-top` chains, `:first-child` margin stripping, or negative margins.

## Loading boundaries

- **Load this reference first** when the issue is whitespace rhythm, scale discipline, `gap` vs `margin`, grid vs flex for spacing, responsive gutters, or negative-margin smell.
- **Do not load this reference first** when the issue is purely breakpoint math or container-query thresholds (open [responsive.md](responsive.md) first), pure token grammar without spatial rules (open [tokens.md](tokens.md)), or hit-area/contrast policy (open [accessibility.md](accessibility.md)).

## Core policy

- Spacing encodes **relationship, hierarchy, and density** — not “empty decoration”.
- One **global discrete scale** applies to padding, gaps, and margins that participate in rhythm; literals outside the scale need a documented reason.
- **Primary rhythm** uses multiples of **8** (in `rem`); **4**-step increments are reserved for **micro** spacing inside dense components (icon gaps, tight controls).
- **Sibling and cell rhythm** is expressed with `gap` on a Flex or Grid parent whenever possible — not with chained child `margin`.
- **Negative margins** are not a default tool; they are allowed only for rare, intentional overlap with explicit justification.
- **Viewport width** changes which **step** or **gutter token** is appropriate; the scale table itself stays stable.

## Base unit and micro layer

- **8 — main grid.** Prefer `0.5rem` (8px at default 16px root), `1rem`, `1.5rem`, `2rem`, … for most padding, gaps, and section separation.
- **4 — micro only.** Use `0.25rem` (4px) only inside components for tight icon/text pairs or compact controls. Do not build page-level rhythm from 4 alone.

## Spacing scale (canonical steps)

Use these steps for padding, `gap`, and rhythmic margins. Map them to tokens per [tokens.md](tokens.md) (`--space-{n}`). Px values assume a **16px** root; prefer `rem` in CSS so spacing tracks user font settings.


| Step | `rem` | px (16px root) | Typical use                                        |
| ---- | ----- | -------------- | -------------------------------------------------- |
| 1    | 0.125 | 2              | Hairline separation, rare                          |
| 2    | 0.25  | 4              | Micro (icon inset, tight chip)                     |
| 3    | 0.5   | 8              | Small gap, dense stacks                            |
| 4    | 0.75  | 12             | Compact card padding, form clusters                |
| 5    | 1     | 16             | **Default** inset/gap for most UI                  |
| 6    | 1.5   | 24             | Section padding, relaxed stacks                    |
| 7    | 2     | 32             | Section separation, hero inset                     |
| 8    | 2.5   | 40             | Large sections (aligns with min hit area thinking) |
| 9    | 3     | 48             | Major vertical rhythm breaks                       |
| 10   | 4     | 64             | Page-level bands                                   |
| 11   | 5     | 80             | Wide layouts, marketing sections                   |
| 12   | 6     | 96             | Maximum common macro spacing                       |
| 13   | 10    | 160            | Rare hero / editorial span                         |


**Rules**

- **Padding** and `gap` on the same surface should usually pick from the same step or adjacent steps — not arbitrary off-scale values.
- **Gutter** (edge padding) uses the same steps; at page level, switch **which step or token** applies per breakpoint rather than inventing one-off pixels.

### Optional tighter profile

Teams that need a stricter 4-based micro grid may use steps **2–4** more often internally while keeping **8-based** steps for layout shells and sections. Do not mix profiles inside one component without reason.

## Spatial intent and terminology

Do not redefine terms; use [terminology.md](terminology.md).


| Intent                          | CSS / pattern                                         | Terminology                 |
| ------------------------------- | ----------------------------------------------------- | --------------------------- |
| Inset from own border           | `padding`, logical `padding-inline` / `padding-block` | `Box` context; not `Gutter` |
| Space between children          | `gap`, `row-gap`, `column-gap` on Flex/Grid           | `Gap`                       |
| Inline-axis inset from viewport | Outer wrapper `padding-inline` on `Inner` / shell     | `Gutter`                    |
| Vertical sibling rhythm         | Parent Flex/Grid + `gap`, or stack composition        | `Stack` / composition       |


## Implementation: prefer `gap`, prefer Flex/Grid

### Principle

**Prefer `gap` over `margin` for spacing between siblings.** This is not only “when you already have Flex/Grid”: structure layouts so a parent can own rhythm with `gap`.

### Layout choice

- Use **Flex** for single-axis lists, toolbars, and vertical stacks (`flex-direction: column` + `gap`).
- Prefer **Grid** when **rows and columns** both need rhythm: card grids, dense dashboards, responsive columns with consistent row/column spacing. Set `gap` (or `row-gap` + `column-gap`) on the grid container.
- A **one-column** vertical stack does not require Grid; Flex with `gap` is enough. **Use Grid when 2D rhythm or column templates are the point**, not as a blanket replacement for Flex.

### Why `gap`

- No margin collapsing between children; no `:last-child` margin zero hacks.
- Wrapping flex/grid lines keep spacing consistent on the last row.
- Rhythm is **owned by the parent**, which matches composition responsibility in [terminology.md](terminology.md).

### When `margin` remains acceptable

- Flow offsets outside a flex/grid group (e.g. centered block with `margin-inline: auto`).
- One-off separation not modeled as sibling groups.
- Typography conventions (e.g. heading `margin-block-end`) where `gap` is not the containing model.
- Intentional overlap (rare); document the intent.

**Avoid** using only child `margin-top` for vertical lists that could be a single column flex with `gap`.

### Logical properties and `rem`

- Prefer **logical** properties (`padding-inline`, `margin-block`, `gap`) for multi-writing-mode safety; pair with [responsive.md](responsive.md) for direction-agnostic layout.
- Use `rem` for spacing tied to readability and user zoom (see [typography.md](typography.md)).

### Coordination with responsive layout

- Use Flex/Grid inside **container-query** contexts per [responsive.md](responsive.md); spacing rules here do not replace threshold calculation — they govern **which step** you apply once layout structure is chosen.

## Responsive spacing

- **Claim:** Available width changes; the **same numeric step** is often too tight on small screens or too loose on large ones for **gutters** and **section shells**.
- **Practice:** Keep **one scale table**. At **page-level breakpoints**, switch **which step** you use (e.g. smaller gutter step on narrow, larger on wide) or swap **gutter tokens** — do not rely on “magic” per-pixel media queries scattered through components.
- **Container-level** layout still follows escalation in [responsive.md](responsive.md): intrinsic behavior first; container queries before viewport media queries where appropriate.
- Do not use the same gutter step everywhere if narrow viewports feel cramped; re-evaluate **step choice** per width band.

## Negative margins

### Policy

**Do not use negative margins by default.** CSS allows negative margins, but they are easy to misuse as **structural hacks**.

### Why avoid habitual use

- **Margin collapsing** with negative values is harder to reason about and review.
- Ancestors with `overflow: hidden` may clip content pulled “back” with negative margins.
- Undoing parent `padding` with negative margins hides layout problems instead of fixing hierarchy (wrapper split, grid column span, explicit full-bleed track).

### Preferred alternatives

- **Full-bleed / breakout:** use **Grid** column spanning, an extra grid track, or a dedicated outer wrapper — patterns belong in layout structure, not margin tricks.
- **Misaligned padding:** refactor **parent/child** boundaries or tokens instead of pulling children outward with negative margins.

### Exceptions

- Deliberate **overlap** for visual effect (e.g. layered cards) with **explicit** documentation or local convention.
- Legacy constraints where no structural change is possible — treat as **debt**, not pattern.

## Accessibility

Minimum touch targets and expanding hit areas are defined in [accessibility.md](accessibility.md). Spacing must not squeeze interactive targets below policy; if the visual control is small, use padding or pseudo-element expansion — not negative margin hacks that clip or confuse hit testing.

## Anti-patterns

- **NEVER** build rhythmic sibling spacing only with child `margin-top` / `margin-inline` chains, **because** it fights collapsing, wrapping, and parent-owned composition — use `gap` on Flex/Grid.
- **NEVER** use **negative margins** to cancel parent `padding` as a routine pattern, **because** it obscures structure and breaks under `overflow` changes.
- **NEVER** conflate **Gutter** with **Gap**, **because** edge protection and inter-item rhythm are different responsibilities ([terminology.md](terminology.md)).
- **NEVER** sprinkle **off-scale pixel** spacing without token or rationale, **because** rhythm drifts and themes cannot remap values.
- **NEVER** force **Grid** for a trivial single-column stack, **because** Flex + `gap` is simpler — use Grid when **2D** rhythm or column templates matter.
- **NEVER** keep **identical** page gutters on all breakpoints when narrow layouts feel cramped, **because** viewport-appropriate **step** changes are part of good rhythm.

## Checklist

- Padding and gaps use the **canonical scale** (or documented exception).
- **8-based** rhythm for layout; **4** only for **micro** internals.
- Sibling/cell spacing uses `gap` on Flex/Grid where possible.
- **Grid** used for **2D** layouts; **Flex** for single-axis stacks.
- **Logical** spacing properties preferred; `rem` for user-scaling alignment.
- **Gutter** vs **Gap** respected per [terminology.md](terminology.md).
- **Breakpoint** changes adjust **step or gutter token**, not one-off literals only.
- No habitual **negative margins**; full-bleed solved with **structure**.
- Hit areas meet [accessibility.md](accessibility.md) after spacing choices.

## Related references

- [tokens.md](tokens.md) — `--space-`* naming and aliases.
- [terminology.md](terminology.md) — `Gutter`, `Gap`, `Stack`, composition.
- [responsive.md](responsive.md) — intrinsic layout, container queries, breakpoints.
- [typography.md](typography.md) — measure, `rem`, type-adjacent spacing.
- [accessibility.md](accessibility.md) — targets, focus, reduced motion.