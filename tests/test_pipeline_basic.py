# tests/test_pipeline_basic.py
import os
from pathlib import Path

from pipeline import production_etl_flow


def test_flow_runs(tmp_path):
    """Test that the ETL flow processes a CSV file successfully."""

    # Setup: Copy demo data to temporary folder
    demo_csv = Path("tests/data/raw_production_sample.csv")

    # Verify test data exists
    if not demo_csv.exists():
        raise FileNotFoundError(f"Test data not found at {demo_csv}")

    watch = tmp_path / "incoming"
    watch.mkdir()
    dest = watch / demo_csv.name
    dest.write_text(demo_csv.read_text())

    # Verify the file was copied
    assert dest.exists(), f"Failed to copy test file to {dest}"

    # Set database URL for testing (use in-memory SQLite)
    os.environ["SUPABASE_DATABASE_URL"] = "sqlite:///:memory:"

    # Execute: Run the flow with test folders
    production_etl_flow(
        watch_folder=str(watch),
        processed_folder=str(tmp_path / "processed"),
        table_name="production_clean_test",
    )

    # Assert: Verify file was archived
    processed_files = list((tmp_path / "processed").glob("*.csv"))
    assert (
        len(processed_files) == 1
    ), f"Expected 1 processed file, found {len(processed_files)}"

    # Additional assertion: Verify original file no longer in watch folder
    remaining_files = list(watch.glob("*.csv"))
    assert (
        len(remaining_files) == 0
    ), f"Expected 0 files in watch folder, found {len(remaining_files)}"
