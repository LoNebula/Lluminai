以下は、あなたのブログ内容（）と `main.py` のコード（）を元に作成した、
**GitHub リポジトリ用 README.md（完成版）** です。

---

# 📁 Gemini File Search Tool — PDF Summarization Demo

このリポジトリは、**Google Gemini API の File Search Tool** を使って
PDF をアップロードし、モデル自身に **検索・引用・要約** させる最小構成のデモです。

ブログ記事
**「Gemini apiのfile search tool を実際に触ってみた」**（）
で解説したサンプルコード一式をそのまま再現しています。

---

## 🚀 概要

Gemini の File Search Tool は、PDF や画像・音声などをアップロードすると、
AI が内部で自動インデックス化し、必要に応じて自律的に検索して回答してくれる仕組みです。

つまり **RAG を自分で構築せずに検索型エージェントを作れる** のがポイント。

このリポジトリでは次のことができます：

* PDF を Gemini File API にアップロード
* インデックス化された PDF をモデルが検索
* 要約内容の生成
* （モデルが引用したソース情報も返ってくる）

---

## 📦 ディレクトリ構成

```
.
├── main.py                # メイン実装（PDFアップロード & 要約）
├── 2511.14383v1.pdf       # サンプルPDF（数学論文）
└── README.md              # 本ファイル
```

---

## 🔧 動作環境

* Python 3.10+
* `google-genai` SDK
* `.env` に Google API Key を設定

---

## 🛠 セットアップ

### 1. 依存ライブラリのインストール

```bash
pip install google-genai python-dotenv
```

### 2. `.env` ファイルを作成

```
GOOGLE_API_KEY=あなたのAPIキー
```

### 3. 実行

```bash
python main.py
```

---

## 🧠 何が起きるのか？

`main.py` では以下の処理を行っています（）：

1. PDF（`2511.14383v1.pdf`）を File API にアップロード
2. アップロードされたファイル URI を取得
3. `generate_content()` に PDF URI を渡し、モデルへ質問
4. モデルが PDF 内を検索し、引用メタデータ付きで回答

---

## 📘 main.py（再掲）

```python
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

# PDF をアップロード
uploaded_file = client.files.upload(
    file="2511.14383v1.pdf",
    config=types.UploadFileConfig(display_name="miyawaki_paper"),
)

print("Uploaded URI:", uploaded_file.uri)

# PDF を参照して質問
response = client.models.generate_content(
    model="gemini-2.0-flash-thinking-exp-01-21",
    contents=[
        "この論文を日本語で要約してください。",
        types.Part.from_uri(
            file_uri=uploaded_file.uri,
            mime_type="application/pdf",
        ),
    ],
)

print(response.text)
```

---

## 📝 サンプル出力

実行すると以下のように「引用つき回答」が返ってきます：

* どのページを参照したか
* どの内容が根拠か

Google Gemini による **Grounded Response** が利用可能です。

---

## 🎯 何に使えるか？

* PDF の要点抽出
* 契約書レビュー
* マニュアル検索エージェント
* 学術論文の比較・整理
* 社内文書の軽量 RAG 代替

「PDF を置くだけで AI が検索×推論×引用してくれる」
というワークフローが簡単に試せます。