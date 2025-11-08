# 1. ベースイメージの選択 (変更なし)
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# 2. タイムゾーンなどの設定（変更なし）
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# --- ↓↓ ここを修正 ↓↓ ---

# 3. 必要なパッケージのインストール (Python 3.11 と pip をインストール)
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
    python3.11 \
    python3.11-distutils \
    git \
    vim \
    curl \
    && curl -fsSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.11 get-pip.py \
    && rm get-pip.py \
    && rm -rf /var/lib/apt/lists/*

# --- ↑↑ ここまで修正 ↑↑ ---

# 4. Pythonライブラリのインストール (変更なし)
# PyTorchをCUDA 12.1対応版でインストールします
RUN pip3.11 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 5. Ollamaのインストール (変更なし)
RUN curl -fsSL https://ollama.com/install.sh | sh

# 6. 作業ディレクトリの指定 (変更なし)
WORKDIR /workspace

# 7. Ollamaが使用するポートを開放 (変更なし)
EXPOSE 11434

# 8. コンテナ起動時のデフォルトコマンド (変更なし)
CMD ["ollama", "serve"]