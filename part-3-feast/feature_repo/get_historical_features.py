import os
import pandas as pd
from feast import FeatureStore

def main():
    store = FeatureStore(repo_path=".")
    parquet_path = os.path.join("data", "features.parquet")
    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"'{parquet_path}' does not exist. Run setup_feature_store.py first.")

    features_df = pd.read_parquet(parquet_path)
    entity_df = features_df[["sample_id", "event_timestamp"]].copy()

    service = store.get_feature_service("exam_feature_service")
    training_data = store.get_historical_features(
        entity_df=entity_df,
        features=service,
    ).to_df()

    print(f"[get_historical_features] Retrieved point-in-time correct historical training dataset.")
    print(f"[get_historical_features] Shape: {training_data.shape}")
    print("[get_historical_features] First 3 rows:")
    print(training_data.head(3).to_string())

if __name__ == "__main__":
    main()
