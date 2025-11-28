# run_pipeline.py
"""
Main entry point for running the production ETL pipeline.
Run this script to process all CSV files in the watch folder.
"""
import argparse
from src.pipeline import production_etl_flow


def main():
    parser = argparse.ArgumentParser(description="Run Production ETL Pipeline")
    parser.add_argument(
        "--watch-folder",
        help="Folder to watch for CSV files " "(default: from .env or 'demo_data')",
    )
    parser.add_argument(
        "--processed-folder",
        help="Folder to archive processed files "
        "(default: from .env or 'processed_csv')",
    )
    parser.add_argument(
        "--table-name",
        help="Database table name " "(default: from .env or 'production_clean')",
    )

    args = parser.parse_args()

    print("🚀 Starting Production ETL Pipeline...")
    print("=" * 50)

    try:
        production_etl_flow(
            watch_folder=args.watch_folder,
            processed_folder=args.processed_folder,
            table_name=args.table_name,
        )
        print("=" * 50)
        print("✅ Pipeline completed successfully!")
    except Exception as e:
        print("=" * 50)
        print(f"❌ Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()
