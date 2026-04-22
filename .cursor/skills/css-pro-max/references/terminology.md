# Design System Terminology

Naming is not labelling; it is a design contract that expresses responsibility, meaning, behaviour, scope, and reuse rules. This reference is the canonical vocabulary for the design system so that designers, engineers, writers, and operators all mean the same thing.

## When to use this reference

- Choosing names for new components, patterns, sections, or layout primitives.
- Reviewing an existing naming choice against canonical terms.
- Resolving a disagreement over whether something is a `Link`, `Button`, `Menu`, `Navigation`, `Component`, `Pattern`, or `Template`.
- Deciding between `Inner` and `Outer`, `Gap` and `Gutter`, `Columns`, `Flex Columns`, and `Grid`.
- Authoring design-system glossaries, component indexes, and implementation guidelines.
- Authoring CMS / page-builder / no-code UI terminology that must match internal documentation.

## Core policy

- Terms must not contradict established web standards.
- Terms must be defined by responsibility, not appearance.
- Static structure, dynamic UI, reusable parts, page-level rendering definitions, and visual themes must never be conflated.
- A word must carry one meaning only.
- One word must not collect multiple concepts under it.

## Foundational principles

### 1. Do not redefine words that already have a web-standard meaning

If HTML, CSS, ARIA, or browser implementations have given a word a stable meaning, that meaning takes precedence. The following are especially prone to collision and must not be repurposed as convenience names:

- `block`
- `container`
- `button`
- `menu`
- `columns`
- `row`

### 2. Name by responsibility, not appearance

A name reflects role, meaning, HTML element, behaviour, and scope — not how it looks. If an element that looks like a button is actually an `<a>`, its name is `Link`, not `Button`. If the element is a `<button>`, its name is `Button`.

### 3. Do not conflate structure and behaviour

Structural elements, static patterns, dynamic UI, components, templates, and themes are separate categories. Keep the boundaries visible in the vocabulary.

### 4. Use broad words narrowly

Words that are too broad blur responsibility. `Block`, `Module`, `Widget`, `Container` should not be official names at the top level.

### 5. Names must express design boundaries

Naming partitions responsibility. A vague name is a symptom of a vague boundary.

## Layout primitives vocabulary

These terms describe reusable layout behavior. They are not component names by default.

### Stack

#### Definition

`Stack` is vertical flow spacing applied by parent context (`* + *`) between siblings.

#### Rules

- Use `Stack` when the main responsibility is vertical rhythm.
- Treat `Stack` as context behavior, not as a content component.
- `Stack` does not define column logic.

### Box

#### Definition

`Box` is a containment primitive that provides padding, border, and optional visual surface.

#### Rules

- Use `Box` when containment and internal edge distance are the primary responsibilities.
- A `Box` may be nested inside any other primitive.

### Center

#### Definition

`Center` constrains readable inline size and centers content in the inline axis.

#### Rules

- Use `Center` for readable measure and horizontal centering.
- Do not call every centered flex wrapper a `Center`; only use when measure control is part of the contract.

### Cluster

#### Definition

`Cluster` is an inline wrapping group that keeps consistent horizontal/vertical gaps while items wrap naturally.

#### Rules

- Use `Cluster` for tag groups, inline controls, and mixed small actions.
- If column logic is required, prefer `Grid` or `Switcher`.

### Sidebar

#### Definition

`Sidebar` is a two-region layout where one side has fixed/intrinsic behavior and the other side flexes.

#### Rules

- Use `Sidebar` when side/main responsibilities are asymmetric.
- Do not rename generic two-column grids as `Sidebar` unless asymmetry is explicit.

### Switcher

#### Definition

`Switcher` is a layout that stays inline until a threshold, then stacks items.

#### Rules

- Use `Switcher` when item count/width should decide row vs stack behavior.
- Thresholds must be content-derived, not device-derived.

### Cover

#### Definition

`Cover` is a full-block layout with optional top and bottom regions and one centered focal region.

#### Rules

- Use `Cover` for hero-like or modal-like vertical composition where center emphasis matters.
- `Cover` is about vertical composition, not just full-height visuals.

### Frame

#### Definition

`Frame` preserves aspect ratio for media slots.

#### Rules

- Use `Frame` when ratio stability is a contract (image/video cards, embeds).
- Keep crop behavior explicit (`object-fit`, focal point tokens).

### Reel

#### Definition

`Reel` is a horizontal scroller with item sequence and controlled snap/overflow behavior.

#### Rules

