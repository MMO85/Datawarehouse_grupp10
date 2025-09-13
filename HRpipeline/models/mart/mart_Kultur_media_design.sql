with
    fct_HR_JOBS as (select * from {{ ref('fct_HR_JOBS') }}),
    dim_occupation as (select * from {{ ref('dim_occupation') }})
select
    f.vacancies,
    f.relevance,
    o.occupation,
    o.occupation_group,
    o.occupation_field,
    f.application_deadline,
from fct_HR_JOBS f
left join dim_occupation o on f.occupation_id = o.occupation_id
where o.occupation_field = 'Kultur, media, design'