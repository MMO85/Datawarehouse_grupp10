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
# Flik 1: Översikt
# ----------------------------
with tabs[0]:
    st.header("Översikt (alla tabeller)")

    # KPI-beräkningar
    total_annons = len(df_all)
    total_tjanster = int(df_all["VACANCIES"].sum())
    unika_yrken = df_all["OCCUPATION"].nunique()
    antal_yrkesomraden = df_all["OCCUPATION_FIELD"].nunique()
    storsta_yrkesomrade = df_all.groupby("OCCUPATION_FIELD")["VACANCIES"].sum().idxmax()
    mest_annons_yrke = df_all.groupby("OCCUPATION")["VACANCIES"].sum().idxmax()

    # Layout med 6 KPI-boxar
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("Totalt antal annonser", total_annons)
    col2.metric("Totalt antal tjänster", total_tjanster)
    col3.metric("Antal unika yrken", unika_yrken)
    col4.metric("Antal yrkesområden", antal_yrkesomraden)
    col5.metric("Största yrkesområde", storsta_yrkesomrade)
    col6.metric("Mest annonserade yrke", mest_annons_yrke)

    st.subheader("Antal annonser per yrkesområde")
    field_summary = df_all.groupby("OCCUPATION_FIELD")["VACANCIES"].sum().reset_index()
    fig_fields = px.bar(field_summary, x="OCCUPATION_FIELD", y="VACANCIES", text="VACANCIES")
    fig_fields.update_layout(
        xaxis_tickangle=0,
        xaxis={'categoryorder':'total descending'},
        xaxis_title=None,
        yaxis_title=None
    )
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
    fig_top.update_layout(
        xaxis_tickangle=-45,
        xaxis={'categoryorder':'total descending'},
        xaxis_title=None,
        yaxis_title=None
    )
    st.plotly_chart(fig_top, use_container_width=True)

# ----------------------------
# Flik 2: Bygg & Anläggning
# ----------------------------
with tabs[1]:
    st.header("Bygg & Anläggning")
    df_bygg = all_data["MART_BYGG_OCH_ANLAGGNING"]
    st.metric("Antal annonser", int(df_bygg["VACANCIES"].sum()))

    top_10 = df_bygg.groupby("OCCUPATION")["VACANCIES"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_bygg = px.bar(top_10, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig_bygg.update_layout(
        xaxis_tickangle=0,
        xaxis={'categoryorder':'total descending'},
        xaxis_title=None,
        yaxis_title=None
    )
    st.plotly_chart(fig_bygg, use_container_width=True)

    st.dataframe(df_bygg)

# ----------------------------
# Flik 3: Kultur/Media/Design
# ----------------------------
with tabs[2]:
    st.header("Kultur / Media / Design")
    df_kultur = all_data["MART_KULTUR_MEDIA_DESIGN"]
    st.metric("Antal annonser", int(df_kultur["VACANCIES"].sum()))

    top_10 = df_kultur.groupby("OCCUPATION")["VACANCIES"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_kultur = px.bar(top_10, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig_kultur.update_layout(
        xaxis_tickangle=0,
        xaxis={'categoryorder':'total descending'},
        xaxis_title=None,
        yaxis_title=None
    )
    st.plotly_chart(fig_kultur, use_container_width=True)

    st.dataframe(df_kultur)

# ----------------------------
# Flik 4: Pedagogik
# ----------------------------
with tabs[3]:
    st.header("Pedagogik")
    df_pedagogik = all_data["MART_PEDAGOGIK"]
    st.metric("Antal annonser", int(df_pedagogik["VACANCIES"].sum()))

    top_10 = df_pedagogik.groupby("OCCUPATION")["VACANCIES"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_pedagogik = px.bar(top_10, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig_pedagogik.update_layout(
        xaxis_tickangle=0,
        xaxis={'categoryorder':'total descending'},
        xaxis_title=None,
        yaxis_title=None
    )
    st.plotly_chart(fig_pedagogik, use_container_width=True)

    st.dataframe(df_pedagogik)