- Use `Reel` for chip rails, card rails, and media strips.
- Do not use `Reel` when wrapping layout is required; use `Cluster` or `Grid`.

### Imposter

#### Definition

`Imposter` is an overlay primitive that positions a surface over another context.

#### Rules

- Use `Imposter` for overlays, anchored sheets, and transient floating surfaces.
- Layering policy for `Imposter` is defined in [z-index.md](z-index.md).

### Icon

#### Definition

`Icon` is a semantic glyph primitive used as visual support, not a button contract by itself.

#### Rules

- `Icon` remains a visual primitive; interaction semantics come from `Button`/`Link`.
- Keep icon sizing and alignment rules independent from naming semantics.

### Container (layout primitive context)

#### Definition

As a layout primitive term, `Container` represents query-container context for descendant adaptation.

#### Rules

- This usage must remain consistent with the CSS `container` feature definition in this file.
- Generic content-width wrappers are still `Inner`, not `Container`.

## Architecture vocabulary

This vocabulary defines CSS architecture responsibilities and should coexist with `Pattern`, `Component`, and `Template`.

### Composition

#### Definition

`Composition` is layout flow and spatial orchestration across elements.

#### Rules

- Put spacing/rhythm/layout primitives in composition scope.
- Composition should not carry component skin decisions.

### Utility

#### Definition

`Utility` is a single-purpose class or declaration set that performs one job.

#### Rules

- Utilities must stay atomic and predictable.
- Utilities are not replacements for component contracts.

### Block

#### Definition

In architecture context, `Block` means a self-contained styling unit with internal parts.

#### Rules

- This architectural meaning is valid only when explicitly scoped to architecture discussions.
- Do not use `Block` as a canonical element-level naming term elsewhere in this vocabulary.

### Exception

#### Definition

`Exception` is a deliberate local deviation from baseline composition/block/utilities.

#### Rules

- Keep exceptions explicit, rare, and easy to remove.
- If exceptions repeat, promote them into composition, utility, or component contracts.

## Term definitions

### Element

#### Definition

`Element` is an HTML element itself, or the smallest unit that corresponds directly to an HTML element.

Examples:

- `div`
- `section`
- `h1`–`h6`
- `p`
- `a`
- `button`
- `img`
- `ul`
- `table`

#### Rules

- Units that map one-to-one to an HTML element must be called `Element`.
- When speaking generically about HTML elements, prefer `Element`.
- Do not wrap HTML elements in an additional abstract term.

#### Forbidden

- Calling every element `Block`.
- Using `Module` or `Widget` as an umbrella for HTML elements.

### Section

#### Definition

`Section` is a semantic or structural region inside a page, used as a higher-level grouping concept. The default HTML implementation is the `<section>` element, with `<article>` and other semantic elements as context-specific alternatives.

#### Rules

- Regions inside a page are called `Section`.
- `Section` is a conceptual name; it is not strictly one-to-one with the `<section>` element.
- Distinguish the cases where `<section>` is correct from the cases where a different semantic element is correct.
- A `Section` is not the same thing as a content-width wrapper.

#### Forbidden

- Calling any generic box `Section` without reason.
- Using `Section` to mean "content-width wrapper".

### Container

#### Definition

`Container` refers to an element on which the CSS `container` property has been applied.

#### Rules

- Only elements with the `container` family of properties are `Containers`.
- Always name in pairs (for example, `section container`). `Container` alone fails to state the "of what".
- `Container` is a technical term for the CSS container feature; never use it as the name of a content-width wrapper.

#### Forbidden

- Calling every structural box `Container`.

#### Note

Some CSS frameworks (Bootstrap and similar) use `Container` for a content-width wrapper. This vocabulary does not adopt that usage. Content-width wrappers are `Inner`; `Container` is reserved for the CSS container feature.

### Inner / Outer

#### Definition

`Inner` is the inner wrapper placed directly inside a `Section` (or similar), responsible for content-width control and horizontal centring.

`Outer` is the outer wrapper placed outside a component or pattern, responsible for outside margins, surrounding placement, and other external-relationship layout concerns.

#### Rules

- Content-width control is the responsibility of `Inner`.
- `Outer` is reserved for external spacing, alignment, and adjacent-element relationships.
- Always pair `Inner` / `Outer` with a subject: `section inner`, `card outer`. Never use them alone.
- Do not use `Inner` / `Outer` as generic wrappers.

#### Note

A typical structure is `Section > SectionInner > ChildComponent` or `Section > SectionInner > ChildComponentOuter > ChildComponent`.

