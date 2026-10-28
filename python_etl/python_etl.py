"""
STEP 6: Python ETL & Automation
Project: Last-Mile Logistics Data Intelligence

Memory rule:
1. Extract   -> find/read source files
2. Validate  -> check schema, keys, basic quality
3. Load      -> bulk load into PostgreSQL raw tables
4. Verify    -> compare source vs database row counts
5. Log       -> record what happened

IMPORTANT:
- raw.* is treated as the source layer.
- Cleaning/standardization remains in staging.* SQL views.
- Never hard-code a real password in GitHub.
"""

from __future__ import annotations

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd
import psycopg2


DATA_DIR = Path(
    os.getenv("LOGISTICS_DATA_DIR", r"C:\path\to\carrybee_logistics_dataset")
)

DB_CONFIG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": int(os.getenv("PGPORT", "5432")),
    "dbname": os.getenv("PGDATABASE", "logistics_intelligence"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", ""),
}

TABLE_ORDER = [
    "hubs",
    "merchants",
    "couriers",
    "orders",
    "tracking_events",
    "payments",
    "returns",
]

PRIMARY_KEYS = {
    "hubs": "hub_id",
    "merchants": "merchant_id",
    "couriers": "courier_id",
    "orders": "order_id",
    "tracking_events": "event_id",
    "payments": "payment_id",
    "returns": "return_id",
}

EXPECTED_COLUMNS = {
    "hubs": [
        "hub_id", "hub_name", "city", "zone",
        "daily_capacity", "opened_date"
    ],
    "merchants": [
        "merchant_id", "merchant_name", "segment", "industry",
        "base_city", "base_hub_id", "onboard_date",
        "acquisition_channel", "default_order_source", "active_flag"
    ],
    "couriers": [
        "courier_id", "courier_name", "hub_id", "vehicle_type",
        "join_date", "employment_status", "daily_capacity"
    ],
    "orders": [
        "order_id", "merchant_id", "order_created_at",
        "origin_hub_id", "destination_hub_id", "destination_city",
        "destination_zone", "service_type", "package_category",
        "weight_kg", "declared_value_bdt", "shipping_fee_bdt",
        "payment_type", "cod_amount_bdt", "promised_delivery_date",
        "assigned_courier_id", "final_status", "order_source"
    ],
    "tracking_events": [
        "event_id", "order_id", "event_time", "event_type",
        "hub_id", "courier_id", "failure_reason"
    ],
    "payments": [
        "payment_id", "order_id", "shipping_fee_due_bdt",
        "shipping_fee_paid_bdt", "cod_due_bdt", "cod_collected_bdt",
        "collection_date", "settlement_status", "settlement_date",
        "reconciliation_status"
    ],
    "returns": [
        "return_id", "order_id", "return_initiated_at",
        "return_reason", "return_status", "return_completed_at",
        "return_cost_bdt"
    ],
}

