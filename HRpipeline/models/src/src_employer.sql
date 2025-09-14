with STG_HR_JOBS as (select * from {{ source('HR_JOBS', 'stg_ads') }})

select
    employer__name as employer_name,
    COALESCE(employer__workplace, 'Ospecifierad') AS employer_workplace,
    COALESCE(employer__organization_number, 'Ospecifierat') AS employer_organization_number,
    {{ capitalize_first_letter("COALESCE(workplace_address__street_address, 'Ospecifierad')") }} as workplace_street_address,
    {{ capitalize_first_letter("COALESCE(workplace_address__region, 'Ospecifierad')") }} as workplace_region,
    {{ capitalize_first_letter("COALESCE(workplace_address__postcode, 'Ospecifierad')")}} as workplace_postcode,
    {{ capitalize_first_letter("COALESCE(workplace_address__city, 'Ospecifierad')") }} as workplace_city,
    {{ capitalize_first_letter("COALESCE(workplace_address__country, 'Ospecifierad')") }} as workplace_country
from STG_HR_JOBS 