import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator


with DAG(
    dag_id="run_logistics_etl",
    description="Run the logistics ETL and dbt analytics pipeline",
    start_date=pendulum.datetime(2026, 10, 1, tz="Asia/Dhaka"),
    schedule=None,
    catchup=False,
    tags=["logistics", "etl", "dbt", "learning"],
) as dag:

    start = EmptyOperator(
        task_id="start"
    )

    run_python_etl = BashOperator(
        task_id="run_python_etl",
        bash_command="""
        set -e

        source /home/maidul/logistics_project/.env

        /home/maidul/logistics_project/project_venv/bin/python \
        /home/maidul/logistics_project/python_etl/python_etl.py
        """
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="""
        set -e

        source /home/maidul/logistics_project/.env

        cd /home/maidul/logistics_project/logistics_dbt_starter

        /home/maidul/logistics_project/project_venv/bin/dbt run \
        --profiles-dir .
        """
    )

    test_dbt = BashOperator(
        task_id="test_dbt",
        bash_command="""
        set -e

        source /home/maidul/logistics_project/.env

        cd /home/maidul/logistics_project/logistics_dbt_starter

        /home/maidul/logistics_project/project_venv/bin/dbt test \
        --profiles-dir .
        """
    )

    end = EmptyOperator(
        task_id="end"
    )

    start >> run_python_etl >> run_dbt >> test_dbt >> end
