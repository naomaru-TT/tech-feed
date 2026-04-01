# IT News Hub — テックフィード

クラウド・AI・インフラ系のITニュースを自動集約するGitHub Pages サイトです。

🌐 **サイトURL**: https://naomaru-tt.github.io/tech-feed/

## 収集ソース

| ソース | タグ | 更新 |
|---|---|---|
| AWS 公式ブログ（日本語） | AWS | 3時間ごと |
| Zenn（AWS / Kubernetes / インフラ） | Zenn | 3時間ごと |
| Google Cloud リリースノート | GCP | 3時間ごと |
| Azure Updates | Azure | 3時間ごと |
| Hacker News（クラウド・インフラ関連） | HN | 3時間ごと |
| The New Stack | インフラ | 3時間ごと |
| OpenAI Blog | AI | 3時間ごと |
| Anthropic News | AI | 3時間ごと |
| Google AI Blog | AI | 3時間ごと |

## セットアップ

### 1. リポジトリを作成

GitHub で新しいパブリックリポジトリを作成し、このファイル一式をプッシュします。

```
your-repo/
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

Actions タブから `Update IT News` を手動実行 (`workflow_dispatch`) して `docs/news.json` が生成されることを確認します。

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
| v1.0.0 | 2026-04-01 | 初回リリース。AWS・Zenn・GCP・Azure・HN・AI系フィード対応、3時間ごと自動更新 |
