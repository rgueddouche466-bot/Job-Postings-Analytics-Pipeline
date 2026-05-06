# Job Postings Analytics Pipeline

End-to-end data pipeline that pulls live job postings from the Adzuna API, loads into Snowflake, transforms with dbt, and visualizes in Looker Studio.

## Architecture

Adzuna API → Python → Snowflake (RAW) → dbt → Snowflake (MARTS) → Looker Studio/PBI
![design diagram .png](design%20diagram%20.png)

## Tech Stack
| Layer | Tool |
|---|---|
| Ingestion | Python (requests, pandas, snowflake-connector) |
| Warehouse | Snowflake |
| Transformation | dbt Core |
| Visualization | Looker Studio |

## What the Pipeline Does
- Pulls 600+ job postings across 4 search terms and 2 location strategies (Chicago + remote)
- Uses Snowflake MERGE to prevent duplicate inserts across runs
- dbt staging layer cleans and types raw data (views)
- dbt mart layer answers 3 business questions (tables):
  - `jobs_skill_match` — scores and ranks jobs against a weighted skill set
  - `jobs_by_skill` — counts job demand by tech skill (Kafka, Snowflake, Java, Python, etc.)
  - `jobs_by_city` — aggregates job count and salary by city
- 12 passing dbt data quality tests (not_null, unique, accepted_values)

## How to Run
```bash
# 1. Install dependencies
pip install -r requirments.txt

# 2. Add a .env file with Adzuna and Snowflake credentials

# 3. Run ingestion
cd ingestion && python ingest_jobs.py

# 4. Run dbt
cd job_pipeline_dbt && dbt run && dbt test
```

## Environment Variables

ADZUNA_APP_ID, ADZUNA_API_KEY
SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT
SNOWFLAKE_DATABASE, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_SCHEMA

## Dashboard

**Job Match Dashboard** — jobs ranked by skill match score
![match skills.png](match%20skills.png)

**Market Intelligence** — jobs by city and skills in demand
![market by skill and city .png](market%20by%20skill%20and%20city%20.png)