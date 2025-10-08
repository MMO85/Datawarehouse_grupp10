with STG_HR_JOBS as (select * from {{ source('HR_JOBS', 'stg_ads') }})

select
    COALESCE(employment_type__label, 'Ospecifierad') as employment_type,
    COALESCE(salary_type__label, 'Ospecifierad') as salary_type,
    COALESCE(duration__label, 'Ospecifierad') as duration,
    scope_of_work__min as scope_of_work_min,
    scope_of_work__max as scope_of_work_max
from STG_HR_JOBS 