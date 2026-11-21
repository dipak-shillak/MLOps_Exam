import os
import pandas as pd
from feast import FeatureStore
from sklearn.cluster import KMeans

def main():
    store = FeatureStore(repo_path=".")
    parquet_path = os.path.join("data", "features.parquet")
    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"'{parquet_path}' does not exist. Run setup_feature_store.py first.")

    features_df = pd.read_parquet(parquet_path)
    entity_df = features_df[["sample_id", "event_timestamp"]].copy()

    service = store.get_feature_service("exam_feature_service")
    retrieved_df = store.get_historical_features(
        entity_df=entity_df,
        features=service,
    ).to_df()

    feature_cols = [c for c in retrieved_df.columns if c not in ["sample_id", "event_timestamp", "target_label"]]
    X = retrieved_df[feature_cols].fillna(0)

    print(f"[reuse_features_clustering] Reusing '{service.name}' for unsupervised KMeans clustering.")
    print(f"[reuse_features_clustering] Features utilized ({len(feature_cols)}): {feature_cols[:5]}...")
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)
    cluster_counts = pd.Series(clusters).value_counts().sort_index().to_dict()

    print(f"[reuse_features_clustering] Clustering complete! Cluster distribution across {len(X)} samples:")
    for cluster_id, count in cluster_counts.items():
        print(f"  Cluster {cluster_id}: {count} samples")

if __name__ == "__main__":
    main()
