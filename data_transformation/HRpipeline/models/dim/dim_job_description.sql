with src_job_description as (select * from {{ ref('src_job_description') }})

select
    id as job_description_id,
    headline,
    description_text,
    description_html
from src_job_description