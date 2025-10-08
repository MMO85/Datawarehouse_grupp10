-- this is an extract of the model

with STG_HR_JOBS as (select * from {{ source('HR_JOBS', 'stg_ads') }})

select
    id,
    COALESCE(employment_type__label, 'Ospecifierad') as employment_type,
    COALESCE(salary_type__label, 'Ospecifierad') as salary_type,
    COALESCE(duration__label, 'Ospecifierad') as duration,
    COALESCE(experience_required, FALSE) as experience_required,
    COALESCE(access_to_own_car, FALSE) as access_to_own_car,
    COALESCE(driving_license_required, FALSE) as driving_license_required,
    scope_of_work__min as scope_of_work_min,
    scope_of_work__max as scope_of_work_max,
    employer__name as employer_name,
    occupation__label as occupation,
    COALESCE(number_of_vacancies, 1) as vacancies,
    relevance,
    application_deadline
from STG_HR_JOBS