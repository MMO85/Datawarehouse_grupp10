with STG_HR_JOBS as (select * from {{ source('HR_JOBS', 'stg_ads') }})

select
    occupation_group__concept_id as occupation_group_id,
    occupation_field__concept_id as occupation_field_id,
    occupation__label as occupation,
    occupation_group__label as occupation_group,
    occupation_field__label as occupation_field
from STG_HR_JOBS 