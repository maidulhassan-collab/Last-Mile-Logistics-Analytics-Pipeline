# End-to-End Last-Mile Logistics Analytics Pipeline

A portfolio data engineering and analytics project demonstrating how last-mile logistics data can be ingested, validated, transformed, tested, orchestrated, and visualized using a modern analytics workflow.

> **Note:** This project uses synthetic logistics data created for learning and portfolio demonstration purposes.

## Project Overview

The project simulates a last-mile delivery operation and builds an end-to-end analytics pipeline covering orders, couriers, hubs, payments, returns, and tracking events.

The pipeline processes:

- 60,000 orders
- 4.24M+ tracking events
- 60,000 payment records
- 2,930 return records
- 600 merchants
- 220 couriers
- 12 hubs

## Architecture

```text
CSV Source Data
      ↓
Python ETL
      ↓
PostgreSQL Raw Layer
      ↓
dbt Transformations
      ↓
dbt Data Quality Tests
      ↓
Analytics Tables
      ↓
Power BI Dashboard

Apache Airflow orchestrates:
Python ETL → dbt run → dbt test
```

## Technology Stack

### Data Engineering
- Python
- Pandas
- PostgreSQL
- psycopg2

### Transformation & Data Quality
- dbt
- SQL
- dbt tests

### Orchestration
- Apache Airflow

### Business Intelligence
- Microsoft Power BI

### Environment
- WSL2
- Ubuntu

## ETL Pipeline

The Python ETL pipeline performs:

1. Extraction of logistics CSV files
2. Schema and primary-key validation
3. Data-quality profiling
4. Loading into PostgreSQL raw tables
5. Source-to-database row-count verification

All major source tables were successfully validated and loaded.

## dbt Transformation Layer

dbt transforms raw logistics data into analytics-ready models for reporting and operational analysis.

The project includes:

- Staging models
- Intermediate transformation models
- Order-level fact models
- Daily KPI models
- Data-quality tests

### dbt Test Result

```text
PASS=16
WARN=0
ERROR=0
SKIP=0
TOTAL=16
```

All 16 configured data-quality tests passed successfully.

## Airflow Orchestration

Apache Airflow orchestrates the complete pipeline:

```text
start
  ↓
run_python_etl
  ↓
run_dbt
  ↓
test_dbt
  ↓
end
```

The complete five-task DAG executed successfully.

## Power BI Dashboard

A one-page executive logistics dashboard was developed to monitor operational performance.

Key metrics include:

- Total Orders
- SLA Compliance
- Delivery Success Rate
- Average Delivery Turnaround Time
- Quarterly Order Volume
- Order Status Distribution
- Hub Performance
- Courier Performance

## Key Results

- **Total Orders:** 60K
- **Delivery Success Rate:** 92.42%
- **SLA Compliance:** 75.82%
- **Average Delivery TAT:** 44.15 hours
- **Tracking Events Processed:** 4.24M+
- **dbt Tests:** 16/16 passed

## Repository Structure

```text
logistics_project/
│
├── airflow/
│   └── dags/
│       └── run_logistics_etl.py
│
├── data/
│
├── python_etl/
│   └── python_etl.py
│
├── logistics_dbt_starter/
│   ├── models/
│   ├── tests/
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── .env.example
├── .gitignore
└── README.md
```

## Environment Configuration

Create your local environment file:

```bash
cp .env.example .env
```

Then configure your PostgreSQL credentials locally.

Real credentials are excluded from version control.

## Pipeline Execution

### Python ETL

```bash
python python_etl/python_etl.py
```

### dbt

```bash
cd logistics_dbt_starter
dbt run --profiles-dir .
dbt test --profiles-dir .
```

### Airflow

Airflow orchestrates:

```text
Python ETL → dbt transformations → dbt tests
```

## Business Value

This project demonstrates how raw logistics data can be transformed into reliable operational analytics for monitoring delivery performance, SLA compliance, courier effectiveness, hub performance, returns, and business trends.

It demonstrates practical experience across the complete analytics lifecycle: ingestion, validation, database loading, transformation, testing, orchestration, and visualization.

## Future Improvements

- Automated scheduling
- Retry and failure alerts
- Incremental dbt models
- Dockerized deployment
- CI/CD testing
- Cloud deployment
- Advanced Power BI drill-through analysis
- Merchant and COD performance analysis
- Data-quality monitoring dashboards

## Author

**Md. Maidul Hassan Shanto**

Data Analytics | Data Engineering | Business Intelligence
