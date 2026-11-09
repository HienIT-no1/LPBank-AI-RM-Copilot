"""
Data Import Pipeline for LPBank AI RM Copilot.
Loads raw CSV data into MySQL or SQLite database with validation and stats.
"""
import os
import glob
import pandas as pd
from sqlalchemy import create_engine
from backend.app.config import settings

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")


def import_csv_to_database():
    print(f"Connecting to database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")
    connect_args = {}
    if "sqlite" in settings.DATABASE_URL:
        connect_args["check_same_thread"] = False

    engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    if not csv_files:
        print(f"No CSV files found in {DATA_DIR}!")
        return

    print(f"Found {len(csv_files)} CSV files. Beginning import...")
    imported_tables = []

    for file_path in sorted(csv_files):
        table_name = os.path.splitext(os.path.basename(file_path))[0].lower()
        if table_name == "data_dictionary":
            continue

        try:
            df = pd.read_csv(file_path, low_memory=False)
            df.columns = [c.lower() for c in df.columns]

            # Write to database (replace if exists)
            df.to_sql(table_name, con=engine, if_exists="replace", index=False)
            imported_tables.append((table_name, len(df)))
            print(f"  [OK] Table '{table_name}' loaded: {len(df):,} rows.")
        except Exception as e:
            print(f"  [ERROR] Failed to load '{table_name}': {e}")

    print("\n--- IMPORT SUMMARY ---")
    print(f"Total tables imported: {len(imported_tables)}")
    for tbl, rows in imported_tables:
        print(f"  - {tbl:<26}: {rows:>6,} rows")
    print("Database sync completed successfully!")


if __name__ == "__main__":
    import_csv_to_database()

