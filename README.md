# End-to-End Last-Mile Logistics Analytics Pipeline

<p align="center">
  <b>An End-to-End Data Engineering, Analytics Engineering, Workflow Orchestration & Business Intelligence Project</b>
</p>

<p align="center">
  Python • PostgreSQL • dbt • Apache Airflow • Power BI • Pandas • SQL • WSL2
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-ETL-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/dbt-Analytics%20Engineering-FF694B?logo=dbt&logoColor=white" alt="dbt">
  <img src="https://img.shields.io/badge/Apache%20Airflow-Orchestration-017CEE?logo=apacheairflow&logoColor=white" alt="Apache Airflow">
  <img src="https://img.shields.io/badge/Power%20BI-Business%20Intelligence-F2C811?logo=powerbi&logoColor=black" alt="Power BI">
  <img src="https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas&logoColor=white" alt="Pandas">
</p>

<p align="center">
  <b>60K Orders • 4.24M+ Tracking Events • 16/16 dbt Tests Passed • 5/5 Airflow Tasks Successful</b>
</p>

![Project Overview](https://github.com/maidulhassan-collab/Last-Mile-Logistics-Analytics-Pipeline/blob/main/presentation_gif.gif)

---

## Project Overview

This project demonstrates a complete last-mile logistics analytics workflow, transforming raw operational data into validated, analytics-ready datasets and executive-level business intelligence.

The pipeline integrates:

**CSV Source Data → Python ETL → PostgreSQL → dbt Transformations → dbt Testing → Apache Airflow → Power BI**

The project covers the complete analytics lifecycle, including data ingestion, validation, relational storage, analytical modelling, automated testing, workflow orchestration, and dashboard development.

> **Note:** The project uses synthetic logistics data created for portfolio and learning purposes.
---

## Project Highlights

| Metric | Result |
|---|---:|
| Orders | **60,000** |
| Tracking events | **4.24M+** |
| Payment records | **60,000** |
| Return records | **2,930** |
| Merchants | **600** |
| Couriers | **220** |
| Hubs | **12** |
| dbt tests | **16 / 16 passed** |
| Delivery success rate | **92.42%** |
| SLA compliance | **75.82%** |
| Average delivery TAT | **44.15 hours** |
| Airflow workflow | **5 / 5 tasks successful** |

---

## Dashboard Preview

<p align="center">
  <img src="https://github.com/maidulhassan-collab/Last-Mile-Logistics-Analytics-Pipeline/blob/main/powerbi_snap.png" width="900"/>
</p>

The Power BI executive dashboard summarizes operational delivery performance through:

- Total Orders
- Delivery Success Rate
- SLA Compliance
- Average Delivery Turnaround Time
- Quarterly Order Volume
- Order Status Distribution
- Hub Performance
- Courier Performance

---

## Business Problem

Last-mile delivery operations generate large volumes of fragmented data across orders, tracking events, hubs, couriers, payments, returns, and merchants.

The project was designed to answer practical operational questions such as:

- How many orders are being processed?
- What proportion of eligible orders are successfully delivered?
- Are deliveries meeting SLA targets?
- How long does delivery take on average?
- What are the main final order outcomes?
- Which hubs show stronger delivery performance?
- Which couriers show stronger delivery performance?
- Can the complete workflow be executed reliably from ingestion to analytics?

---

## Solution Architecture

```text
                    ┌───────────────────────────┐
                    │      CSV Source Data      │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │        Python ETL         │
                    │  Validation + Profiling   │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │      PostgreSQL Raw       │
                    │          Layer            │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │     dbt Transformations   │
                    │ Staging → Intermediate →  │
                    │      Facts / Marts        │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │      dbt Data Tests       │
                    │    16 / 16 Successful     │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │     Analytics Models      │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │       Power BI            │
                    │   Executive Dashboard     │
                    └───────────────────────────┘

                 Apache Airflow orchestrates:
           Python ETL → dbt run → dbt test
```

---

## Technology Stack

### Data Engineering
- Python 3
- Pandas
- psycopg2
- PostgreSQL

### Analytics Engineering
- SQL
- dbt
- Staging, intermediate, fact, and mart models
- Automated dbt data-quality tests

### Workflow Orchestration
- Apache Airflow
- DAG-based dependency management
- BashOperator / EmptyOperator workflow

### Business Intelligence
- Microsoft Power BI
- KPI design
- Operational performance reporting
- Hub and courier performance analysis

### Development Environment
- WSL2
- Ubuntu
- Git / GitHub
- Python virtual environments
- Environment-variable based credential management

---

## Dataset Overview

The synthetic dataset models a realistic last-mile logistics environment.

| Dataset Area | Scale |
|---|---:|
| Orders | 60,000 |
| Tracking Events | 4,244,332 |
| Payments | 60,000 |
| Returns | 2,930 |
| Merchants | 600 |
| Couriers | 220 |
| Hubs | 12 |

The project works with multiple operational entities rather than a single flat table, allowing the pipeline to demonstrate ingestion, relational modeling, transformation, validation, and analytics across a more realistic data landscape.

---

## 1. Python ETL Pipeline

The Python ETL layer is responsible for bringing source data into PostgreSQL safely and consistently.

### Main responsibilities

1. Read logistics CSV files
2. Validate expected schemas
3. Validate primary keys
4. Profile missing values and selected data-quality conditions
5. Load validated data into PostgreSQL raw tables
6. Verify source row counts against database row counts
7. Record pipeline execution information in logs

### ETL validation result

The source files passed the ingestion checks, and the major tables were successfully loaded and verified against their source row counts.

Example verification:

```text
raw.hubs             source=12       database=12       MATCH
raw.merchants        source=600      database=600      MATCH
raw.couriers         source=220      database=220      MATCH
raw.orders           source=60000    database=60000    MATCH
raw.tracking_events  source=4244332  database=4244332  MATCH
raw.payments         source=60000    database=60000    MATCH
raw.returns          source=2930     database=2930     MATCH
```

---

## 2. PostgreSQL Data Foundation

PostgreSQL serves as the central analytical database.

The solution separates raw ingestion from analytical transformation so that the source data remains distinct from business-facing models.

Conceptually:

```text
Raw Tables
    ↓
Staging Models
    ↓
Intermediate Models
    ↓
Fact / Mart Models
    ↓
Analytics Tables
```

This separation improves clarity, maintainability, and reproducibility.

---

## 3. dbt Transformation Layer

dbt transforms raw logistics tables into reusable analytical models.

The project includes:

- Source definitions
- Staging models
- Intermediate transformation models
- Order-level fact model
- Daily KPI mart
- Schema tests
- Custom KPI range tests

Example model flow:

```text
raw.orders
raw.tracking_events
        ↓
stg_orders
stg_tracking_events
        ↓
int_order_events
        ↓
fct_orders
        ↓
mart_daily_kpi
```

---

## 4. Data Quality Testing

The project uses dbt tests to validate analytical reliability.

### Test coverage includes

- Not-null checks
- Unique-key checks
- Accepted-value checks
- Source-level integrity checks
- KPI range validation

### Final dbt test result

```text
PASS=16
WARN=0
ERROR=0
SKIP=0
TOTAL=16
```

**All 16 configured dbt tests passed successfully.**


---

## 5. Apache Airflow Orchestration

Apache Airflow orchestrates the end-to-end workflow.

### DAG sequence

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

The dependency chain ensures that:

- dbt transformations do not run before ingestion succeeds
- dbt tests do not run before transformation succeeds
- the workflow completes only after all upstream stages succeed

### Final orchestration result

**All five Airflow tasks completed successfully.**


---

## 6. Power BI Executive Dashboard

The final analytics layer is consumed in Power BI through business-facing PostgreSQL analytics tables.

The dashboard focuses on operational performance rather than reproducing transformation logic in Power BI.

### Key dashboard KPIs

| KPI | Result |
|---|---:|
| Total Orders | **60K** |
| Delivery Success Rate | **92.42%** |
| SLA Compliance | **75.82%** |
| Average Delivery TAT | **44.15 hrs** |

### Main visuals

- Quarterly Order Volume
- Order Status Distribution
- Delivery Success Rate by Hub
- Top Courier Performance

This allows the technical pipeline to end with a business-facing layer that can be understood quickly by operational or management stakeholders.

---

## Key Analytical Observations

### High Delivery Success
The portfolio dataset produced a **92.42% delivery success rate**, indicating that the large majority of eligible orders reached a successful delivery outcome.

### SLA Opportunity
SLA compliance was **75.82%**, showing that delivery completion and delivery timeliness should be evaluated separately.

### Delivery Turnaround
Average delivery turnaround time was approximately **44.15 hours**.

### Order Outcomes
Most orders were delivered, while smaller proportions were returned, failed, cancelled, in transit, or out for delivery.

> These observations describe the synthetic dataset only and should not be interpreted as performance claims about a real logistics company.

---

## Project Deliverables

The repository can include the following portfolio artifacts:

- 📊 **Power BI Dashboard**
- 📄 **Full Project Report**
- 🎤 **Project Presentation**
- ⚙️ **Apache Airflow DAG**
- 🧪 **dbt Models & Tests**
- 🐍 **Python ETL Pipeline**
- 🗄️ **PostgreSQL Analytics Workflow**

### Portfolio Files

- [View Full Project Report](https://github.com/maidulhassan-collab/Last-Mile-Logistics-Analytics-Pipeline/blob/main/Last_Mile_Logistics_Analytics_Project_Report.pdf)
- [View Project Presentation](https://github.com/maidulhassan-collab/Last-Mile-Logistics-Analytics-Pipeline/blob/main/Last_Mile_Logistics_presentation.pptx)

If the Power BI `.pbix` file is included in the repository:

- [Open Power BI Project File](https://github.com/maidulhassan-collab/Last-Mile-Logistics-Analytics-Pipeline/blob/main/Last_Mile_Logistics_Analytics_Dashboard.pbix)

---

## Repository Structure

```text
logistics_project/
│
├── airflow/
│   └── dags/
│       └── run_logistics_etl.py
│
├── data/
│   └── carrybee_logistics_dataset/
│       ├── couriers.csv
│       ├── hubs.csv
│       ├── merchants.csv
│       ├── orders.csv
│       ├── payments.csv
│       ├── returns.csv
│       └── tracking_events.csv
│
├── logistics_dbt_starter/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   ├── marts/
│   │   └── sources.yml
│   ├── tests/
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── python_etl/
│   └── python_etl.py
│
├── docs/
│   ├── dashboard.png
│   ├── airflow_success.png
│   ├── dbt_tests.png
│   ├── Last_Mile_Logistics_Analytics_Project_Report.pdf
│   └── Last_Mile_Logistics_Analytics_Presentation.pptx
│
├── dashboard/
│   └── Last_Mile_Logistics_Analytics_Dashboard.pbix
│
├── .env.example
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

Install or configure:

- Python 3
- PostgreSQL
- dbt with PostgreSQL adapter
- Apache Airflow
- Power BI Desktop
- WSL2 / Ubuntu if reproducing the same development environment

---

## Environment Configuration

Copy the environment template:

```bash
cp .env.example .env
```

Then configure the local values.

Example:

```bash
export LOGISTICS_DATA_DIR="/home/YOUR_USERNAME/logistics_project/data/carrybee_logistics_dataset"

export PGHOST="YOUR_POSTGRES_HOST"
export PGPORT="5432"
export PGDATABASE="logistics_intelligence"
export PGUSER="postgres"
export PGPASSWORD="YOUR_POSTGRES_PASSWORD"
```

> Never commit real credentials. The `.env` file is excluded from version control through `.gitignore`.

---

## Running the Pipeline

### 1. Activate the Python environment

```bash
source project_venv/bin/activate
```

### 2. Load environment variables

```bash
source .env
```

### 3. Run Python ETL

```bash
python python_etl/python_etl.py
```

### 4. Run dbt transformations

```bash
cd logistics_dbt_starter
dbt run --profiles-dir .
```

### 5. Run dbt tests

```bash
dbt test --profiles-dir .
```

Expected final test result:

```text
PASS=16
WARN=0
ERROR=0
SKIP=0
TOTAL=16
```

### 6. Run through Airflow

Start Airflow using the configured Airflow environment and trigger:

```text
run_logistics_etl
```

Airflow executes:

```text
Python ETL → dbt run → dbt test
```

---

## Credential & Repository Security

The project keeps credentials outside version control.

Ignored items include:

```text
.env
project_venv/
venv/
.venv/
__pycache__/
*.log
logistics_dbt_starter/target/
logistics_dbt_starter/logs/
dbt_packages/
```

`profiles.yml` reads database credentials from environment variables rather than hard-coding passwords.

---

## Engineering Challenges Solved

During development, the project required troubleshooting across several parts of the stack.

| Challenge | Resolution |
|---|---|
| WSL environment instability | Rebuilt a clean Ubuntu/WSL environment and recovered project assets |
| Python environment corruption | Recreated isolated virtual environments and dependencies |
| PostgreSQL connectivity from WSL | Configured host-based environment variables and verified the database connection |
| Airflow metadata errors | Reinitialized/migrated the Airflow metadata database |
| Pipeline reproducibility | Rebuilt and validated ETL, dbt, and Airflow components independently before orchestration |
| Credential security | Used `.env`, `.env.example`, `.gitignore`, and environment-variable based dbt configuration |

These challenges strengthened the project beyond dashboard creation by requiring environment recovery, debugging, and end-to-end system integration.

---

## Skills Demonstrated

### Data Engineering
- Python ETL development
- Multi-file ingestion
- Data validation
- PostgreSQL loading
- Row-count reconciliation
- Data-quality profiling

### Analytics Engineering
- dbt modeling
- Staging and intermediate layers
- Fact and mart design
- SQL transformations
- Automated testing

### Orchestration
- Apache Airflow
- DAG creation
- Task dependencies
- End-to-end workflow execution

### Business Intelligence
- Power BI dashboard development
- KPI design
- Operational performance analysis
- Hub and courier comparisons

### Engineering Practices
- Linux / WSL
- Virtual environments
- Git / GitHub
- Environment variables
- Credential isolation
- Debugging and recovery

---

## Limitations

This is a portfolio project and intentionally remains smaller than a production logistics platform.

Current limitations include:

- Synthetic rather than live operational data
- No cloud deployment
- No CI/CD pipeline
- No production alerting
- No incremental dbt processing
- No real-time event streaming
- Power BI analysis is currently focused on a single executive page

These limitations are intentionally documented rather than presented as completed capabilities.

---

## Future Improvements

Planned extensions include:

### Pipeline Reliability
- Scheduled Airflow execution
- Retry policies
- Failure notifications
- SLA monitoring

### Analytics Engineering
- Incremental dbt models
- Additional dimensional models
- Automated data-quality monitoring
- dbt documentation enhancements

### Deployment
- Dockerized environments
- CI/CD testing
- Cloud-hosted PostgreSQL / warehouse deployment
- Managed orchestration

### Business Analytics
- Merchant performance analysis
- COD reconciliation analytics
- Return reason analysis
- Courier drill-through reporting
- Hub-level operational diagnostics
- Predictive delivery-risk modeling

---

## Why This Project Matters

This project demonstrates more than dashboard creation.

It covers the complete analytical lifecycle:

```text
Raw Operational Data
        ↓
Validated Ingestion
        ↓
Structured Database
        ↓
Reusable Transformations
        ↓
Automated Data Tests
        ↓
Workflow Orchestration
        ↓
Business Intelligence
```

The result is a single portfolio project that combines **data engineering, analytics engineering, data quality, workflow automation, and business intelligence**.

---

## Author

**Md. Maidul Hassan Shanto**

Data Analytics | Data Engineering | Business Intelligence

---

### If you found this project useful

Feel free to explore the source code, analytical models, project report, presentation, and dashboard included in the repository.
