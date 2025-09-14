import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd

def query_all_job_listings():
    load_dotenv()

    tables = [
        "MART_BYGG_OCH_ANLAGGNING",
        "MART_KULTUR_MEDIA_DESIGN",
        "MART_PEDAGOGIK"
    ]

    data = {}

    with snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    ) as conn:

        for table in tables:
            query = f"""
                SELECT *
                FROM {table}
            """
            df = pd.read_sql(query, conn)
            data[table] = df

    return data

all_data = query_all_job_listings()

df_bygg = all_data["MART_BYGG_OCH_ANLAGGNING"]
df_kultur = all_data["MART_KULTUR_MEDIA_DESIGN"]
df_pedagogik = all_data["MART_PEDAGOGIK"]

print(df_bygg.head())
print(df_kultur.head())
print(df_pedagogik.head())