Both `Inner` and `Outer` belong to the component as children. Do not nest `ChildComponentOuter` inside `ChildComponent` itself, and do not promote `ChildComponentOuter` to a component of its own.

#### Forbidden

- Confusing `Inner` / `Outer` with the container-query subject.
- Defining `Inner` / `Outer` as anything other than a child of a component.

### Gutter

#### Definition

`Gutter` is the inline-axis padding that protects content from the viewport edge.

#### Rules

- Edge-protecting inline padding is called `Gutter`.
- Gutter values are tokenised and shared across the system.
- Do not replace `Gutter` with ad-hoc `padding` tweaks per section.

#### Forbidden

- Calling column or item spacing `Gutter`.
- Treating `Gutter` as synonymous with `gap` or `space`.

### Gap

#### Definition

`Gap` is the spacing between children in Flex, Grid, or Multi-column layouts.

#### Rules

- Between-element distances are called `Gap`.
- Row gaps, column gaps, card gaps, chip gaps — all belong to `gap`.
- Keep `Gap` and `Gutter` strictly separated.

#### Forbidden

- Calling normal-flow `margin` `Gap`.

#### Note

Numeric spacing steps, `gap` vs `margin`, and responsive gutter policy → [spacing.md](spacing.md).

### Columns

#### Definition

`Columns` refers to structure produced by CSS Multi-column Layout.

#### Rules

- Only column arrangements produced by Multi-column Layout are `Columns`.
- Flexbox-based column arrangements are `Flex Columns`.
- Grid-based column arrangements are `Grid`.

#### Forbidden

- Calling a Flex or Grid layout simply `Columns`.
- Lumping Flex/Grid layouts together with Multi-column under the same term.

### Flex Columns

#### Definition

`Flex Columns` is the column structure produced by Flexbox placing items along the horizontal axis.

#### Rules

- Flexbox-based column arrangements are called `Flex Columns`.
- Do not confuse them with `Columns` (Multi-column Layout) or `Grid`.

#### Forbidden

- Referring to a Flexbox-based column arrangement as `Columns`.

### Grid

#### Definition

`Grid` is structure produced by CSS Grid Layout. It is the first-class choice for structural layout design.

#### Rules

- For structural layouts, consider `Grid` first.
- `Grid` and `Flex` are separate concepts and must be described separately.

### Row

#### Definition

`Row` is not a standalone element name; it is a placement concept that arises from a parent layout context.

#### Rules

- Do not define `Row` as a standalone element type.
- Describe `Row` as the result of a layout, not a thing in itself.

#### Forbidden

- Introducing `Row` as a canonical element name.

### Paragraph

#### Definition

`Paragraph` is a single paragraph or a single block of text.

#### Rules

- Call single-paragraph text `Paragraph`.
- Keep `Paragraph` and `Rich Text` as separate definitions.

#### Forbidden

- Referring to single paragraphs as the vague `Text`.

### Rich Text

#### Definition

`Rich Text` is an editorial region that may contain multiple inline decorations and multiple kinds of child elements.

#### Rules

- Long-form editorial regions are called `Rich Text`.
- When offering a `Rich Text`, also design the control surface for child elements.
- Do not conflate `Rich Text` with single paragraphs or simple text insertion.

#### Forbidden

- Grouping `div`, `p`, `span`, and long-form editorial regions under `Text`.
- Placing a `Rich Text` as a core building block without control over its children.

### Link

#### Definition

`Link` is the navigation element, corresponding to HTML's `<a>`.

#### Rules

- Any element using `<a>` is a `Link`.
- A `Link` may be styled to look like a button, but that is a visual matter and does not justify renaming it.

#### Forbidden

- Calling an `<a>` a `Button` in official vocabulary.

### Button

#### Definition

`Button` is the element that fires in-page events or state changes, corresponding to HTML's `<button>`.

#### Rules

- Any element using `<button>` is a `Button`.
- `Button` is defined by meaning and behaviour, not appearance.
- Styling an `<a>` to look like a button is permissible as a visual decision; it is not a reason to call it a `Button`.

#### Forbidden

- Calling an element `Button` because it looks like one.
- Treating `<a>` as a `Button` by default.

#### Link / Button edge cases

- `<input type="submit">`, `<input type="button">`, and `<input type="reset">` behave as `Button`.
- `<a role="button">` is treated as a `Button` because its responsibility is now button-like, though this pattern should be avoided in principle.
- ARIA roles add semantics but are not the primary decider for the canonical name.

