# 🗺️ FastAPI 機能カタログ (FastAPI Features Catalog)

FastAPIの基本機能から、Pydantic V2によるバリデーション、依存性注入（DI）、そして実務で必須となる環境変数管理やLifespanイベントまでを網羅しています。

## 📋 Features

このリポジトリには、以下の実装が含まれています。

1. **Basic**: Hello World, Swagger UI
2. **Parameters**: Path, Query, Body, and Mixed params
3. **Validation**: `Annotated` combined with `Query`, `Path`
4. **Response Handling**: `response_model` filtering (Password hiding), Error handling
5. **Dependency Injection (DI)**: Function & Class dependencies
6. **Structure**: `APIRouter` usage
7. **IO**: Form data, File upload, Cookie, Header
8. **Database**: SQLModel / SQLAlchemy setup
9. **Security**: OAuth2 Password Bearer foundation, CORS
10. **Advanced**: Middleware, Background Tasks, WebSockets
11. **Operations**: Testing, Static Files
12. **Settings**: `pydantic-settings` implementation
13. **Lifespan**: ML Model loading pattern

## 🛠️ Requirement

* Python 3.10+
* FastAPI (Standard)
* Pydantic Settings
* SQLModel

## 🚀 Installation & Usage

### 1. クローンと仮想環境の作成

```bash
git clone https://github.com/LoNebula/Lluminai.git
cd 23_1_4_fastapi

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Mac/Linux
# .\venv\Scripts\activate  # Windows

```

### 2. 依存関係のインストール

```bash
pip install "fastapi[standard]" pydantic-settings sqlmodel httpx

```

### 3. 環境変数の設定 (.env)

プロジェクトルートに `.env` ファイルを作成します。

```env
APP_NAME="FastAPI Catalog"
ADMIN_EMAIL="admin@example.com"
ITEMS_PER_USER=50

```

### 4. サーバーの起動

開発モード（ホットリロード有効）で起動します。

```bash
fastapi dev main.py

```

* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 5. テストの実行

```bash
pytest

```

## 📂 Project Structure

```
.
├── main.py            # エントリーポイントと主要な実装
├── routers/           # ルーター分割のサンプル
│   └── users.py
├── static/            # 静的ファイル配信のサンプル
│   └── .gitkeep
├── .env               # 環境変数（Git対象外にするのが一般的ですがサンプルとして記載）
├── .gitignore
└── README.md

```

## 🧩 Key Concepts

### Lifespan Events (ML Model Loading)

`main.py` 内の以下のセクションでは、サーバー起動時の一度だけの重い処理（MLモデルのロードなど）をシミュレートしています。

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load models
    ml_models["answer_bot"] = load_heavy_model()
    yield
    # Shutdown: Clean up
    ml_models.clear()

```

### Settings Management

`pydantic-settings` を使用し、`.env` ファイルから型安全に設定を読み込んでいます。
