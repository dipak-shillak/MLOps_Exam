import os
import sys
from pathlib import Path

# Add parent directory to path to import dataset_loader
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dataset_loader import get_dataset, DATASET_NAME

def generate_v1():
    print(f"[DVC Stage: Generate Data] Loading active dataset: '{DATASET_NAME}'...")
    df, feature_cols, target_col = get_dataset()
    
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "dataset_v1.csv"
    
    df.to_csv(output_file, index=False)
    
    print(f"Successfully generated Version 1 dataset at: {output_file}")
    print(f"Dataset Name: {DATASET_NAME}")
    print(f"Total Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)} ({len(feature_cols)} features + target '{target_col}')")
    print(f"Preview (first 2 rows):\n{df.head(2)}")

if __name__ == "__main__":
    generate_v1()
