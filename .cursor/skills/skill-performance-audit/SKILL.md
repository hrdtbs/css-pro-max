---

## name: skill-performance-audit
description: 定期的にAgent Skillの性能評価を実行し、静的品質スコアとトリガー精度を比較レポート化する。Use when the user asks to evaluate skills regularly, benchmark trigger accuracy, run recurring skill audits, or compare current vs previous skill performance.

# Skill Performance Audit

このスキルは、Agent Skill の定期検査を再現可能な形で実行するための運用スキルです。
目的は「単発レビュー」ではなく、同じ手順で繰り返し測定し、改善/劣化を追跡することです。

## When to use

- 「この検査を定期的に回したい」
- 「毎週/毎月スキル性能をチェックしたい」
- 「前回と比べて発火率が落ちていないか見たい」
- 「description変更の影響をベンチマークしたい」

## Required outputs

実行ごとに以下を作成すること。

- `evals/skills/<skill-name>/<YYYY-MM-DD>/judge-report.md`
- `evals/skills/<skill-name>/<YYYY-MM-DD>/trigger-eval.json`
- `evals/skills/<skill-name>/<YYYY-MM-DD>/iter-0/results.json`
- `evals/skills/<skill-name>/<YYYY-MM-DD>/iter-0/metrics.json`
- `evals/skills/<skill-name>/<YYYY-MM-DD>/evaluation-report.md`

改善案を再計測した場合は `iter-1/` 以降も同様に作る。

## Audit workflow

1. **Resolve target**
  - 対象スキルの `SKILL.md` パスを確定する。
  - 未指定なら `AskQuestion` で選択させる。
2. **Create run directory**
  - 日付ディレクトリを作成する。
  - 既存 run がある場合は `run-2`, `run-3` を追加して衝突回避する。
3. **Static review (120-point rubric)**
  - `skill-judge` の8次元で採点し、根拠付きで `judge-report.md` を作る。
  - 最低限、D1/D4/D5 を明示評価する。
4. **Build trigger eval set**
  - `references/eval-query-guidelines.md` の配分に従い、20件作成する。
  - `should_trigger: true 10件 / false 10件` を必ず維持する。
  - 抽象ケースとニアミスを混ぜる。
5. **Run trigger benchmark (baseline)**
  - `generalPurpose` subagent を readonly で使い、3 trials 実行する。
  - 各 trial は20件すべてに `would_trigger` を返す JSON のみを出力。
  - `iter-0/results.json` にまとめる。
6. **Compute metrics**
  - `scripts/compute_trigger_metrics.py` を実行して `iter-0/metrics.json` を作る。
  - 指標: recall / specificity / balanced_score / agreement_mean。
7. **Optional retest**
  - false positive / false negative がある場合のみ description 改善案を作る。
  - `iter-1` で再計測し、before/after を比較する。
  - 改善不要なら skip してよい。
8. **Consolidate report**
  - `evaluation-report.md` を作成。
  - 必須項目:
    - static score
    - trigger metrics
    - 前回 run との差分
    - 優先度付き改善チケット (P1/P2/P3)

## Comparison rule (periodic operation)

定期運用時は、同一スキルの直近 run と比較する。

- 比較対象: `evals/skills/<skill-name>/` 配下の最新2 run
- 比較観点:
  - `judge score` の増減
  - `balanced_score` の増減
  - `specificity` 低下（誤発火増）を優先警戒
- レポートに `Regression Check` セクションを必ず入れる。

## Subagent prompt contract

トリガー判定に使うサブエージェントには以下契約を必ず指定する。

- 入力: `trigger-eval.json` + 対象スキル description
- 出力: JSON only
- 形式:

```json
{
  "trial": 1,
  "results": [
    {
      "id": "p01",
      "should_trigger": true,
      "would_trigger": true,
      "reason": "brief reason"
    }
  ]
}
```

## Guardrails

- ユーザー指示がない限り、対象スキル本体 (`SKILL.md`) は編集しない。
- 評価クエリは毎回コピーせず、対象ドメインに合わせて更新する。
- `should_trigger` ラベルは実行前にユーザー確認を取る。
- 結果が満点でも、境界条件の弱さ（将来の誤発火リスク）を記述する。

## Quick run checklist

- 対象スキル確定
- runディレクトリ作成
- `judge-report.md` 作成
- `trigger-eval.json` 作成
- 3 trials 実行
- `metrics.json` 生成
- 前回比較
- `evaluation-report.md` 作成

