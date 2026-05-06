-- This model answers: which tech skills appear most in job postings?
-- We do this by checking if each job title CONTAINS a skill keyword.

with jobs as (

    select job_id, job_title
    from {{ ref('stg_jobs') }}
    where job_title is not null

),

-- We define the skills we want to track

skills as (

    select 'Python'     as skill union all
    select 'SQL'        as skill union all
    select 'Snowflake'  as skill union all
    select 'Kafka'      as skill union all
    select 'dbt'        as skill union all
    select 'Spark'      as skill union all
    select 'Azure'      as skill union all
    select 'AWS'        as skill union all
    select 'Airflow'    as skill

),

matched as (

    select
        s.skill,
        count(j.job_id)     as job_count
    from skills s
    left join jobs j
        -- contains() checks if the job title includes the skill name.
        -- upper() on both sides makes the match case-insensitive.
        on contains(upper(j.job_title), upper(s.skill))
    group by s.skill

)

select
    skill,
    job_count,
    -- This adds a % share column — useful for Power BI pie/bar charts
    round(job_count * 100.0 / nullif(sum(job_count) over (), 0), 1) as pct_of_total
from matched
order by job_count desc