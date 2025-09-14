with src_job_details as (select * from {{ ref('src_job_details') }})

select
    {{ dbt_utils.generate_surrogate_key(['employment_type', 'salary_type', 'duration', 'scope_of_work_min', 'scope_of_work_max'])}} as job_details_id,
    max(employment_type) as employment_type,
    max(salary_type) as salary_type,
    max(duration) as duration,
    max(scope_of_work_min) as scope_of_work_min,
    max(scope_of_work_max) as scope_of_work_max
from src_job_details
group by job_details_id
