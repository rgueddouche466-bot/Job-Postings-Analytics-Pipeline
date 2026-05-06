-- ============================================================
-- MART: jobs_skill_match
-- ============================================================

with jobs as (

    select
        job_id,
        job_title,
        company_name,
        location,
        salary_min,
        salary_max,
        created_at,
        job_description
    from {{ ref('stg_jobs') }}
    where job_title is not null

),

-- ----------------------------------------------------------------
-- Each skill has a weight
-- Higher weight = more valuable signal when a job mentions it.
--
-- TIER 1 (weight 15): Your strongest, most marketable skills
-- TIER 2 (weight 10): Strong but more common
-- TIER 3 (weight 5) : Foundational skills everyone has
-- ----------------------------------------------------------------
your_skills as (

    -- TIER 1 — Your differentiators (Kafka + Snowflake + Azure combo is rare)
    select 'Snowflake'    as skill, 15 as weight union all
    select 'Kafka'        as skill, 15 as weight union all
    select 'Azure'        as skill, 15 as weight union all
    select 'Power BI'     as skill, 15 as weight union all

    -- TIER 2 — Strong but widely shared
    select 'Java'         as skill, 10 as weight union all
    select 'Spring Boot'  as skill, 10 as weight union all
    select 'Spring'       as skill, 10 as weight union all
    select 'Python'       as skill, 10 as weight union all
    select 'SQL'          as skill, 10 as weight union all

    -- TIER 3 — Foundational, good to have
    select 'AWS'          as skill,  5 as weight union all
    select 'Docker'       as skill,  5 as weight union all
    select 'Terraform'    as skill,  5 as weight union all
    select 'dbt'          as skill,  5 as weight union all
    select 'Microservices' as skill, 5 as weight

),


skill_matches as (

    select
        j.job_id,
        j.job_title,
        j.company_name,
        j.location,
        j.salary_min,
        j.salary_max,
        j.created_at,
        s.skill                         as matched_skill,
        s.weight                        as skill_weight
    from jobs j
    inner join your_skills s
        on contains(upper(j.job_title), upper(s.skill))
        or contains(upper(j.job_description), upper(s.skill))

),

-- ----------------------------------------------------------------

scored as (

    select
        job_id,
        job_title,
        company_name,
        location,
        salary_min,
        salary_max,
        created_at,

        -- Sum up the weights of all skills found in this job title
        sum(skill_weight)                                    as raw_score,

        -- Readable list of which skills matched
        listagg(matched_skill, ', ')
            within group (order by skill_weight desc)        as matched_skills,

        -- Count how many of  skills appeared
        count(matched_skill)                                 as skills_matched_count

    from skill_matches
    group by
        job_id, job_title, company_name,
        location, salary_min, salary_max, created_at

),

-- ----------------------------------------------------------------
-- Normalize the score to 0–100 scale..
-- ----------------------------------------------------------------
max_possible as (

    select sum(weight) as max_score from your_skills

),

final as (

    select
        s.job_id,
        s.job_title,
        s.company_name,
        s.location,
        s.salary_min,
        s.salary_max,
        s.created_at,
        s.matched_skills,
        s.skills_matched_count,
        s.raw_score,

        -- Final score: what % of the max possible score did this job hit?
        -- least() caps it at 100 in case of any rounding edge case
        least(
            round(s.raw_score * 100.0 / m.max_score, 1),
            100
        )                                                    as match_score_pct,


        case
            when round(s.raw_score * 100.0 / m.max_score, 1) >= 60 then 'Strong Match'
            when round(s.raw_score * 100.0 / m.max_score, 1) >= 35 then 'Good Match'
            when round(s.raw_score * 100.0 / m.max_score, 1) >= 15 then 'Partial Match'
            else 'Weak Match'
        end                                                  as match_label

    from scored s
    cross join max_possible m
    -- cross join here is intentional — max_possible is a single number,
    -- we just need to divide every row by it

)

select * from final
order by match_score_pct desc