import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# .env 読み込み
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

# PDF をアップロード
uploaded_file = client.files.upload(
    file="2511.14383v1.pdf",
    config=types.UploadFileConfig(
        display_name="miyawaki_paper",
    ),
)

print("Uploaded URI:", uploaded_file.uri)

# アップロードしたファイルを参照して質問
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
