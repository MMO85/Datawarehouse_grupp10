
with HR_JOBS as (select * from {{ ref('src_job_ads') }})

select
    id as job_description_id,
    {{ dbt_utils.generate_surrogate_key(['experience_required', 'access_to_own_car', 'driving_license_required'])}} as auxilliary_id,
    {{ dbt_utils.generate_surrogate_key(['employer_name'])}} as employer_id,
    {{ dbt_utils.generate_surrogate_key(['employment_type', 'salary_type', 'duration', 'scope_of_work_min', 'scope_of_work_max'])}} as job_details_id,
    {{ dbt_utils.generate_surrogate_key(['occupation']) }} as occupation_id,
    vacancies,
    relevance,
    application_deadline
from HR_JOBS