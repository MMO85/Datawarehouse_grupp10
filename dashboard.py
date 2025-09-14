import streamlit as st
import pandas as pd
import plotly.express as px
from connect_data_warehouse import query_all_job_listings

# --- Ladda data ---
all_data = query_all_job_listings()
df_all = pd.concat(all_data.values(), ignore_index=True)

# --- Streamlit Layout ---
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")
st.title("HR Analytics Dashboard")

# ----------------------------
# 🔹 Skapa huvudflikar
# ----------------------------
tabs = st.tabs(["Översikt", "Bygg & Anläggning", "Kultur/Media/Design", "Pedagogik"])

# ----------------------------
# Tab 1: Översikt
# ----------------------------
with tabs[0]:
    st.header("Översikt (alla tabeller)")

    col1, col2, col3 = st.columns(3)
    col1.metric("Totalt antal annonser", int(df_all["VACANCIES"].sum()))
    col2.metric("Unika yrken", df_all["OCCUPATION"].nunique())
    col3.metric("Genomsnittlig relevans", round(df_all["RELEVANCE"].mean(), 2))

    st.subheader("Vacancies per Occupation Field")
    field_summary = df_all.groupby("OCCUPATION_FIELD")["VACANCIES"].sum().reset_index()
    fig_fields = px.bar(field_summary, x="OCCUPATION_FIELD", y="VACANCIES", text="VACANCIES")
    fig_fields.update_layout(xaxis_tickangle=0, xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_fields, use_container_width=True)

    st.subheader("Topp 10 yrken (alla tabeller)")
    top_jobs = (
        df_all.groupby("OCCUPATION")["VACANCIES"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig_top = px.bar(top_jobs, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig_top.update_layout(xaxis_tickangle=0, xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_top, use_container_width=True)

# ----------------------------
# Tab 2: Bygg & Anläggning
# ----------------------------
with tabs[1]:
    st.header("Bygg & Anläggning")
    df_bygg = all_data["MART_BYGG_OCH_ANLAGGNING"]
    st.metric("Antal annonser", int(df_bygg["VACANCIES"].sum()))

    top_10 = df_bygg.groupby("OCCUPATION")["VACANCIES"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_bygg = px.bar(top_10, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig_bygg.update_layout(xaxis_tickangle=0, xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_bygg, use_container_width=True)

    st.dataframe(df_bygg)

# ----------------------------
# Tab 3: Kultur/Media/Design
# ----------------------------
with tabs[2]:
    st.header("Kultur / Media / Design")
    df_kultur = all_data["MART_KULTUR_MEDIA_DESIGN"]
    st.metric("Antal annonser", int(df_kultur["VACANCIES"].sum()))

    top_10 = df_kultur.groupby("OCCUPATION")["VACANCIES"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_kultur = px.bar(top_10, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig_kultur.update_layout(xaxis_tickangle=0, xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_kultur, use_container_width=True)

    st.dataframe(df_kultur)

# ----------------------------
# Tab 4: Pedagogik
# ----------------------------
with tabs[3]:
    st.header("Pedagogik")
    df_pedagogik = all_data["MART_PEDAGOGIK"]
    st.metric("Antal annonser", int(df_pedagogik["VACANCIES"].sum()))

    top_10 = df_pedagogik.groupby("OCCUPATION")["VACANCIES"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_pedagogik = px.bar(top_10, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig_pedagogik.update_layout(xaxis_tickangle=0, xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_pedagogik, use_container_width=True)

    st.dataframe(df_pedagogik)