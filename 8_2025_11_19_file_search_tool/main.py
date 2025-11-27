import os
import mimetypes
import dotenv
from google import genai
from google.genai import types

dotenv.load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 1. File Search Store を作成
store = client.file_search_stores.create(
    config={"display_name": "project_docs"}
)
print("Created store:", store.name)

folder = "Lluminai/Blog/8_2025_11_19_file_search_tool/documents"

# 2. Store にファイルをアップロード
for file in os.listdir(folder):
    path = os.path.join(folder, file)

    if os.path.isfile(path):

        # MIME タイプ判定
        mime, _ = mimetypes.guess_type(path)
        if mime is None:
            mime = "application/octet-stream"

        print(f"Uploading: {path} ({mime})")

        # === 新仕様に完全適合 ===
        op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=store.name,
            file=path,
            config=types.UploadToFileSearchStoreConfig(
                display_name=file,
                mime_type=mime
            )
        )

print("All files uploaded & indexed.")

# 3. File Search Tool を使って質問
response = client.models.generate_content(
    model="models/gemini-2.5-pro",
    contents="このフォルダー内の文書を横断して要点をまとめてください。",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[store.name]
                )
            )
        ]
    )
)

print("\n=== AI Summary ===\n")
print(response.text)
