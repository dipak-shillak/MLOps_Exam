import os
import sys
from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np

# Ensure parent directory is in path to import dataset_loader
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dataset_loader import get_dataset, DATASET_NAME

def main():
    os.makedirs("data", exist_ok=True)
    df, feature_cols, target_col = get_dataset()
    print(f"[setup_feature_store] Preparing Feast store for dataset '{DATASET_NAME}'...")

    # Select base numeric features for interaction engineering
    numeric_cols = [c for c in feature_cols if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() > 1]
    if len(numeric_cols) < 2:
        numeric_cols = feature_cols[:2]

    col_a, col_b = numeric_cols[0], numeric_cols[1]
    print(f"[setup_feature_store] Generating interaction features from '{col_a}' and '{col_b}'")

    # Feature engineering
    df["feat_interaction_prod"] = (df[col_a] * df[col_b]).astype(float)
    df["feat_interaction_ratio"] = (df[col_a] / (df[col_b].abs() + 1e-5)).astype(float)
    eng_cols = ["feat_interaction_prod", "feat_interaction_ratio"]

    # Cast raw feature columns to float64 for Feast schema consistency
    for c in feature_cols:
        df[c] = df[c].astype(float)

    # Add sample_id entity key and timestamps
    df["sample_id"] = np.arange(len(df), dtype=np.int64)
    now = datetime.now(timezone.utc)
    # Give timestamps over the past 24 hours
    df["event_timestamp"] = [now - timedelta(hours=i % 24 + 1) for i in range(len(df))]
    df["created_timestamp"] = now

    parquet_path = os.path.join("data", "features.parquet")
    df.to_parquet(parquet_path, index=False)
    print(f"[setup_feature_store] Saved offline features parquet to '{parquet_path}' ({len(df)} rows)")

    # Dynamically generate features.py with accurate schema
    raw_fields = ",\n        ".join([f'Field(name="{c}", dtype=Float64)' for c in feature_cols])
    eng_fields = ",\n        ".join([f'Field(name="{c}", dtype=Float64)' for c in eng_cols])

    # Use forward slashes in path for cross-platform compatibility
    parquet_rel = "data/features.parquet"

    features_code = f'''# Dynamically generated Feast feature definitions for '{DATASET_NAME}'
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, FeatureService
from feast.types import Float64
from feast.value_type import ValueType

# Define Entity
sample_id = Entity(
    name="sample_id",
    join_keys=["sample_id"],
    value_type=ValueType.INT64,
    description="Unique identifier for each sample",
)

# FileSource pointing to offline Parquet data
source = FileSource(
    path="{parquet_rel}",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# FeatureView 1: Raw Features
raw_features_fv = FeatureView(
    name="raw_features_fv",
    entities=[sample_id],
    ttl=timedelta(days=365),
    schema=[
        {raw_fields}
    ],
    online=True,
    source=source,
)

# FeatureView 2: Engineered Features
engineered_features_fv = FeatureView(
    name="engineered_features_fv",
    entities=[sample_id],
    ttl=timedelta(days=365),
    schema=[
        {eng_fields}
    ],
    online=True,
    source=source,
)

# FeatureService bundling both feature views for cross-model reuse
exam_feature_service = FeatureService(
    name="exam_feature_service",
    features=[raw_features_fv, engineered_features_fv],
)
'''
    with open("features.py", "w", encoding="utf-8") as f:
        f.write(features_code)

    print("[setup_feature_store] Generated 'features.py' successfully.")

if __name__ == "__main__":
    main()