LOG_FILE = Path("etl_run.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


def source_path(table_name: str) -> Path:
    return DATA_DIR / f"{table_name}.csv"


def extract_csv(table_name: str) -> pd.DataFrame:
    path = source_path(table_name)

    if not path.exists():
        raise FileNotFoundError(f"Missing source file: {path}")

    logger.info("EXTRACT | Reading %s", path.name)
    df = pd.read_csv(path)

    logger.info(
        "EXTRACT | %s rows=%s cols=%s",
        table_name,
        len(df),
        len(df.columns),
    )

    return df


def validate_schema(table_name: str, df: pd.DataFrame) -> None:
    expected = EXPECTED_COLUMNS[table_name]
    actual = list(df.columns)

    missing = [c for c in expected if c not in actual]
    unexpected = [c for c in actual if c not in expected]

    if missing or unexpected:
        raise ValueError(
            f"{table_name}: schema mismatch | "
            f"missing={missing} unexpected={unexpected}"
        )

    logger.info("VALIDATE | %s schema OK", table_name)


def validate_primary_key(table_name: str, df: pd.DataFrame) -> None:
    pk = PRIMARY_KEYS[table_name]

    null_keys = int(df[pk].isna().sum())
    duplicate_keys = int(df[pk].duplicated().sum())

    if null_keys > 0:
        raise ValueError(
            f"{table_name}: {null_keys} NULL values in primary key {pk}"
        )

    if duplicate_keys > 0:
        raise ValueError(
            f"{table_name}: {duplicate_keys} duplicate primary-key values in {pk}"
        )

    logger.info("VALIDATE | %s primary key OK", table_name)


def profile_nulls(table_name: str, df: pd.DataFrame) -> None:
    null_counts = df.isna().sum()
    null_counts = null_counts[null_counts > 0]

    if null_counts.empty:
        logger.info("PROFILE | %s has no pandas-detected NULLs", table_name)
        return

    for column, count in null_counts.items():
        logger.warning(
            "PROFILE | %s.%s missing=%s (%.2f%%)",
            table_name,
            column,
            int(count),
            100 * count / len(df),
        )


def validate_dataframe(table_name: str, df: pd.DataFrame) -> None:
    validate_schema(table_name, df)
    validate_primary_key(table_name, df)
    profile_nulls(table_name, df)


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def truncate_raw_tables(conn) -> None:
    sql = """
    TRUNCATE TABLE
        raw.returns,
        raw.payments,
        raw.tracking_events,
        raw.orders,
        raw.couriers,
        raw.merchants,
        raw.hubs
    RESTART IDENTITY CASCADE;
    """

    with conn.cursor() as cur:
        cur.execute(sql)

    conn.commit()
    logger.info("LOAD | Raw tables truncated")


def bulk_copy_csv(conn, table_name: str) -> None:
    path = source_path(table_name)
    columns = EXPECTED_COLUMNS[table_name]

    copy_sql = f"""
        COPY raw.{table_name} ({", ".join(columns)})
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE,
            DELIMITER ',',
            NULL ''
        )
    """

    logger.info("LOAD | Loading raw.%s", table_name)

    with path.open("r", encoding="utf-8") as file_obj:
        with conn.cursor() as cur:
            cur.copy_expert(copy_sql, file_obj)

    conn.commit()
    logger.info("LOAD | raw.%s loaded", table_name)


def database_row_count(conn, table_name: str) -> int:
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM raw.{table_name};")
        return int(cur.fetchone()[0])


def verify_row_count(conn, table_name: str, expected_source_rows: int) -> None:
    db_rows = database_row_count(conn, table_name)

    if db_rows != expected_source_rows:
        raise ValueError(
            f"{table_name}: row-count mismatch | "
            f"source={expected_source_rows} database={db_rows}"
        )

    logger.info(
        "VERIFY | %s source=%s database=%s MATCH",
        table_name,
        expected_source_rows,
        db_rows,
    )


def run_pipeline() -> None:
    logger.info("=" * 65)
    logger.info("ETL START | %s", datetime.now().isoformat(timespec="seconds"))
    logger.info("DATA_DIR  | %s", DATA_DIR)
    logger.info("=" * 65)

    source_counts = {}

    for table_name in TABLE_ORDER:
        df = extract_csv(table_name)
        validate_dataframe(table_name, df)
        source_counts[table_name] = len(df)

    logger.info("VALIDATE | All source files passed ingestion checks")

    conn = get_connection()

    try:
        truncate_raw_tables(conn)

        for table_name in TABLE_ORDER:
            bulk_copy_csv(conn, table_name)
            verify_row_count(conn, table_name, source_counts[table_name])

        logger.info("=" * 65)
        logger.info("ETL SUCCESS | All raw tables refreshed successfully")
        logger.info("=" * 65)

    except Exception:
        conn.rollback()
        logger.exception("ETL FAILED")
        raise

    finally:
        conn.close()
        logger.info("DATABASE | Connection closed")


if __name__ == "__main__":
    run_pipeline()
