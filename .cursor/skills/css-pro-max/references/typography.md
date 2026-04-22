# Typography

Typography is the largest lever on readability and tone. This reference is the canonical source for font strategy, text-wrap behavior, Japanese typography specifics, `line-height`, readable measure, numeric feature rules, and fluid type. Accessibility policy references live in [accessibility.md](accessibility.md).

## When to use this reference

- Picking a font stack (`sans-serif`, `system-ui`, `@font-face` with `local()`).
- Configuring `text-wrap: balance` / `pretty` for headings and body, especially on Japanese pages.
- Setting `font-feature-settings`, `font-variant-east-asian`, `font-kerning` for CJK content.
- Tuning `line-height`, body measure (`45ch`–`75ch`), `text-box-trim`, hanging punctuation.
- Deciding `px` vs `rem` for text properties.
- Building a fluid-type utility with `clamp(rem, slope × svi + intercept, rem)`.
- Configuring `font-variant-numeric` for tabular numerals and numeric features.
- Handling manual line breaks (`<br>`, `<wbr>`, zero-width joiner, BudouX).

## Loading boundaries

- **Load this reference first** when the issue is readability, rhythm, line breaks, Japanese/English mixed text quality, or font-feature behavior.
- **Do not load this reference first** when the issue is structural layout collapse (open [responsive.md](responsive.md)) or interaction-motion behavior (open [animations.md](animations.md)).

## Font family

### Prefer the bare generic

The simplest posture is to leave type to the OS.

```css
:root {
  font-family: sans-serif;
}
```

This inherits the user's system font, matches system feel on every device, and avoids brand-font downloads entirely. In the vast majority of products, this is good enough.

### Do not reach for `system-ui` without a plan

`system-ui` maps to the OS default UI font, but the mapping is inconsistent:

- Windows tends to land on Segoe UI.
- macOS lands on San Francisco.
- In some Japanese environments, `system-ui` resolves to fonts that were never designed for UI (for example, Yu Mincho on older Windows or unexpected CJK fallbacks), which looks wrong.

If you want an explicit CJK stack, spell it out. If you do not, prefer `sans-serif`.

### Noto Sans JP with the `@font-face` local() pattern

When brand or design requires a specific Japanese face, prefer Noto Sans JP and use `@font-face` with `local()` to let already-installed copies on the OS or Adobe Fonts satisfy the request.

```css
@font-face {
  font-family: "NotoSansJP";
  font-style: normal;
  font-weight: 400 900;
  font-display: swap;
  src:
    local("Noto Sans CJK JP"),
    local("Noto Sans JP"),
    url("/fonts/NotoSansJP.woff2") format("woff2");
}

:root {
  font-family: "NotoSansJP", sans-serif;
}
```

Rules:

- List `local()` candidates first so local copies (macOS, Android, Adobe Fonts, etc.) are used directly. The remote font becomes a fallback.
- Noto Sans CJK JP is the OS-installed version; Noto Sans JP is the Google Fonts version. Both exist on real users' machines.
- `font-weight: 400 900` enables variable weight where supported. Serve a variable file for a single fetch and full weight range.
- `font-display: swap` prevents invisible text during download.

### Match fallback metrics

When you must download a brand font, add `size-adjust`, `ascent-override`, `descent-override`, `line-gap-override` to the `@font-face` fallback that users see until the brand font loads. This removes the layout jump when the brand font swaps in.

## Japanese semantic emphasis and italic policy

Japanese UI copy generally does not rely on italic emphasis. Keep semantic intent, but adapt visual output.

- For `em` in Japanese text, prefer stronger weight over italic style.
- Reset italic styling for semantic elements that default to italics in many UA styles (`i`, `cite`, `em`, `dfn`, `var`, `address`) when scoped to Japanese.
- Keep this rule language-scoped so English typography is unaffected.

```css
:where(em:lang(ja)) {
  font-weight: bolder;
}

:where(:is(i, cite, em, dfn, var, address):lang(ja)) {
  font-style: unset;
}
```

Rules:

- Scope by `:lang(ja)`; do not remove italic globally.
- Keep semantic tags in markup even when visual output changes.
- Validate readability with the selected Japanese font, especially at heading sizes.

## Text wrapping

### `text-wrap: balance`

Distributes width across all lines so a heading never ends on a single orphan word.

- Use on headings, short marketing copy, and calls-to-action.
- Implementations typically cap balanced lines at about 6–10; use on short text.
- Apply to headings by default:

```css
:where(h1, h2, h3, h4, h5, h6) {
  text-wrap: balance;
}
```

### `text-wrap: pretty`

Prevents orphans (the last line having a single word) on body text.

