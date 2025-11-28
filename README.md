# ETL Production Pipeline

A Prefect-based ETL pipeline for processing oil & gas production data with built-in quality checks, database storage, and email notifications.

## Features

- 📂 **Automatic file processing** - Watches a local folder for CSV production files
- 🔍 **Quality checks** - Raw data QC (BRONZE) and cleaned data QC (SILVER/GOLD)
- 🧹 **Data cleaning** - Uses the `production_tools` package for data transformation
- 💾 **Database storage** - Uploads clean data to PostgreSQL (Supabase)
- 📧 **Email notifications** - Sends summary reports with QC results via Gmail SMTP
- 📦 **File archiving** - Archives processed CSVs automatically
- ✅ **Tested** - Includes pytest test suite

## Project Structure
```
ETL-Pipeline/
├── src/
│   ├── pipeline.py              # Main Prefect flow
│   ├── storage.py               # Database connection
│   ├── notifier.py              # Email notifications
│   ├── utils.py                 # Helper functions
│   └── production_tools/        # Data cleaning & QC modules
├── tests/
│   ├── test_pipeline_basic.py   # Pipeline tests
│   └── data/                    # Test data
├── demo_data/                   # Sample CSV files (watched folder)
├── processed_csv/               # Archived processed files
├── run_pipeline.py              # Main entry point
├── .env.example                 # Environment variables template
├── pyproject.toml               # Project configuration
└── README.md
```

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database (e.g., Supabase)
- Gmail account with App Password for SMTP

## Installation

1. **Clone the repository**
```bash
   git clone <repository-url>
   cd ETL-Pipeline
```

2. **Create and activate virtual environment**
```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
```

3. **Install the package**
```bash
   pip install -e .
```

4. **Configure environment variables**
```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env with your credentials
```

## Configuration

Create a `.env` file with the following variables:
```env
# Database
SUPABASE_DATABASE_URL=postgresql://user:password@host:port/database

# Email notifications
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@example.com

# Pipeline folders
WATCH_FOLDER=demo_data
PROCESSED_FOLDER=processed_csv
TABLE_NAME=production_clean
```

### Gmail SMTP Setup

1. Enable 2-factor authentication on your Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Use the App Password in `SMTP_PASSWORD`

## Usage

### Run the pipeline once
```bash
python run_pipeline.py
```

### Run with custom folders
```bash
python run_pipeline.py --watch-folder my_data --processed-folder my_processed
```

### View help
```bash
python run_pipeline.py --help
```

## Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html -v

# Run specific test
python -m pytest tests/test_pipeline_basic.py -v
```

## Scheduling (Production)

### Option 1: Prefect Deployment (Recommended)

Create a deployment for scheduled runs:
```bash
# Create deployment with weekly schedule
prefect deployment build src/pipeline.py:production_etl_flow \
  --name "weekly-production-etl" \
  --cron "0 0 * * 0"  # Every Sunday at midnight

# Apply the deployment
prefect deployment apply production_etl_flow-deployment.yaml

# Start a worker
prefect worker start --pool default
```

### Option 2: Cron (Linux/macOS)
```bash
# Edit crontab
crontab -e

# Add line for weekly run (every Sunday at midnight)
0 0 * * 0 cd /path/to/ETL-Pipeline && /path/to/.venv/bin/python run_pipeline.py
```

### Option 3: Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., weekly on Sunday)
4. Action: Start a program
   - Program: `C:\path\to\.venv\Scripts\python.exe`
   - Arguments: `run_pipeline.py`
   - Start in: `C:\path\to\ETL-Pipeline`

## Development

### Install with dev dependencies
```bash
pip install -e ".[dev]"
```

### Code formatting
```bash
black .
```

### Linting
```bash
flake8 .
```

## Pipeline Flow
```
1. Watch folder for CSV files
   ↓
2. Read CSV file
   ↓
3. Run raw QC checks (BRONZE)
   ↓
4. Clean data (SILVER)
   ↓
5. Run cleaned QC checks (GOLD)
   ↓
6. Upload to PostgreSQL
   ↓
7. Archive CSV file
   ↓
8. Send email report
```

## Troubleshooting

### Import errors
```bash
# Reinstall package
pip install -e .
```

### Database connection errors

- Verify `SUPABASE_DATABASE_URL` is correct
- Check firewall allows PostgreSQL connections
- Test connection: `psql $SUPABASE_DATABASE_URL`

### Email not sending

- Verify Gmail App Password is correct
- Check SMTP settings in `.env`
- Ensure 2FA is enabled on Gmail account

### No CSVs found

- Check `WATCH_FOLDER` path in `.env`
- Ensure CSV files exist in the watch folder
- Verify file permissions

## CI/CD

GitHub Actions workflow included (`.github/workflows/python-ci.yml`):
- Runs tests on push/PR
- Tests on Python 3.10 and 3.11
- Linting with black and flake8

Add secrets to GitHub repository:
- `SUPABASE_DATABASE_URL`

## License

MIT

## Author

Alejandro Perez Tabares

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request