### Navigation

#### Definition

`Navigation` is the region that carries wayfinding inside a site or app. It corresponds to `<nav>` by default.

#### Rules

- Site wayfinding is called `Navigation`.
- When scope matters, qualify: `Primary Navigation`, `Footer Navigation`, `Local Navigation`.

#### Forbidden

- Calling site wayfinding `Menu` in canonical naming.

### Menu

#### Definition

`Menu` is a UI for executing commands or selecting operations. It is not used for site wayfinding.

#### Rules

- UIs whose items are commands or choices to execute are called `Menu`.
- Qualify as needed: `Edit Menu`, `Command Menu`.
- Site wayfinding is `Navigation`, not `Menu`.

#### Forbidden

- Using `Menu` for site navigation.
- Using `Nav` for toolbars or command pickers.

### Template

#### Definition

`Template` is the rendering definition applied at the page level or at a comparable top-level unit. A `Template` can involve dynamic data, conditional logic, build-time data injection, or swappable page structures.

#### Rules

- `Template` denotes a page-level or equivalent rendering definition, not a static fragment.
- Keep `Template` separate from `Pattern` and `Component`.

### Pattern

#### Definition

`Pattern` is a reusable, static visual fragment.

#### Rules

- Reusable, static visual fragments are called `Pattern`.
- A `Pattern` does not assume dynamic data or conditional logic.
- Keep `Pattern` separate from `Template` and `Component`.

#### Forbidden

- Calling a static layout fragment a `Template`.
- Treating any reusable fragment as a `Component` by default.

### Component

#### Definition

`Component` is a reusable unit managed from a single definition, with explicit input surfaces (props, slots, content areas, variants) and a declared contract over structure, presentation, and optionally behaviour.

#### Rules

- A `Component` is managed from a single source.
- A `Component` should expose swappable inputs (props, slots, content areas, variants).
- A `Component` has a definition/instance relationship, not just duplicate markup.

#### Forbidden

- Calling something a `Component` only because its visual is shared.

### Dynamic Element

#### Definition

`Dynamic Element` is an interaction-centred UI element driven by JavaScript or state transitions.

#### Rules

- `Dynamic Element` is a behaviour axis, not a structural rung.
- `Dynamic Element` and `Component` are not mutually exclusive. A dynamic UI with a reuse contract is both.

#### Forbidden

- Treating `Dynamic Element` and `Component` as exclusive categories on the same axis.
- Collapsing all behaviour-driven UIs into the single term `Component`.

### Theme

#### Definition

`Theme` is the bundle of visuals — tokens, typography, colour, spacing, pre-configured layout — that sits atop a shared architecture.

#### Rules

- Themes are defined independently of the architecture.
- Themes carry appearance and default-value differences, not structural or functional ones.
- Swapping a theme must not break the architecture or dynamic logic.

#### Forbidden

- Calling the architecture itself a `Theme`.
- Assuming that theme changes require structural breakage.

## Deprecated terms

Not recommended as official names.

### Block

CSS's `display: block` and adjacent logical keywords collide with it, and as a general-purpose word it is too vague.

### Wrapper

This system splits wrapper responsibilities into `Inner` (content-width) and `Outer` (external relationships). `Wrapper` fails to express which responsibility is meant.

### Text

Cannot differentiate single paragraph, inline text, and long-form editorial region.

### Widget / Module

Scope is undefined and these do not express a design boundary.

## Decision flow

Before coining a new name, answer:

### 1. Is the word already defined by a web standard?

If yes, only use the word when your meaning matches. If your meaning differs, pick another name.

### 2. Is the name about appearance?

If yes, rework it. Prefer responsibility, meaning, HTML element, behaviour, or scope.

### 3. Is it static or dynamic?

Static things are likely `Pattern`. Dynamic things are likely `Dynamic Element`; page-level conditionally-rendered things are likely `Template`.

### 4. Is it managed from a single source?

If yes, and it carries a reuse contract, it is probably `Component`. Otherwise it is a `Pattern` or a plain `Element`.

### 5. Does it apply to a full page?

If yes, and it is conditionally applied, consider `Template`. Otherwise do not call it `Template`.

## Recommended mapping