- Use on paragraphs and long-form body text.
- **Known Safari bug with Japanese**: as of Safari 18.x, `text-wrap: pretty` produces awkward line breaks in Japanese text (breaks appear mid-token, sometimes leaving a single character on the final line). Until Safari fixes this, scope `text-wrap: pretty` to `:lang(en)` or similar, or skip it on Japanese pages entirely.

```css
:where(p) {
  text-wrap: pretty;
}

/* Guard against the Safari Japanese bug. */
:where(p):lang(ja) {
  text-wrap: wrap;
}
```

### `overflow-wrap` and `line-break`

- `overflow-wrap: anywhere` on containers that may receive unbreakable tokens (URLs, hashes, filenames).
- `line-break: strict` tightens Japanese line-break behaviour around punctuation; use inside prose.

## `font-feature-settings` — Japanese kerning via `palt` / `vpal`

OpenType features let fonts reflow punctuation and width with Japanese text.

- `palt` — "proportional alternate widths" horizontally. Removes the extra space around punctuation like `、`, `。`, `「` in horizontal writing mode.
- `vpal` — the same in vertical writing mode.
- Apply both when supporting both writing modes.

```css
:root:lang(ja) {
  font-feature-settings: "palt" 1, "vpal" 1;
}
```

Caveats:

- `palt`/`vpal` can look too tight on body text. Use on headings and short lines; leave long prose alone.
- Any `font` shorthand after this will reset the feature setting. Set `font-feature-settings` last or avoid the shorthand.

### Relationship with `font-kerning`

- `palt`/`vpal` and `font-kerning` operate on different layers and are not additive.
- `palt`/`vpal` reflow glyph widths via proportional-alternate metrics.
- `font-kerning` adjusts pair spacing via the OpenType `kern` table.
- On high-quality Japanese fonts, enabling both often produces the intended compact display at heading sizes.

## `font-variant-east-asian`

A higher-level alternative to `font-feature-settings` with more robust cascade handling.

```css
:where(h1, h2, h3):lang(ja) {
  font-variant-east-asian: proportional-width;
}
```

- `proportional-width` is the high-level equivalent of `palt`.
- `traditional` / `simplified` switch variant forms.
- Unlike `font-feature-settings`, `font-variant-*` properties stack without overriding each other.

## `font-kerning` — Japanese vs English tradeoff

`font-kerning: normal` enables OpenType `kern` pair tables. For Latin text this improves spacing measurably. For Japanese text it is more complicated:

- Japanese fonts frequently carry `kern` tables that target Latin pairs inside mixed Japanese/English text. Some fonts carry aggressive CJK kerning that backfires at body-text sizes.
- Scoping by language is a common pattern:

```css
:root:lang(en) {
  font-kerning: normal;
}

:root:lang(ja) {
  font-kerning: none;
}
```

- If you want kerning applied only to Latin pairs embedded in Japanese text, there is no portable switch today; `font-kerning: normal` will apply to both sides of the font's kern table.
- Rule of thumb:
  - Heading display text: `palt`/`vpal` + `font-kerning: normal` is acceptable when the chosen font renders cleanly.
  - Body text: keep `palt`/`vpal` limited to headings (or off) and keep `font-kerning` at the engine default (`auto`) or `none` for `:lang(ja)` when the body appears over-kerned.

### The `apkn` / `vapk` future

OpenType defines `apkn` (alternate proportional kerning) and `vapk` (vertical alternate proportional kerning), which target Japanese kerning specifically.

Recommended staging:

- **Today (until broad browser support lands)**: apply `palt`/`vpal` to `:lang(ja)` headings, and keep `font-kerning: none` (or `auto` after visual validation) on `:lang(ja)` body text.
- **When `apkn`/`vapk` support is broadly available**: use `font-feature-settings: "palt" 1, "vpal" 1, "apkn" 1, "vapk" 1` on `:lang(ja)` headings and keep a bare `font-kerning: normal` on `:lang(en)`.

## `text-autospace` and `text-spacing-trim`

CSS Text 4 introduces two properties for spacing around Japanese punctuation and ideograph/Latin boundaries.

- `text-autospace` inserts ideographic quarter-width space between CJK and non-CJK glyphs. Values include `normal`, `ideograph-alpha`, `ideograph-numeric`, `no-autospace`.
- `text-spacing-trim` trims unnecessary space around Japanese punctuation at line starts/ends. Values include `normal`, `space-all`, `space-first`, `trim-start`.

```css
:where(p):lang(ja) {
  text-autospace: ideograph-alpha ideograph-numeric;
  text-spacing-trim: trim-start;
}
```

Treat both as progressive enhancement; fallbacks are fine.

## `line-height`

