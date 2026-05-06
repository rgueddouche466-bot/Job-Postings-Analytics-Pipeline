-- This model takes the raw job data loaded by Python and cleans it up.
-- "with" blocks (CTEs) are just named subqueries — they make SQL readable.

with source as (

    select * from {{ source('raw', 'JOBS') }}

),

cleaned as (

    select
        JOB_ID                            as job_id,
        trim(TITLE)                       as job_title,       -- trim() removes extra spaces
        trim(COMPANY)                     as company_name,
        trim(LOCATION)                    as location,
        SALARY_MIN::float                 as salary_min,      -- ::float ensures it's a number, not text
        SALARY_MAX::float                 as salary_max,
        try_to_timestamp(CREATED)         as created_at,       -- converts text date to a real timestamp
        DESCRIPTION                       as job_description                                                   -- try_ means it returns NULL instead of crashing on bad values
    from source
    where JOB_ID is not null                                  -- filter out any rows with no ID

)

select * from cleaned