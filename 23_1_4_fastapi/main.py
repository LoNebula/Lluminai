from fastapi import FastAPI, HTTPException, status, Query, Path, Depends, Form, File, UploadFile, Cookie, Header, Request, BackgroundTasks, WebSocket
import time
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from contextlib import asynccontextmanager
# from routers import users

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}

# @app.get("/items/")
# def read_items(skip: int = 0, limit: int = 10):
#     return {"skip": skip, "limit": limit}

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool | None = None

# @app.post("/items/")
# def create_item(item: Item):
#     return item

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item, q: str | None = None):
#     return {"item_id": item_id, "q": q, **item.model_dump()}\

# @app.get("/items/")
# def read_items(
#     q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
#     item_id: Annotated[int, Path(ge=1, le=1000)] = ..., # 1以上1000以下
# ):
#     return {"q": q, "item_id": item_id}

# # 1. 入力用モデル（パスワードが必要）
# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: str

# # 2. 出力用モデル（パスワードを除外）
# class UserOut(BaseModel):
#     username: str
#     email: str

# # response_model に「出力用」を指定する
# @app.post("/user/", response_model=UserOut)
# def create_user(user: UserIn):
#     # user は UserIn 型なので password を持っている
#     print(f"DBに保存: {user.password}") 
    
#     # そのまま user オブジェクトを返しても、
#     # FastAPIが UserOut の形に自動でフィルタリング（不要な項目を削除）して返却する
#     return user

# @app.post("/items/", status_code=status.HTTP_201_CREATED)
# def create_item(name: str):
#     return {"name": name}

# @app.get("/items/{item_id}")
# def read_item(item_id: str):
#     if item_id == "not_found":
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"item": item_id}

# async def common_params(q: str | None = None, limit: int = 100):
#     return {"q": q, "limit": limit}

# @app.get("/items/")
# def read_items(commons: Annotated[dict, Depends(common_params)]):
#     return commons


# class CommonQueryParams:
#     def __init__(self, q: str | None = None, limit: int = 100):
#         self.q = q
#         self.limit = limit

# @app.get("/items/")
# def read_items(commons: Annotated[CommonQueryParams, Depends()]):
#     return commons

# app.include_router(users.router)

# @app.post("/login/")
# def login(username: str = Form(), password: str = Form()):
#     return {"username": username}

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     content = await file.read()
#     return {"filename": file.filename, "size": len(content)}

# @app.get("/items/")
# def read_items(
#     ads_id: Annotated[str | None, Cookie()] = None,
#     user_agent: Annotated[str | None, Header()] = None,
# ):
#     return {"ads_id": ads_id, "User-Agent": user_agent}

# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str

# # 依存性注入でセッションを渡すのが一般的
# def get_session():
#     with Session(engine) as session:
#         yield session

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# @app.get("/users/me")
# def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

# def write_log(message: str):
#     with open("log.txt", "a") as log:
#         log.write(message)

# @app.post("/send-notification/")
# async def send_notification(email: str, background_tasks: BackgroundTasks):
#     background_tasks.add_task(write_log, f"email sent to {email}")
#     return {"message": "Notification sent"}

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")

# client = TestClient(app)

# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World"}

# app.mount("/static", StaticFiles(directory="static"), name="static")

# class Settings(BaseSettings):
#     app_name: str = "Awesome API"
#     admin_email: str
#     items_per_user: int = 50
#     # 環境変数がない場合のデフォルト値を設定するか、型ヒントで必須にする

#     # .env ファイルを読み込む設定
#     model_config = SettingsConfigDict(env_file=".env")

# # lru_cacheを使うことで、設定ファイルの読み込みを一度だけに抑える
# @lru_cache
# def get_settings():
#     return Settings()

# @app.get("/info")
# def get_info(settings: Annotated[Settings, Depends(get_settings)]):
#     return {
#         "app_name": settings.app_name,
#         "admin_email": settings.admin_email,
#     }

# # グローバル変数としてモデルを保持する辞書
# ml_models = {}

# def load_heavy_model():
#     # 本来はここでPyTorchやTensorFlowのモデルをロード
#     return "This represents a loaded ML model"

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # --- 起動時の処理 ---
#     print("Loading ML models...")
#     ml_models["answer_bot"] = load_heavy_model()
    
#     yield # ここでアプリケーションが稼働し続ける
    
#     # --- 終了時の処理 ---
#     print("Cleaning up resources...")
#     ml_models.clear()

# app = FastAPI(lifespan=lifespan)

# @app.get("/predict")
# async def predict(q: str):
#     model = ml_models["answer_bot"]
#     return {"query": q, "result": f"Predicted by {model}"}