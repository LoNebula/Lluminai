import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report

class CanineEmotionClassifier:
    def __init__(self):
        # 論文でベストスコアを出したExtraTreesを採用
        self.classifier = ExtraTreesClassifier(
            n_estimators=100,
            criterion='gini',
            random_state=42
        )
        # 特徴量選択用のRandomForest
        self.selector = SelectFromModel(
            estimator=RandomForestClassifier(n_estimators=100, random_state=42),
            threshold="mean" # 平均以上の重要度を持つ特徴のみ残す
        )

    def synchronize_data(self, visual_df, inertial_df, physio_df):
        """
        [Multimodal Convergence]
        異なるサンプリングレートのデータを結合します。
        論文ではWindowing後の統計量を使っていますが、ここでは
        最も粗い粒度（生理データ: 1Hz）に合わせてリサンプリングする例を示します。
        """
        print("🔄 Synchronizing multimodal data...")
        
        # 1秒ごとのタイムラインに合わせる (Physiological Dataベース)
        # visual (30fps) -> 平均化
        vis_resampled = visual_df.resample('1S').mean().add_suffix('_vis')
        
        # inertial (252Hz) -> 平均化 (実際はTSFEL等で高度な特徴抽出を行う)
        iner_resampled = inertial_df.resample('1S').mean().add_suffix('_inert')
        
        # physio (1Hz) -> そのまま
        phys_resampled = physio_df.resample('1S').mean().add_suffix('_phys')

        # 結合 (Inner Joinで欠損時間を除外)
        multimodal_df = pd.concat(
            [vis_resampled, iner_resampled, phys_resampled], 
            axis=1, 
            join='inner'
        )
        
        print(f"✅ Data merged. Shape: {multimodal_df.shape}")
        return multimodal_df

    def select_features(self, X, y):
        """
        [Feature Selection]
        320次元の特徴量から、本当に効くものだけを選抜します。
        """
        print("📉 Selecting important features...")
        self.selector.fit(X, y)
        
        X_new = self.selector.transform(X)
        selected_indices = self.selector.get_support(indices=True)
        
        # 選ばれた特徴量の名前などを確認可能
        print(f"✅ Features reduced: {X.shape[1]} -> {X_new.shape[1]}")
        return X_new

    def train_and_evaluate(self, X, y):
        """
        [Classification & Results]
        Stratified 5-fold CVで評価を行います。
        """
        print("🚀 Starting training with ExtraTrees...")
        
        # 5-fold Cross Validation
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        # F1スコアで評価
        scores = cross_val_score(self.classifier, X, y, cv=cv, scoring='f1_macro')
        
        print("-" * 30)
        print(f"🏆 Average F1-Score: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
        print("-" * 30)
        
        return scores

# --- 実行フロー ---

if __name__ == "__main__":
    # 1. ダミーデータの生成 (本来はCSVからロード)
    # 時間インデックスを作成
    time_idx = pd.date_range(start="2025-01-01", periods=300, freq='S') # 300秒分
    
    # 視覚特徴量 (例: キーポイント座標など180次元)
    df_visual = pd.DataFrame(
        np.random.rand(300, 180), index=time_idx
    )
    
    # 慣性特徴量 (例: 加速度統計量など40次元)
    df_inertial = pd.DataFrame(
        np.random.rand(300, 40), index=time_idx
    )
    
    # 生理特徴量 (例: 体温・心拍統計量など20次元)
    df_physio = pd.DataFrame(
        np.random.rand(300, 20), index=time_idx
    )
    
    # 正解ラベル (4クラス)
    labels = np.random.choice(
        ['Toy', 'Petting', 'Frustration', 'Abandonment'], 
        size=300
    )
    
    # 2. パイプライン実行
    pipeline = CanineEmotionClassifier()
    
    # データ統合
    X_df = pipeline.synchronize_data(df_visual, df_inertial, df_physio)
    y = labels[:len(X_df)] # 長さを合わせる
    
    # 特徴量選択
    X_selected = pipeline.select_features(X_df.values, y)
    
    # 学習と評価
    pipeline.train_and_evaluate(X_selected, y)