USE ROLE ROLE_DBT;             -- یا نقشی که USAGE دارد
USE WAREHOUSE COMPUTE_WH;
USE DATABASE HR_JOBS;

-- همه‌ی جدول‌های اسکیمای STAGING
SHOW TABLES IN SCHEMA STAGING;

-- (جایگزین قابل فیلتر)
SELECT table_schema, table_name
FROM HR_JOBS.INFORMATION_SCHEMA.TABLES
WHERE table_schema IN ('STAGING','DWH','MART')
ORDER BY table_schema, table_name;

-- اگر View هم داری:
SHOW VIEWS IN SCHEMA STAGING;

-- دیدن ستون‌های یک جدول مشخص:
DESCRIBE TABLE HR_JOBS.STAGING.TECHNICAL_FIELD_JOB_ADS;
