# run.py
"""
Run the ETL pipeline manually.
"""
from src.pipeline import production_etl_flow

if __name__ == "__main__":
    print("▶️  Running ETL pipeline...")
    production_etl_flow()
    print("✅ Done!")
