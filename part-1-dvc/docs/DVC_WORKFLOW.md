# DVC Data Versioning Workflow Documentation

## 1. Overview of Data Version Control (DVC)

Traditional Git repositories are designed for source code (lightweight text files). Tracking large binary files or datasets directly in Git leads to bloated repositories, slow clone operations, and repository size limit violations.

**DVC (Data Version Control)** solves this problem by separating:
1. **The Data Itself:** Stored in a remote storage system or local cache (content-addressable storage).
2. **The Metadata (`.dvc` pointer files):** Small text files containing the file's MD5 checksum, file path, and size, which are committed directly to Git.

---

## 2. Content-Addressable Storage (CAS) & MD5 Hashing

When you run `dvc add <path/to/data>`, DVC performs the following:
1. Calculates the **MD5 hash** of the file contents.
2. Creates an entry in the DVC cache (by default inside `.dvc/cache/`).
3. Uses a 2-level directory structure based on the MD5 hash:
   ```
   .dvc/cache/files/md5/<first-2-chars>/<remaining-30-chars>
   ```
   *Example:* If the MD5 hash is `a1b2c3d4e5f6...`, the cached file is stored at:
   ```
   .dvc/cache/files/md5/a1/b2c3d4e5f6...
   ```
4. Generates a `.dvc` pointer file (e.g., `data/raw/dataset_v1.csv.dvc`) containing:
   ```yaml
   outs:
   - md5: a1b2c3d4e5f67890abcdef1234567890
     size: 14250
     hash: md5
     path: dataset_v1.csv
   ```
5. Appends the original file (`dataset_v1.csv`) to `.gitignore` to prevent raw data from entering Git.

---

## 3. Remote Storage Architecture

DVC supports multiple remote storage backends (AWS S3, Google Cloud Storage, Azure Blob, SSH, and Local Filesystem). In exam and local laboratory environments, a local folder remote is used.

### Configuring a Local Remote
```cmd
:: Create a dedicated remote storage directory in the user profile
mkdir "%USERPROFILE%\dvc-remote-storage"

:: Add the remote to DVC configuration
dvc remote add -d myremote "%USERPROFILE%\dvc-remote-storage"
```
The `-d` flag sets `myremote` as the default remote for all push/pull operations.

---

## 4. The Complete DVC + Git Lifecycle Cycle

```
[Raw Data] ---> `dvc add` ---> [.dvc Cache / MD5 Hash]
     |                                    |
     v                                    v
[.dvc Pointer File]                 `dvc push`
     |                                    |
     v                                    v
[Git Staging & Commit]            [Remote Storage]
```

### Step-by-Step Lifecycle:
1. **Generate or update data:**
   ```cmd
   python src/generate_data.py
   ```
2. **Track data with DVC:**
   ```cmd
   dvc add data/raw/dataset_v1.csv
   ```
3. **Commit the `.dvc` pointer file to Git:**
   ```cmd
   git add data/raw/dataset_v1.csv.dvc data/raw/.gitignore .gitignore
   git commit -m "feat(data): track version 1 of raw dataset"
   ```
4. **Push data to remote storage:**
   ```cmd
   dvc push
   ```

---

## 5. Version Comparison (`dvc diff`)

When data changes (e.g., via `python src/augment_data.py`), DVC can inspect changes before or after tracking:
```cmd
:: Check data status compared to current .dvc pointer
dvc status

:: Compare workspace data against a specific Git commit or branch
dvc diff
dvc diff HEAD~1
```

`dvc diff` displays:
- Modified files
- Hash differences
- Size differences (bytes added or removed)

---

## 6. Historical Version Restoration (`git checkout` + `dvc checkout`)

To revert data to a historical version:
1. **Switch Git commit/branch to the desired point in time:**
   ```cmd
   git checkout <commit_hash> -- data/raw/dataset_v1.csv.dvc
   ```
2. **Sync the working data directory with the checked-out `.dvc` pointer:**
   ```cmd
   dvc checkout
   ```
DVC immediately swaps the working file with the cached version matching the historical MD5 hash without needing to download or re-generate data.
