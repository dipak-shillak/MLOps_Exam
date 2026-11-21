# Feature Store Analysis & Production Architecture

## 1. Feature Store Overview
A Feature Store solves one of the most critical challenges in production machine learning: bridging the gap between batch feature engineering (for training) and low-latency feature retrieval (for real-time inference).

```
               +--------------------------------------------+
               |        Raw Data Sources (Parquet/DB)       |
               +---------------------+----------------------+
                                     |
                                     v
                       +-----------------------------+
                       |   Feast Feature Definitions |
                       | (Entities, Views, Services) |
                       +--------------+--------------+
                                      |
                 +--------------------+--------------------+
                 |                                         |
                 v (Offline Retrieval)                     v (Materialization)
    +--------------------------+              +--------------------------+
    |   Offline Feature Store  |              |   Online Feature Store   |
    | (Parquet / Data Lake)    |              | (Low-Latency SQLite/Redis|
    +-------------+------------+              +-------------+------------+
                  |                                         |
                  v                                         v
         Model Training                            Real-Time Inference
   (Point-in-Time Correct)                      (Sub-millisecond latency)
```

---

## 2. Key Architectural Pillars

### 2.1 Offline Store vs. Online Store
- **Offline Store (Parquet/Warehouse):**
  - Designed for high-throughput batch operations over large volumes of historical data.
  - Retains all timestamped historical events.
  - Used during model training, evaluation, and feature exploration.
- **Online Store (SQLite / Redis / DynamoDB):**
  - Key-value lookup optimized for single-entity or micro-batch low-latency retrieval.
  - Stores only the *latest* known feature values for each entity ID.
  - Used by inference services in production (APIs, microservices).

### 2.2 Point-in-Time Correctness (Time-Travel)
In production, features change continuously over time. If a model training pipeline joins future feature states with past labels, it introduces **data leakage** (also known as *lookahead bias* or *time-travel bug*).
- Feast performs **as-of point-in-time joins**: for every observation timestamp `T_obs` in `entity_df`, Feast retrieves the feature value valid at `T <= T_obs`.
- Future features are strictly excluded from the training dataset.

### 2.3 Elimination of Training-Serving Skew
Training-serving skew occurs when feature engineering code in training differs from the inference code (e.g. Pandas code in Python training vs. Java/Go implementation in production backend):
- In Feast, features are defined **once** in `features.py`.
- Both offline training (`get_historical_features`) and online inference (`get_online_features`) read from the identical feature definitions.
- Feature transformations and schema definitions are guaranteed to match 100%.

### 2.4 Cross-Model Feature Reusability via FeatureService
- Features defined in `raw_features_fv` and `engineered_features_fv` are grouped into `exam_feature_service`.
- Any team or model (e.g., supervised Random Forest classifier, unsupervised KMeans clusterer) can reuse the exact same features without rewriting any data pipelines.
