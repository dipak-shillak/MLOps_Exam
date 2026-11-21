import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add parent directory to path to import dataset_loader
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dataset_loader import DATASET_NAME

def augment_v2():
    input_file = Path("data/raw/dataset_v1.csv")
    if not input_file.exists():
        print(f"[ERROR] '{input_file}' not found. Please run 'python src/generate_data.py' first.")
        sys.exit(1)
        
    print(f"[DVC Stage: Augment Data] Reading base dataset from: {input_file}...")
    df = pd.read_csv(input_file)
    initial_rows = len(df)
    target_col = "target_label"
    
    # Identify numeric feature columns
    numeric_feature_cols = [
        c for c in df.columns 
        if c != target_col and pd.api.types.is_numeric_dtype(df[c])
    ]
    
    print(f"Original row count: {initial_rows}")
    print(f"Sampling 20 random rows (random_state=42) and adding Gaussian noise N(0, 0.05)...")
    
    # Sample 20 rows
    sample_df = df.sample(n=min(20, len(df)), random_state=42, replace=(len(df) < 20)).copy()
    
    # Add Gaussian noise
    rng = np.random.default_rng(42)
    noise = rng.normal(0, 0.05, size=(len(sample_df), len(numeric_feature_cols)))
    sample_df[numeric_feature_cols] = sample_df[numeric_feature_cols] + noise
    
    # Concatenate to create Version 2
    df_v2 = pd.concat([df, sample_df], ignore_index=True)
    updated_rows = len(df_v2)
    
    # Overwrite dataset_v1.csv
    df_v2.to_csv(input_file, index=False)
    
    print(f"Successfully augmented dataset (Version 2).")
    print(f"Initial Rows: {initial_rows}")
    print(f"Added Rows: {len(sample_df)}")
    print(f"Updated Total Rows: {updated_rows} (Expected {initial_rows + 20})")
    print(f"Dataset overwritten at: {input_file}")

if __name__ == "__main__":
    augment_v2()
