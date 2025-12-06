# Modern Transformer Implementation (Llama Style) 🦙

GPT-2などの従来のTransformerではなく、**Llama 2/3 や Mistral などのSOTA（State-of-the-Art）モデルで採用されている「モダンなアーキテクチャ」** をPyTorchでフルスクラッチ実装したリポジトリです。

Zenn記事連載 **「LLM自作入門」Vol.2** の実証コードとして作成。

## 🚀 Key Features

現代のLLM開発における "デファクトスタンダード" となる以下の3つの技術要素を実装しています。

1.  **RMSNorm (Root Mean Square Layer Normalization)** ⚖️
    * 従来の `LayerNorm` (Mean & Variance) ではなく、二乗平均のみで正規化。
    * 計算コストを削減しつつ、深層学習の安定性を向上させます。
2.  **RoPE (Rotary Positional Embeddings)** 🌀
    * 絶対位置埋め込み（Absolute PE）を廃止し、複素数演算を用いた「回転」による相対位置埋め込みを採用。
    * 学習時よりも長いシーケンス長への外挿性能（Extrapolation）を理論的に保証します。
3.  **SwiGLU Activation** 🚪
    * `ReLU` や `GELU` ではなく、Gating機構を持つ `SiLU` ベースの活性化関数を採用。
    * パラメータ数は増加しますが、Scaling Lawsにおける学習効率が向上します。

## 🛠 Architecture Overview

本実装は **Decoder-only Transformer** であり、以下の構成を持ちます。

* **Pre-Normalization**: 各ブロックの入力側で正規化（学習の安定化）。
* **No Bias**: Linear層やNorm層からバイアス項を除去（Llama/PaLM流儀）。
* **Flash Attention Ready**: PyTorch 2.0+ の `F.scaled_dot_product_attention` を使用。

## 📦 Requirements

* Python 3.8+
* PyTorch 2.0+ (Required for Flash Attention & Complex Float support)

## 💻 Usage

### 1. Model Configuration
`ModelArgs` クラスでモデルのサイズを柔軟に定義できます。

```python
from model import ModelArgs, Transformer

# Configure the model (e.g., Mini Llama)
args = ModelArgs(
    dim=512,
    n_layers=8,
    n_heads=8,
    vocab_size=32000,
    max_seq_len=512,
    multiple_of=256
)

# Initialize
model = Transformer(args)
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
```

### 2\. Forward Pass (Inference)

トークンIDのバッチを入力として受け取り、Logitsを出力します。

```python
import torch

# Dummy input (Batch=2, Seq=128)
x = torch.randint(0, args.vocab_size, (2, 128))

# Forward pass
logits = model(x)
print(logits.shape) # torch.Size([2, 128, 32000])
```

## 📝 Code Structure

  * `RMSNorm`: 正規化層の実装 (`torch.rsqrt` 使用)
  * `precompute_freqs_cis` & `apply_rotary_emb`: RoPEの事前計算と適用ロジック（複素数演算）
  * `FeedForward`: SwiGLUを採用したFFN (Gate, Up, Down projections)
  * `Attention`: Multi-Head Attention (Flash Attention対応)
  * `TransformerBlock` & `Transformer`: 全体の組み立て
