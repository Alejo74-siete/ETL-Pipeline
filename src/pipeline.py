# src/pipeline.py
import os
from pathlib import Path
from datetime import datetime, UTC
from typing import Optional

import pandas as pd
from dotenv import load_dotenv

from prefect import flow, task, get_run_logger
from production_tools.clean_productiondata import clean_productiondata
from production_tools.qc_checks import (
    run_qc_raw,
    qc_raw_report,
    run_qc_checks,
    format_qc_table,
)

from notifier import send_email_report
from storage import get_engine
from utils import ensure_folders, archive_file

load_dotenv()

engine = None
try:
    engine = get_engine()
except Exception:
    engine = None  # tests may use sqlite in-memory


@task
def list_csv_files(folder: str):
    p = Path(folder)
    return sorted([str(f) for f in p.glob("*.csv")])


@task
def read_csv(path: str) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info(f"Reading {path}")
    df = pd.read_csv(path)
    return df


@task
def run_raw_qc_task(df: pd.DataFrame) -> str:
    qc = run_qc_raw(df)
    return qc_raw_report(qc)


@task
def clean_df_task(df: pd.DataFrame) -> pd.DataFrame:
    return clean_productiondata(df)


@task
def run_clean_qc_task(df: pd.DataFrame) -> str:
    qc = run_qc_checks(df)
    return format_qc_table(qc)


@task
def upload_to_postgres_task(df: pd.DataFrame, table_name: str):
    logger = get_run_logger()
    if engine is None:
        logger.warning("No DB engine configured; skipping upload.")
        return 0
    df.to_sql(table_name, engine, if_exists="append", index=False)
    logger.info(f"Uploaded {len(df)} rows to {table_name}")
    return len(df)


@task
def archive_task(path: str, processed_folder: str):
    dest = archive_file(path, processed_folder)
    return dest


@flow(name="production_etl_flow")
def production_etl_flow(
    watch_folder: Optional[str] = None,
    processed_folder: Optional[str] = None,
    table_name: Optional[str] = None,
):
    """
    ETL flow for production data.

    Args:
        watch_folder: Folder to watch for CSV files
            (defaults to env var or 'demo_data')
        processed_folder: Folder to archive processed files
            (defaults to env var or 'processed_csv')
        table_name: Database table name
            (defaults to env var or 'production_clean')
    """
    logger = get_run_logger()

    # Use provided values or fall back to env vars
    watch_folder = watch_folder or os.getenv("WATCH_FOLDER", "demo_data")
    processed_folder = processed_folder or os.getenv(
        "PROCESSED_FOLDER", "processed_csv"
    )
    table_name = table_name or os.getenv("TABLE_NAME", "production_clean")

    ensure_folders([watch_folder, processed_folder])

    files = list_csv_files(watch_folder)
    if not files:
        logger.info("No CSVs found.")
        return

    for path in files:
        logger.info(f"Processing file: {path}")
        df_raw = read_csv(path)
        raw_report = run_raw_qc_task(df_raw)

        df_clean = clean_df_task(df_raw)
        clean_report = run_clean_qc_task(df_clean)

        rows_uploaded = upload_to_postgres_task(df_clean, table_name)

        new_path = archive_task(path, processed_folder)

        timestamp = datetime.now(UTC).isoformat()
        full_report = (
            f"File: {Path(path).name}\nProcessed: {timestamp}\n\n"
            "===== RAW QC =====\n"
            f"{raw_report}\n\n"
            "===== CLEAN QC =====\n"
            f"{clean_report}\n\n"
            f"Archived to: {new_path}\n"
            f"Rows uploaded: {rows_uploaded}\n"
        )

        send_email_report(full_report)
    logger.info("ETL cycle complete.")
