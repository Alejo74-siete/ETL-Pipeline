# tests/test_pipeline_basic.py
import os
import pandas as pd
from src.pipeline import production_etl_flow
from pathlib import Path

def test_flow_runs(tmp_path):
    # copy demo data into a temporary watch folder
    demo_csv = Path("demo_data/sample_raw_production.csv")
    watch = tmp_path / "incoming"
    watch.mkdir()
    dest = watch / demo_csv.name
    dest.write_text(demo_csv.read_text())

    # set env override (monkeypatch via env vars works in your CI)
    os.environ["WATCH_FOLDER"] = str(watch)
    os.environ["PROCESSED_FOLDER"] = str(tmp_path / "processed")
    os.environ["SUPABASE_DATABASE_URL"] = os.environ.get("SUPABASE_DATABASE_URL", "sqlite:///:memory:")
    # run flow (should not raise)
    production_etl_flow()
    # assert file archived
    assert len(list((tmp_path / "processed").glob("*.csv"))) == 1