- Body text should have `line-height: 1.5` or more.
- Small labels, badges, and dense tables may go down to `1.25`.
- Headings can sit at `1.1`–`1.3`.
- `line-height: 1` is reserved for single-line UI where vertical centering depends on it.
- Avoid unitless heights on inherited chains where child font-sizes change (use `1lh` context or re-declare).

## Measure (readable line length)

Long-form body text reads fastest in the `45ch`–`75ch` range. Keep an upper bound on prose containers rather than letting text span the full viewport.

```css
:where(.prose, article, .rich-text) {
  max-inline-size: 72ch;
}
```

- Use `max-inline-size` (not `width`) so the bound applies per writing mode.
- `ch` units scale with the computed font size, so the bound tracks user zoom.
- For UIs with dense secondary text (sidebars, captions, labels), the upper bound is irrelevant — only prose needs it.
- For wider layouts that must contain prose, place the measure constraint on the prose block, not on the outer column.

## `text-box-trim` / `text-box-edge`

`text-box-trim` removes the leading above and below a line of text, so the visual baseline matches the element's box.

```css
.display-heading {
  text-box-trim: trim-both;
  text-box-edge: cap alphabetic;
}
```

- Use on headings with tight surrounding UI (cards, buttons, stat numbers).
- Where the feature is not supported, `calc((1lh - 1em) / 2)` can be used to offset the half-leading manually as a fallback.

## `hanging-punctuation`

Allows opening and closing punctuation to hang outside the text block so the visual left edge aligns with glyphs.

```css
:where(p):lang(ja) {
  hanging-punctuation: allow-end last;
}
```

- Japanese text benefits from `allow-end last` to hang closing brackets and periods.
- English text benefits from `first last allow-end`.
- Only Safari supports this widely; treat as progressive enhancement.

## `line-clamp`

The modern `line-clamp` property truncates block text to N lines.

```css
.excerpt {
  display: block;
  overflow: clip;
  line-clamp: 3;
}
```

- Use `overflow: clip` (not `hidden`) to avoid accidental scroll containers.
- Older codebases use the `-webkit-line-clamp` path with `display: -webkit-box`; the modern path is now supported widely.
- Avoid clamping where the full text is meaningful (legal notices, error messages).

## `word-break: auto-phrase` + BudouX

