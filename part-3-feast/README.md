# Part 3: Feature Store Implementation using Feast

This module demonstrates a complete feature store lifecycle using Feast: entity & feature view definitions, offline Parquet storage, materialization to an SQLite online store, point-in-time correct historical retrieval, and cross-model feature reuse.

---

## 1. Group Collaboration & Git Submission Workflow
> **Note:** Do NOT execute Git commands inside this prep workspace. Follow this workflow when merging into your group's shared repository:

1. Clone shared repo:
   ```cmd
   git clone https://github.com/<owner>/MLOps-Practical-Exam.git
   cd MLOps-Practical-Exam
   ```
2. Sync `main`:
   ```cmd
   git switch main
   git pull origin main
   ```
3. Create feature branch:
   ```cmd
   git switch -c part-3-feast
   ```
4. Copy this `part-3-feast` folder into the repository root, test it, commit and push:
   ```cmd
   git add .
   git commit -m "feat(feast): implement feature store with online and offline retrieval"
   git push -u origin part-3-feast
   ```
5. Open Pull Request on GitHub: `base: main` <- `compare: part-3-feast`.

---

## 2. Dataset Switching
Open `dataset_loader.py` and set the assigned dataset (line 5):
```python
DATASET_NAME = "wine"          # Options: "wine", "breast_cancer", "digits"
```

---

## 3. Step-by-Step Execution Guide (Windows `cmd.exe`)

Open `cmd.exe` and navigate to `part-3-feast\feature_repo`:
```cmd
cd /d c:\Users\dusan\OneDrive\Desktop\MLops_project\part-3-feast\feature_repo
..\..\envs\.venv-feast\Scripts\activate
```

### Step 3.1: Generate Offline Features & Feast Definitions
```cmd
python setup_feature_store.py
```
This writes `data\features.parquet` and dynamically generates `features.py`.

### Step 3.2: Register Features with Feast Registry
```cmd
feast apply
```

### Step 3.3: Verify Registered Catalog
```cmd
feast entities list
feast feature-views list
feast feature-services list
```

### Step 3.4: Materialize Features into SQLite Online Store
```cmd
python materialize.py
```
This loads feature records into `data\online_store.db`.

### Step 3.5: Test Low-Latency Online Feature Retrieval
```cmd
python get_online_features.py
```
Fetches live features for `sample_id` 0, 1, and 2 directly from SQLite.

### Step 3.6: Test Point-in-Time Correct Historical Retrieval
```cmd
python get_historical_features.py
```
Performs time-travel join to ensure no future data leakage.

### Step 3.7: Demonstrate Cross-Model Feature Reuse
```cmd
python reuse_features_clustering.py
```
Trains an unsupervised KMeans model reusing the identical `exam_feature_service`.

---

## 4. Reset to Initial Clean State
To wipe all generated data, Parquet files, SQLite databases, and dynamically generated feature definitions before a new test run or dataset change:
```cmd
cd /d c:\Users\dusan\OneDrive\Desktop\MLops_project\part-3-feast\feature_repo
if exist data rmdir /s /q data
if exist features.py del /q features.py
```
