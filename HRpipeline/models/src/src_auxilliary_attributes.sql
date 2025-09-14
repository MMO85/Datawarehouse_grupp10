with STG_HR_JOBS as (select * from {{ source('HR_JOBS', 'stg_ads') }})

select
    COALESCE(experience_required, FALSE) as experience_required,
    COALESCE(access_to_own_car, FALSE) as access_to_own_car,
    COALESCE(driving_license_required, FALSE) as driving_license_required
from STG_HR_JOBS 