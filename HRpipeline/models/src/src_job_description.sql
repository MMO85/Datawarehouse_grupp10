with STG_HR_JOBS as (select * from {{ source('HR_JOBS', 'stg_ads') }})

select
    id,
    headline,
    COALESCE(description__text, 'Beskrivning saknas') as description_text,
    COALESCE(description__text_formatted, 'Beskrivning saknas') as description_html
from STG_HR_JOBS
