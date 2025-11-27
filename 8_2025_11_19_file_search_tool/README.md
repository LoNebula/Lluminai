# 📁 Gemini File Search Tool — Multi-PDF Retrieval & Summarization Demo

このリポジトリは、**Google Gemini API の File Search Tool（File Search Store）** を用いて、
複数の PDF をアップロードし、モデル自身に **検索 → 統合 → 要約** を行わせるデモプロジェクトです。

ブログ記事
**「Gemini APIのFile Search Toolを実際に触ってみた」**
で紹介したサンプルコードをそのまま再現し、複数PDFに対して横断的な検索ができる最小構成になっています。

---

## 🚀 概要

Google Gemini の **File Search Tool** は、PDF や画像などをアップロードすると：

1. **自動的にインデックスを生成（内部で RAG を構築）**
2. **モデルが対話中に「必要な箇所だけ」検索**
3. **引用つきで回答を生成**

というフローをすべて自動で行います。

つまりこのデモだけで、**RAG 構築なしの「文書検索エージェント」** を体験できます。

---

## 🧩 このリポジトリでできること

* 複数 PDF を **File Search Store** にアップロード
* Gemini が **必要箇所だけ検索して要約**
* 文書をまたぐ **横断的な要点抽出**
* 引用情報（grounding）を含む回答の取得

---

## 📦 ディレクトリ構成

```
.
├── main.py                         # メインコード（File Search Store & Multi-PDF検索）
├── documents/
│   ├── 2511.20547v1.pdf            # サンプルPDF（論文）
│   ├── 2511.20604v1.pdf            # サンプルPDF（論文）
│   └── 2511.20639v1.pdf            # サンプルPDF（論文）
└── README.md
```

---

## 🔧 動作環境

* Python 3.10+
* `google-genai` SDK
* `.env` に Google API Key を設定

---

## 🛠 セットアップ手順

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

## 🧠 実際に何が起きるのか？

`main.py`（実装: ）では次の処理が実行されます：

1. **File Search Store を作成**
2. `documents/` 配下の PDF を MIME 判定しつつ Store にアップロード
3. Gemini 2.5 Pro に検索ツール（File Search）を渡す
4. モデルが **3つの論文を横断的に検索**
5. すべての PDF を統合した要約が出力される

実際のログ例：

```
Created store: fileSearchStores/projectdocs-xxxx
Uploading: documents/2511.20547v1.pdf (application/pdf)
Uploading: documents/2511.20604v1.pdf (application/pdf)
Uploading: documents/2511.20639v1.pdf (application/pdf)
All files uploaded & indexed.

=== AI Summary ===

（3つのPDFを横断した統合要約がここに表示）
```

Gemini は PDF 全体を読み込むのではなく、**質問に応じて必要部分だけ検索**して回答します。
これにより、複数ファイルを扱う場合でも高速な応答が可能です。

---

## 📘 使用している PDF について

このデモでは、以下の PDF を使用しています：

* *From Words to Wisdom: Discourse Annotation and Baseline Models for Student Dialogue Understanding*（2025）
* *On Evaluating LLM Alignment by Evaluating LLMs as Judges*（2025）
* *Latent Collaboration in Multi-Agent Systems*（2025）

これらの PDF はすべて `documents/` フォルダに置かれており、
File Search Store にアップロードされます。

---