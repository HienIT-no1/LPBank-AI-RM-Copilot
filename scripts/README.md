# Scripts Directory

Utility scripts for database seeding, ETL pipelines, and mock generation.

---

## 1. `import_data.py`
Imports all CSV files from `data/raw/` directly into the configured database (MySQL or SQLite).
- Automatically sanitizes column headers to lowercase.
- Logs import statistics per table.
- Usage:
  ```bash
  python scripts/import_data.py
  ```

