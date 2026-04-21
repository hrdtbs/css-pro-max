# Trigger Eval Query Guidelines

定期検査で使う `trigger-eval.json` の品質を揃えるためのガイド。

## Required mix (20 total)

- Positive (`should_trigger: true`): 10
- Negative (`should_trigger: false`): 10

## Positive query design

- 4件: 直接要件（明確に対象ドメイン）
- 3件: 抽象相談（コード指定なし）
- 3件: 境界相談（近接ドメインだが対象に含む）

## Negative query design

- 4件: 明確に対象外
- 4件: ニアミス（用語は近いが別領域）
- 2件: 競合スキル想定（別スキルが優先されるべき）

## Writing rules

- 実際のユーザーが入力しそうな自然文にする。
- 一問一意で、複数テーマを混ぜない。
- 1件あたり1-3文で具体性を持たせる。
- 用語寄せだけの簡単判定問題にしない。

## Anti-patterns

- 「これは発火するはず」と分かりやすすぎるキーワード羅列
- negative が明白すぎて判別力を持たない
- 全件が同じ文体/同じ粒度で、多様性がない

## Quality gate before run

- 10/10 のラベル配分になっている
- 抽象ケースが positive に含まれている
- ニアミスが negative に含まれている
- クエリ重複がない