Japanese line breaking at phrase boundaries is difficult. CSS `word-break: auto-phrase` lets the browser apply phrase-aware breaking in Chromium. Combined with [BudouX](https://github.com/google/budoux) (a phrase-boundary model) as a polyfill, lines break at readable boundaries.

```css
:where(h1, h2, h3):lang(ja) {
  word-break: auto-phrase;
  overflow-wrap: break-word;
}
```

- Combine with `text-wrap: balance` for short headings.
- Where `auto-phrase` is unsupported, use BudouX to insert `<wbr>` or zero-width joiners (see below) at phrase boundaries.

## `hyphens`

`hyphens: auto` enables automatic hyphenation in supported languages. Japanese does not hyphenate.

```css
:where(p):lang(en) {
  hyphens: auto;
}
```

Requires a `lang` attribute on a containing element.

## `text-transform`

- `text-transform: uppercase` does not respect many scripts (including Japanese and several Latin cases with ligatures). Use sparingly.
- When uppercasing Latin text, add a touch of `letter-spacing` (about `0.04em`) to restore optical spacing.

## `font-variant-numeric`

This is the canonical source for numeric feature rules. Apply them where digits matter for layout or legibility.

### Tabular numerals

Any number that updates in place must use tabular numerals so digits do not shift horizontally as values change.

```css
.counter, .price, .timer, .tabular {
  font-variant-numeric: tabular-nums;
}
```

Apply to:

- Counters, timers, progress percentages.
- Price ladders and tables of numbers.
- Vote counts, notification badges, ETA strings.
- Any column of right-aligned numbers.

Rules:

- **Do not** apply `tabular-nums` to prose. Proportional widths read more naturally in running text.
- When you need both tabular and another feature (e.g. lining), combine in a single declaration: `font-variant-numeric: tabular-nums lining-nums;`.
- `font-feature-settings: "tnum" 1` is the lower-level equivalent. Prefer `font-variant-numeric` so it composes cleanly with other numeric features.

### Other numeric features

- `lining-nums` — uniform-height figures; default for most sans-serif UI. Useful alongside `tabular-nums` in data tables.
- `oldstyle-nums` — varying-height figures; use in editorial prose with a serif face designed for them.
- `slashed-zero` — disambiguates `0` from `O` in dense technical UI (credit-card numbers, IDs).
- `ordinal` — raises ordinal suffixes (`1st`, `2nd`) when the font supports it.

### Visual-detail cross-link

Polish-level reminder that tabular numerals matter is also in [visual-details.md](visual-details.md) principle 8. The detailed rules above are the canonical source.

## Hanging `text-indent`

For Japanese paragraph structure that indents the second line and onward under the first:

```css
.dictionary-entry {
  text-indent: -1em;
  padding-inline-start: 1em;
}
```

Used for references, bibliographies, and definitions.

## Fluid typography utility

Build one fluid-type utility and reuse it. See [responsive.md](responsive.md) for the derivation of `clamp(min, slope × unit + intercept, max)`. A common structure:

```css
:where(body) {
  font-size: clamp(
    14 / 16 * 1rem,
    0.00455 * 100svi + 12.18 / 16 * 1rem,
    18 / 16 * 1rem
  );
}
```

- Keep the `rem` minimum so user zoom continues to scale the base.
- Do not apply fluid sizing to micro-UI (badges, nav items) — it creates subpixel inconsistency.

## `px` vs `rem`

Rules:

- Use `rem` for anything tied to readability: `font-size`, `line-height`, paragraph spacing, and `gap`/`padding` that scales with text.
- Use `px` for things that are visual, not textual: 1-pixel borders, hairlines, icon strokes, focus outlines.
- Media-query breakpoints use `rem` (so user zoom moves the breakpoint).
- Tokens are stored in px (for designer parity) and converted at the consumption site: `calc(24 / 16 * 1rem)`.

## Manual line breaks

### `<br>` — last resort

- `<br>` is a hard break. It does not participate in `text-wrap: balance` gracefully and can produce orphans.
- Reserve `<br>` for addresses, poetry, and other structural breaks.

### `<wbr>` — soft break hint

- `<wbr>` inserts a word-break opportunity. It is invisible until a break is needed.
- Combine with `white-space: nowrap` to opt into controlled breaking.

### Zero-width joiner (U+200B / U+200D)

- U+200B (zero-width space) inserts a potential break point with no visible character. Use for long compound Japanese terms where you want the browser to break at specific spots.
- U+200D (zero-width joiner) prevents a break between two glyphs. Use inside ligature-critical sequences.

### BudouX integration

Pipe CMS or static-site text through BudouX during build or at runtime to insert zero-width spaces at phrase boundaries. Combined with `word-break: auto-phrase`, this achieves phrase-aware Japanese line breaking with a graceful fallback.

## Checklist

- Font stack is either `sans-serif` or uses the `@font-face` `local()` pattern.
- Body `line-height` is `1.5` or more; headings between `1.1` and `1.3`.
- Headings use `text-wrap: balance`; Japanese body avoids `text-wrap: pretty` while the Safari bug remains.
- Japanese headings have `font-feature-settings: "palt" 1, "vpal" 1` or the equivalent `font-variant-east-asian`.
- Japanese semantic emphasis uses `em:lang(ja) { font-weight: bolder; }` and resets italic defaults via language-scoped rules.
- `font-kerning` follows the `:lang(en)` vs `:lang(ja)` rule; prepare to migrate to `apkn`/`vapk` when support lands.
- `text-autospace` and `text-spacing-trim` are applied where supported.
- Body prose is bounded in the `45ch`–`75ch` measure range.
- Numeric UI uses `font-variant-numeric: tabular-nums`; prose does not.
- `line-clamp` uses `overflow: clip`.
- `word-break: auto-phrase` is on for `:lang(ja)` headings; BudouX is in place for broader support.
- `hyphens: auto` is on for `:lang(en)` body text.
- `text-transform: uppercase` adds `letter-spacing`.
- Fluid typography retains a `rem` minimum.
- `px` is reserved for borders, hairlines, and focus outlines.
- Manual line breaks use `<br>` sparingly; `<wbr>` / zero-width joiner used for soft breaks.

## Fallback mini-playbook

When text quality degrades and root cause is unclear, recover in this order:

1. Restore baseline readability first (`line-height >= 1.5`, measure `45ch`-`75ch`, `rem` floor in fluid type).
2. Disable aggressive features (`text-wrap: pretty` for Japanese body, overly tight kerning) until prose is stable.
3. Re-enable advanced features (`palt`/`vpal`, `auto-phrase`, BudouX hints) only where they improve headings without harming body text.

## Related references

- [responsive.md](responsive.md) — fluid-type math (`clamp(min, slope × svi + intercept, max)`), viewport units, `cqi`.
- [accessibility.md](accessibility.md) — contrast targets, `rem` floors for user zoom, semantic color tokens.
- [visual-details.md](visual-details.md) — font smoothing, tabular-numeral polish, text-wrap polish.
- [animations.md](animations.md) — motion interaction with typographic state (e.g., `text-box-trim` during enter).

