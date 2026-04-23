# CSS Pro Max

上級者向けの **CSS / レイアウト / タイポグラフィ / アニメーション / アクセシビリティの実務基準**を、日本語ドキュメントサイト（学習導線）と Agent Skill（AI 向け英語正典）の 2 経路で配布しています。

- Docs: https://css-pro-max.h2cos.workers.dev
- Agent Skill 正典: [.cursor/skills/css-pro-max/SKILL.md](.cursor/skills/css-pro-max/SKILL.md)

## 想定読者

- 実装とレビューの両方を担うフロントエンド上級者
- デザインシステムを運用・改善している職能
- PR で「根拠付きの指摘」を返す必要がある人

## 収録トピック（全 12 章）

- **設計基盤**: Terminology / Foundation / Responsive / Tokens / Spacing / Color / Z-Index / Typography / Accessibility
- **モーションと表現**: Animations / Keyframes / Visual Details

各章の詳細と学習順はドキュメントサイト（https://css-pro-max.h2cos.workers.dev）を参照。

## 二つの配布形式

| 形式 | 目的 | 入口 |
| --- | --- | --- |
| Docs サイト（日本語） | 学習導線。シナリオ → 失敗コード → 段階的改善 → 規約サマリの順で判断力に落とす | https://css-pro-max.h2cos.workers.dev |
| Agent Skill（英語） | AI エージェントに同じ判断基準を持たせる。各概念の唯一の正典 | `.cursor/skills/css-pro-max/` |

同一ルールを二つのフォーマットで提供しています。**正典は Skill 側 (`.cursor/skills/css-pro-max/references/*.md`)** で、docs サイトは同じ判断基準を学習向けに再構成したものです。ルール変更時は Skill 側を先に更新してください。

## Agent Skill として導入する

```bash
npx skills add https://github.com/hrdtbs/css-pro-max --skill css-pro-max
```

導入後、CSS / レイアウト / タイポグラフィ / アニメーション / A11y に関わる作業でこの Skill が自動適用されます。

## コントリビュート

ルール変更は正典 (`.cursor/skills/css-pro-max/references/<topic>.md`) を先に更新し、対応する docs ページ (`src/content/docs/references/<topic>.mdx`) を同一 PR で反映させてください。学習導線側だけを更新すると、Skill 利用時の判断基準と乖離します。
