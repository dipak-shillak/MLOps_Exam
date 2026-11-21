from datetime import datetime, timezone, timedelta
from feast import FeatureStore

def main():
    store = FeatureStore(repo_path=".")
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=365)
    print(f"[materialize] Materializing features to online store from {start_date.isoformat()} to {end_date.isoformat()}...")
    store.materialize(start_date=start_date, end_date=end_date)
    print("[materialize] Features successfully materialized into SQLite online store.")

if __name__ == "__main__":
    main()
