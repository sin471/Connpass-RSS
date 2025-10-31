# connpass-rss

connpass API を使用して、特定の都道府県のイベント情報を RSS フィードとして生成する Python プロジェクトです。

## 概要

このプロジェクトは、[connpass](https://connpass.com/) の公開 API からイベント情報を取得し、RSS フィード（`rss.xml`）として出力します。デフォルトでは愛知県のイベント情報を取得しますが、設定を変更することで他の都道府県にも対応できます。

## 主な機能

- connpass API からイベント情報を取得
- 今後開催されるイベントのみをフィルタリング
- RSS 2.0 形式でフィード生成
- イベントの詳細情報を含む：
  - タイトル
  - URL
  - 開催日時
  - 開催地（会場名・住所）
  - 説明文
  - イベント画像

## 必要要件

- Python 3.10 以上
- [uv](https://github.com/astral-sh/uv) (推奨)

## インストール

```bash
# リポジトリをクローン
git clone <your-repo-url>
cd connpass-rss

# uv を使用して依存関係をインストール
uv sync
```

## 環境変数の設定

connpass API キーが必要です。環境変数 `CONNPASS_API_KEY` に設定してください。

**Windows (PowerShell):**
```powershell
$env:CONNPASS_API_KEY="your-api-key-here"
uv run main.py
```

**Windows (コマンドプロンプト):**
```cmd
set CONNPASS_API_KEY=your-api-key-here
uv run main.py
```

**Linux/Mac (bash):**
```bash
export CONNPASS_API_KEY="your-api-key-here"
uv run main.py
```

## 使い方

### 基本的な使用方法

```bash
uv run main.py
```

実行すると、`rss.xml` ファイルが生成されます。

### カスタマイズ

`main.py` の `main()` 関数内で、以下の設定を変更できます：

```python
# 都道府県を変更
PREFECTURE_EN = "tokyo"  # 東京
PREFECTURE_JA = "東京"

# キーワード検索を追加
content = fetch_content(prefecture=PREFECTURE_EN, keyword=["Python", "AI"])
```

## プロジェクト構成

```
connpass-rss/
├── main.py           # メインスクリプト
├── pyproject.toml    # プロジェクト設定ファイル
├── README.md         # このファイル
└── rss.xml           # 生成される RSS フィード
```

## 依存パッケージ

- `feedgen>=1.0.0` - RSS フィード生成
- `requests>=2.32.5` - HTTP リクエスト

## API について

このプロジェクトは [connpass API v2](https://connpass.com/about/api/) を使用しています。

### 利用可能なパラメータ

- `prefecture` - 都道府県（例: "aichi", "tokyo"）
- `keyword` - 検索キーワードのリスト

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します！バグ報告や機能要望は Issue でお知らせください。
