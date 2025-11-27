import streamlit as st
import requests

st.title("🚀 LLM モデル自動切替 UI（FastAPI × OpenAI）")

API_URL = "http://127.0.0.1:8000/inference"

# タスク選択
task = st.selectbox(
    "タスクを選択してください：",
    ["chat", "summarize", "classify", "reasoning"]
)

# プロンプト入力
prompt = st.text_area("プロンプトを入力してください：", height=150)

# 送信ボタン
if st.button("実行する"):
    if not prompt.strip():
        st.warning("プロンプトを入力してください")
    else:
        with st.spinner("推論中..."):
            payload = {"task": task, "prompt": prompt}
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                st.success(f"使用モデル：{data['model_used']}")
                st.write("### 🔽 出力結果")
                st.write(data["output"])
            else:
                st.error(f"エラーが発生しました: {response.text}")
