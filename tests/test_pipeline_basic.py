# tests/test_pipeline_basic.py
import os
from pathlib import Path
import pandas as pd
import sys

# ✅ Aseguramos que src esté en el path, para imports relativos
if str(Path(__file__).resolve().parent.parent / "src") not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# Ahora podemos importar directamente
from pipeline import production_etl_flow

def test_flow_runs(tmp_path):
    # copiar demo data en una carpeta temporal
    demo_csv = Path("tests/data/raw_production_sample.csv")
    watch = tmp_path / "incoming"
    watch.mkdir()
    dest = watch / demo_csv.name
    dest.write_text(demo_csv.read_text())

    # set env override (monkeypatch via env vars works in CI)
    os.environ["WATCH_FOLDER"] = str(watch)
    os.environ["PROCESSED_FOLDER"] = str(tmp_path / "processed")
    os.environ["SUPABASE_DATABASE_URL"] = os.environ.get(
        "SUPABASE_DATABASE_URL", "sqlite:///:memory:"
    )

    # run flow (should not raise)
    production_etl_flow()

    # assert file archived
    processed_files = list((tmp_path / "processed").glob("*.csv"))
    assert len(processed_files) == 1
