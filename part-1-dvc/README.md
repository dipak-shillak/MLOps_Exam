# Part 1: Data Versioning Using DVC

## 1. Overview & Learning Objectives
This module provides hands-on mastery of **Data Version Control (DVC)** for machine learning data management:
- Initializing and configuring DVC with a dedicated local remote storage.
- Tracking and versioning datasets using content-addressable storage (MD5 checksum hashing).
- Managing remote storage and synchronizing datasets with `dvc push` and `dvc pull`.
- Detecting and comparing data changes across versions with `dvc diff`.
- Restoring historical data snapshots using `dvc checkout`.

---

## 2. Git Submission Workflow (For Group Exam Repo)
> **NOTE:** Do NOT run `git init` inside this directory during local practice. Git repository management occurs in your team's cloned exam repo.

1. Clone group exam repo: `git clone https://github.com/<owner>/MLOps-Practical-Exam.git` and `cd MLOps-Practical-Exam`
2. Sync `main`: `git switch main` then `git pull origin main`
3. Create feature branch: `git switch -c part-1-dvc`
4. Copy the entire `part-1-dvc/` folder contents into the cloned repository.
5. Execute the verification steps below, stage changes (`git add .`), commit (`git commit -m "feat(dvc): complete data versioning workflow"`), push (`git push -u origin part-1-dvc`), and create a Pull Request into `main`.

---

## 3. Step-by-Step Execution Guide (`cmd.exe`)

Open Windows Command Prompt (`cmd.exe`) and navigate into `part-1-dvc`:
```cmd
cd "c:\Users\PRATIK\Desktop\Aaditya Patil\MLops_Practical\part-1-dvc"
```

### Step 3.1: Activate Virtual Environment
Activate the `.venv-base` environment:
```cmd
call ..\envs\.venv-base\Scripts\activate.bat
```

### Step 3.2: Configure Runtime Dataset (Optional)
Open `dataset_loader.py` and set `DATASET_NAME` to the examiner's assigned dataset:
```python
# Options: "wine" (default), "breast_cancer", or "digits"
DATASET_NAME = "wine"
```
Verify the dataset loader:
```cmd
python dataset_loader.py
```

### Step 3.3: Initialize DVC
If working inside a cloned Git repository:
```cmd
dvc init #do not run
```
*(If testing standalone outside of a Git repository, initialize with `--no-scm`:)*
```cmd
dvc init --no-scm
```

### Step 3.4: Configure Local Remote Storage
Set up a local storage folder in `%USERPROFILE%\dvc-remote-storage`:
```cmd
if not exist "%USERPROFILE%\dvc-remote-storage" mkdir "%USERPROFILE%\dvc-remote-storage"
dvc remote add -d myremote "%USERPROFILE%\dvc-remote-storage"
dvc remote list
```

### Step 3.5: Generate Version 1 of Dataset & Track
```cmd
python src/generate_data.py
```
Track the generated raw dataset with DVC:
```cmd
dvc add data/raw/dataset_v1.csv
```
This generates `data/raw/dataset_v1.csv.dvc` and updates `.gitignore`.
Push Version 1 data to remote storage:
```cmd
dvc push
```

### Step 3.6: Augment Dataset to Version 2 & Push
Augment the dataset by sampling 20 rows and adding Gaussian noise:
```cmd
python src/augment_data.py
```
Inspect DVC status:
```cmd
dvc status
```
Track Version 2:
```cmd
dvc add data/raw/dataset_v1.csv
dvc push
```

### Step 3.7: Compare Versions with `dvc diff`
Compare the data versions:
```cmd
dvc diff
```
View detailed metadata inside the pointer file:
```cmd
type data\raw\dataset_v1.csv.dvc
```

### Step 3.8: Restore Historical Version 1
To demonstrate rollback, restore an earlier version:
```cmd
:: If in Git, checkout the earlier .dvc file, then run:
dvc checkout
```
Confirm the restored dataset row count matches Version 1:
```cmd
python -c "import pandas as pd; df=pd.read_csv('data/raw/dataset_v1.csv'); print('Current row count:', len(df))"
```

---

## 4. Reset to Initial Clean State

To wipe all generated data, cache, and DVC metadata before a new test run or dataset switch, run:
```cmd
if exist "data\raw\dataset_v1.csv" del /q /f "data\raw\dataset_v1.csv"


if exist "data\raw\.gitignore" del /q /f "data\raw\.gitignore"
if exist ".dvc" rmdir /s /q ".dvc"
if exist ".dvcignore" del /q /f ".dvcignore"
if exist "dvc.lock" del /q /f "dvc.lock"
```
