
with
    fct_job_ads as (select * from {{ ref('fct_job_ads') }}),
    dim_occupation as (select * from {{ ref('dim_occupation') }}),
    dim_job_details as (select * from {{ ref('dim_job_details') }}),
    dim_job_description as (select * from {{ ref('dim_job_description') }}),
    dim_employer as (select * from {{ ref('dim_employer') }}),
    dim_auxilliary_attributes as (select * from {{ ref('dim_auxilliary_attributes') }})
select
    f.vacancies,
    o.occupation,
    o.occupation_field,
    f.application_deadline,
    j.headline,
    j.description_text as job_description,
    j.description_html as job_description_html,
    e.employer_name,
    d.employment_type,
    d.salary_type,
    d.duration,
    e.workplace_region,
    j.job_description_id

from fct_job_ads f
left join dim_occupation o on o.occupation_id = f.occupation_id
left join dim_job_details d on d.job_details_id = f.job_details_id
left join dim_job_description j on j.job_description_id = f.job_description_id
left join dim_employer e on e.employer_id = f.employer_id
left join dim_auxilliary_attributes a on a.auxilliary_id = f.auxilliary_id

where o.occupation_field = 'Bygg och anläggning'