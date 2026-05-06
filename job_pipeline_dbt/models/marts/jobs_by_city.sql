-- This model answers: which cities have the most jobs, and what do salaries look like?

with jobs as (

    select
        job_id,
        location,
        salary_min,
        salary_max
    from {{ ref('stg_jobs') }}
    where location is not null

),

by_city as (

    select
        -- Location comes in as "Chicago, IL" — split_part pulls just the city name
        -- split_part(value, delimiter, position) → position 1 = everything before the first comma
        split_part(location, ',', 1)    as city,

        count(job_id)                   as job_count,

        -- avg() ignores NULLs automatically, so jobs with no salary don't skew the average
        round(avg(salary_min), 0)       as avg_salary_min,
        round(avg(salary_max), 0)       as avg_salary_max,

        -- A midpoint salary is more useful for visualization than showing two columns
        round(avg((salary_min + salary_max) / 2), 0)  as avg_salary_mid

    from jobs
    group by city

)

select *
from by_city
order by job_count desc