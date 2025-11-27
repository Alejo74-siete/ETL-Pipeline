# ETL Production Pipeline (Prefect)

ETL pipeline that:
- Watches a local folder for CSV production files (demo folder included).
- Runs raw QC (BRONZE).
- Cleans data using the `production_tools` package (SILVER).
- Runs cleaned QC (SILVER/GOLD).
- Uploads clean data to PostgreSQL (Supabase).
- Sends an email summary with QC reports (Gmail SMTP).
- Archives processed CSVs.

## Quickstart (local)

1. Copy `.env.example` → `.env` and fill secrets.
2. Create Python environment and install:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
