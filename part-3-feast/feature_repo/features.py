# Dynamically generated Feast feature definitions for 'wine'
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
    path="data/features.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# FeatureView 1: Raw Features
raw_features_fv = FeatureView(
    name="raw_features_fv",
    entities=[sample_id],
    ttl=timedelta(days=365),
    schema=[
        Field(name="alcohol", dtype=Float64),
        Field(name="malic_acid", dtype=Float64),
        Field(name="ash", dtype=Float64),
        Field(name="alcalinity_of_ash", dtype=Float64),
        Field(name="magnesium", dtype=Float64),
        Field(name="total_phenols", dtype=Float64),
        Field(name="flavanoids", dtype=Float64),
        Field(name="nonflavanoid_phenols", dtype=Float64),
        Field(name="proanthocyanins", dtype=Float64),
        Field(name="color_intensity", dtype=Float64),
        Field(name="hue", dtype=Float64),
        Field(name="od280_od315_of_diluted_wines", dtype=Float64),
        Field(name="proline", dtype=Float64)
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
        Field(name="feat_interaction_prod", dtype=Float64),
        Field(name="feat_interaction_ratio", dtype=Float64)
    ],
    online=True,
    source=source,
)

# FeatureService bundling both feature views for cross-model reuse
exam_feature_service = FeatureService(
    name="exam_feature_service",
    features=[raw_features_fv, engineered_features_fv],
)
