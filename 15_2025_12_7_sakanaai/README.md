# 🧬 Evolutionary Model Merge Simulator (Toy Implementation)

Sakana AIが発表した論文 **"Evolutionary Optimization of Model Merging Recipes"** で提案されている「進化的モデルマージ」のアルゴリズムを、GPUなし（CPUのみ）で学習・体験するためのPythonシミュレータです。

大規模言語モデル（LLM）の実学習や推論評価を行う代わりに、**擬似的な評価関数（Mock Evaluation）**を用いることで、進化的アルゴリズムが「最適なマージ比率」を探索・収束させていく過程を数秒で再現します。

## 📦 特徴

* **GPU不要**: `numpy` だけで動作するため、どんなPCでも実行可能です。
* **高速な実験**: LLMのベンチマーク（数十分〜数時間）を擬似スコア計算（数ミリ秒）に置き換えています。
* **アルゴリズムの可視化**: ランダムな初期値からスタートし、世代を重ねるごとに「正解」へ近づく様子をログで確認できます。
* **拡張性**: 評価関数を差し替えることで、実際の `mergekit` と連携した本物の実験スクリプトへの改造も容易です。

## 🚀 インストール & 実行

### 必要要件
* Python 3.8+
* NumPy

### セットアップ
```bash
git clone [https://github.com/YOUR_USERNAME/evolutionary-merge-simulator.git](https://github.com/YOUR_USERNAME/evolutionary-merge-simulator.git)
cd evolutionary-merge-simulator
pip install numpy
```

### 実行

```bash
python evolution_merge_sim.py
```

実行すると、以下のようにコンソール上で「最適解」を探す旅が始まります。

```text
🧬 進化的マージシミュレーション開始
🎯 目標: 秘密の最適配合 [0.35 0.65 0.1  0.9 ] を探索する

Gen 1: Best Score = 42.15 | Params = [0.48 0.52 0.41 0.60]
Gen 2: Best Score = 55.30 | Params = [0.45 0.55 0.30 0.70]
...
Gen 13: Best Score = 99.12 | Params = [0.35 0.65 0.10 0.90]

🎉 最適解を発見しました！
```

## 🧠 コードの仕組み

このスクリプトは、主に以下の3つのパートで構成されています。

### 1\. `mock_evaluate_model(weights)`

実際のLLM開発における「モデルのマージ」と「ベンチマークテスト（MMLU, GSM8kなど）」をシミュレートする関数です。

  * **Input**: 4つのパラメータ（マージ比率など）
  * **Process**: 事前に定義された「正解（`TRUE_OPTIMAL_WEIGHTS`）」との距離を計算し、ノイズを加える。
  * **Output**: スコア（0〜100点）

### 2\. `SimpleEvolutionaryStrategy` クラス

生物の進化を模した探索アルゴリズム（CMA-ESの簡易版）です。

  * **評価**: 個体ごとのスコアを計算。
  * **選択（Selection）**: スコアの高いエリート個体を残す。
  * **交叉・変異（Mutation）**: エリート個体にランダムな変化を加え、次世代の候補を作る。

### 3\. メインループ

指定した世代数（Generations）だけ進化を繰り返し、最適解への収束を目指します。

## 🛠️ 実践への応用 (From Simulation to Reality)

このコードは「シミュレータ」ですが、`mock_evaluate_model` 関数の中身を書き換えることで、**本物のLLM自動マージツール**に進化させることができます。

```python
# 改造イメージ
import subprocess

def real_evaluate_model(weights):
    # 1. mergekit用のYAML設定ファイルを生成
    generate_yaml(weights)
    
    # 2. mergekitを実行してモデルを結合（GPU/CPUメモリが必要）
    subprocess.run(["mergekit-yaml", "config.yaml", "./output_model"])
    
    # 3. lm-evaluation-harness等でベンチマークを実行
    score = run_benchmark("./output_model")
    
    return score
```