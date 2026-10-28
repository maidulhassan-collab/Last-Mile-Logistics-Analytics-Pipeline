STEP 7 DBT STARTER PROJECT

Memory rule:
Source -> Stage -> Transform -> Test -> Document

Recommended local PostgreSQL setup:
1. Create and activate a Python virtual environment.
2. Install: python -m pip install dbt-postgres
3. Run: dbt --version
4. Configure your local ~/.dbt/profiles.yml using profiles.example.yml.
5. Set PGPASSWORD as an environment variable. Do not commit your password.
6. From the project folder run:
   dbt debug
   dbt run
   dbt test
   or dbt build