| Purpose                                  | Recommended       | Deprecated                     |
| ---------------------------------------- | ----------------- | ------------------------------ |
| Umbrella term for HTML elements          | `Element`         | `Block`, `Module`, `Widget`    |
| Section boundary                         | `Section`         | `Group`                        |
| Element with the CSS `container` feature | `Container`       | `Generic container`, `Wrapper` |
| Content-width wrapper                    | `Inner`           | `Container`, `Wrapper`         |
| External-relationship wrapper            | `Outer`           | `Wrapper`                      |
| Edge-protecting padding                  | `Gutter`          | `Padding`, `Column gutter`     |
| Between-item spacing                     | `Gap`             | `Gutter`                       |
| Multi-column columns                     | `Columns`         | `Flex Columns`, `Grid Columns` |
| Flex-based columns                       | `Flex Columns`    | `Columns`                      |
| Grid-based structure                     | `Grid`            | `Columns`, `Grid Columns`      |
| Single paragraph                         | `Paragraph`       | `Text`                         |
| Long-form editorial                      | `Rich Text`       | `Text`                         |
| `<a>`                                    | `Link`            | `Button`, `Link Button`        |
| `<button>`                               | `Button`          | `Link Button`                  |
| Site wayfinding                          | `Navigation`      | `Menu`                         |
| Command menu                             | `Menu`            | `Nav`                          |
| Static reusable fragment                 | `Pattern`         | `Template`                     |
| Page rendering definition                | `Template`        | `Pattern`                      |
| Unit with a reuse contract               | `Component`       | `Static copy`                  |
| Behaviour-centred UI                     | `Dynamic Element` | Blanket `Component`            |
| Appearance differences                   | `Theme`           | `Architecture`                 |


## Documentation rules

### 1. Every canonical term needs a definition

At a minimum, each entry must state:

- What it refers to.
- What it does not refer to.
- Where it is used.
- Where it is not used.

### 2. Prefer parity between UI labels and canonical names

When product UI and implementation documentation diverge, onboarding costs rise and misunderstandings multiply.

### 3. Treat term changes as breaking changes

Renaming is a model change, not a label change. Do not rename without assessing impact.

### 4. Slang is not a canonical name

Even when colloquial names are tolerated, the canonical name must exist separately in official documentation.

## Final rule

The purpose of this vocabulary is to sharpen design boundaries, not to polish word choice. When a name is unclear, test it against:

- Does it contradict HTML or CSS semantics?
- Does it describe responsibility, not appearance?
- Does it keep static / dynamic / structural / thematic / template separate?
- Does it communicate reuse conditions?
- Will it survive long-term maintenance and onboarding?

A vague name is a reliable signal of a vague responsibility. Kill the vagueness at the naming layer.

## Checklist

Run before merging a naming choice.

- Name does not contradict an existing HTML/CSS/ARIA meaning.
- Name describes responsibility, not appearance.
- Deprecated words (`Block`, `Wrapper`, `Text`, `Widget`, `Module`) are absent from the canonical name.
- `Container` is reserved for elements with the CSS `container` feature; content-width wrappers are `Inner`.
- `Inner` / `Outer` / `Container` are always paired with a subject (`section inner`, `card outer`, `section container`).
- `Gap` (between-child spacing) and `Gutter` (edge-protecting inline padding) are kept separate.
- `Columns` only refers to Multi-column Layout; Flex-based columns are `Flex Columns`; Grid structures are `Grid`.
- `Link` refers to `<a>`; `Button` refers to `<button>`; styling does not flip either.
- `Navigation` (wayfinding) and `Menu` (commands) are not interchanged.
- `Pattern` (static reusable fragment), `Component` (reuse contract), and `Template` (page-level rendering) are each distinct.
- `Dynamic Element` is treated as a behaviour axis, not as a replacement for `Component`.
- `Theme` applies to appearance only; architectural differences are not called a theme.
- Layout primitive names (`Stack`, `Cluster`, `Sidebar`, `Switcher`, `Cover`, `Frame`, `Reel`, `Imposter`) are used only when their responsibilities match.
- `Composition` / `Utility` / `Block` / `Exception` are used as architecture terms, not mixed with element-level canonical naming.
- A term change is treated as a breaking change and communicated accordingly.

## Related references

- [responsive.md](responsive.md) — technical rules that reuse `Container`, `Inner`, `Outer`, `Gap`, `Gutter`.
- [visual-details.md](visual-details.md) — component-level polish that depends on consistent `Inner` / `Outer` usage.
- [accessibility.md](accessibility.md) — `Link` vs `Button` decisions that affect semantics.
- [z-index.md](z-index.md) — layering responsibility for overlays and floating surfaces.
- [foundation.md](foundation.md) — cascade-layer architecture and low-specificity baseline terms.