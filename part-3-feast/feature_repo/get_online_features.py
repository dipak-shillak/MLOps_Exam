from feast import FeatureStore
import pandas as pd

def main():
    store = FeatureStore(repo_path=".")
    entity_rows = [{"sample_id": 0}, {"sample_id": 1}, {"sample_id": 2}]
    service = store.get_feature_service("exam_feature_service")
    response = store.get_online_features(
        features=service,
        entity_rows=entity_rows,
    )
    df = response.to_df()
    print("[get_online_features] Successfully fetched online features from SQLite online store:")
    print(df.to_string())

if __name__ == "__main__":
    main()
