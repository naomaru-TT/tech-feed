# IT News Hub — テックフィード

クラウド・AI・インフラ系のITニュースを自動集約するGitHub Pages サイトです。

🌐 **サイトURL**: https://naomaru-tt.github.io/tech-feed/

## 収集ソース

| ソース | タグ | 更新頻度 |
|---|---|---|
| AWS 公式ブログ（日本語） | AWS | 3時間ごと |
| AWS What's New（日本語） | AWS | 3時間ごと |
| Zenn - AWS | AWS | 3時間ごと |
| Qiita - AWS | AWS | 3時間ごと |
| Zenn - 機械学習 | AI | 3時間ごと |
| Zenn - LLM | AI | 3時間ごと |
| Qiita - 機械学習 | AI | 3時間ごと |
| Qiita - ChatGPT | AI | 3時間ごと |
| ITmedia AI+ | AI | 3時間ごと |
| Zenn - Kubernetes | インフラ | 3時間ごと |
| Zenn - Terraform | インフラ | 3時間ごと |
| Zenn - Docker | インフラ | 3時間ごと |
| Qiita - インフラ | インフラ | 3時間ごと |
| Qiita - Kubernetes | インフラ | 3時間ごと |
| Google Cloud リリースノート | GCP | 3時間ごと |
| Zenn - GCP | GCP | 3時間ごと |
| ITmedia エンタープライズ | テック | 3時間ごと |
| Publickey | テック | 3時間ごと |

## セットアップ

### 1. リポジトリ構成

```
tech-feed/
├── .github/
│   └── workflows/
│       └── update-news.yml
├── docs/
│   └── index.html
├── scripts/
│   └── fetch_news.py
└── README.md
```

### 2. GitHub Pages を有効化

リポジトリの **Settings → Pages** を開き:
- Source: `Deploy from a branch`
- Branch: `main` / `docs` フォルダ

### 3. 動作確認

Actions タブから `最新のITニュース` を手動実行して `docs/news.json` が生成されることを確認します。

## カスタマイズ

`scripts/fetch_news.py` の `FEEDS` リストにRSSフィードのURLを追加・削除するだけでソースを変更できます。

更新頻度は `.github/workflows/update-news.yml` の `cron` 行を編集します。

```yaml
- cron: "0 */3 * * *"   # 3時間ごと → 毎時は "0 * * * *"
```

---

## 変更履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v1.1.0 | 2026-04-01 | ソースを日本語のみに絞り込み、AWS・AI・インフラ系を大幅追加（18ソース）。英語ソース（HN・The New Stack・Azure・英語AI系）を除外 |
| v1.0.0 | 2026-04-01 | 初回リリース。AWS・Zenn・GCP・Azure・HN・AI系フィード対応、3時間ごと自動更新 |
