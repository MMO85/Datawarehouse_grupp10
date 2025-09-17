# Datawarehouse_grupp10
HR pipeline
📊 HR Analytics PoC — Modern Data Stack

Detta projekt är ett Proof of Concept, där vi bygger en pipeline för att hämta, transformera och visualisera jobbannonser från Jobtech API med hjälp av en modern data stack.

🛠️ Teknikstack

Snowflake – Data warehouse

dlt – Data ingestion från Jobtech API

dbt – Transformationer (staging → warehouse → mart)

Streamlit – Dashboard med KPI:er

GitHub Actions – CI för dbt


👥 Teamroller


🔗 Flöde: DLT → DBT → Streamlit
flowchart TD
    A[Jobtech API] -->|DLT pipeline| B[Snowflake STAGING]
    B -->|dbt models| C[Snowflake WAREHOUSE]
    C -->|dbt marts| D[Snowflake MART]
    D -->|SQL queries| E[Streamlit Dashboard]

🚀 Flöde steg-för-steg
⚡ DLT (Data Loading Tool)

Skript: dlt_pipeline/loadjob_ads.py

Hämtar jobbannonser från Jobtech Search API.

Stöder occupation_field som filter + pagination.!

Laddar data till Snowflake → HR_JOBS.STAGING.job_ads.

⚡ DBT (Data Build Tool)

Staging → stg_job_ads.sql

Rensar och standardiserar kolumner.

Warehouse →

fact_job_ads.sql (fakta-tabell)

dim_location.sql (dimension-tabell för städer)

Mart →

mart_job_ads_by_field.sql (aggregeringar per yrkesfält).

Tester i schema.yml:

not_null, unique, accepted_values, relationships.

Dokumentation genereras med dbt docs.

⚡ Streamlit

Dashboard: streamlit_app/app.py

Kopplar till Snowflake (MART-schema).

Visar KPI:er:

Totalt antal annonser

Topp 10 yrken

Topp 10 städer

Fördelning av anställningstyper

Interaktiv meny för att välja occupation_field.

📂 Projektstruktur
├── dlt_pipeline/          # dlt pipelines
│   └── load_job_ads.py
├── dbt_project/           # dbt-projekt (staging → warehouse → mart)
│   ├── models/
│   │   ├── staging/
│   │   ├── warehouse/
│   │   └── mart/
│   └── profiles.yml.example
├── streamlit_app/         # Dashboard
│   └── app.py
├── infra/                 # Infrastruktur
│   └── snowflake_setup.sql
├── .github/workflows/     # CI/CD
│   └── ci.yml
├── docs/                  # Dokumentation & checklist
├── .env.example
├── requirements.txt
└── README.md

🔑 Installation & körning
1. Klona repo och installera beroenden
git clone <repo-url>
cd hr-analytics-poc
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

2. Miljövariabler

Kopiera .env.example → .env och fyll i:

Snowflake credentials

API-inställningar för Jobtech

3. Snowflake-setup

Kör SQL i infra/snowflake_setup.sql för att skapa:

Warehouse

Database & Schemas (STAGING, WAREHOUSE, MART)

Roller & Användare

4. Ladda data (dlt)
python dlt_pipeline/load_job_ads.py

5. Kör dbt
cd dbt_project
dbt deps
dbt debug
dbt run
dbt test

6. Kör dashboard
streamlit run streamlit_app/app.py

✅ Bonusar
🔹 Task 5 — dbt dokumentation & datakvalitet

Extra tester (accepted_values, relationships).

Beskrivningar i schema.yml.

dbt docs generate + dbt docs serve för att visa lineage.

🔹 Task 6 — Orkestrering (Dagster)

Pipeline som kör ingestion (dlt) + transformation (dbt).

Körs två gånger för att analysera trender i data (ex. jämföra antal annonser dag 1 vs dag 2).

📈 Resultat

Full pipeline: Jobtech API → Snowflake → dbt → Streamlit.

Dashboarden visar meningsfulla KPI:er för HR-analys.

Datakvalitet säkras med dbt-tests.

CI via GitHub Actions kör dbt compile + tests på varje PR.

(Bonus) Dagster pipeline för orkestrering.
