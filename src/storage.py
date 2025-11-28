# src/storage.py
from sqlalchemy import create_engine
import os

SUPABASE_DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")


def get_engine():
    if not SUPABASE_DATABASE_URL:
        raise RuntimeError("SUPABASE_DATABASE_URL not set in env")
    engine = create_engine(SUPABASE_DATABASE_URL, future=True)
    return engine
