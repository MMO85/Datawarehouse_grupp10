-- this is an extract of the model

with HR_JOBS as (select * from {{ ref('src_HR_JOBS') }})

select
    {{ dbt_utils.generate_surrogate_key(['occupation__label']) }} as occupation_id,
    occupation__label as occupation,
    occupation_field__label as occupation_field,
    vacancies,
    relevance,
    APPLICATION_DEADLINE 
from HR_JOBS
