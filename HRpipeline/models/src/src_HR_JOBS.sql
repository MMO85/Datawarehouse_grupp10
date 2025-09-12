-- this is an extract of the model

with STG_HR_JOBS as (select * from {{ source('HR_JOBS', 'stg_ads') }})

select
  occupation__label,
  occupation_field__label,
  number_of_vacancies as vacancies,
  relevance,
  application_deadline
from STG_HR_JOBS
order by application_deadline