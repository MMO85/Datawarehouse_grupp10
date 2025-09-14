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
# Skapa huvudflikar
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

    # KPI-rutor
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col1.metric("Totalt antal annonser", total_annons)
    col2.metric("Totalt antal tjänster", total_tjanster)
    col3.metric("Antal unika yrken", unika_yrken)
    col4.metric("Antal yrkesområden", antal_yrkesomraden)
    col5.metric("Största yrkesområde", storsta_yrkesomrade)
    col6.metric("Mest annonserade yrke", mest_annons_yrke)

    # Diagram 1 - Yrkesområden
    st.subheader("Antal tjänster per yrkesområde")
    field_summary = df_all.groupby("OCCUPATION_FIELD")["VACANCIES"].sum().reset_index()
    fig_fields = px.bar(field_summary, x="OCCUPATION_FIELD", y="VACANCIES", text="VACANCIES")
    fig_fields.update_traces(hovertemplate="<b>Yrkesområde:</b> %{x}<br><b>Antal tjänster:</b> %{y}<extra></extra>")
    fig_fields.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'},
                        xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig_fields, use_container_width=True)

    # Diagram 2 - Topp 10 yrken
    st.subheader("Topp 10 yrken (alla tabeller)")
    top_jobs = df_all.groupby("OCCUPATION")["VACANCIES"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_top = px.bar(top_jobs, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig_top.update_traces(hovertemplate="<b>Yrke:</b> %{x}<br><b>Antal tjänster:</b> %{y}<extra></extra>")
    fig_top.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'},
                        xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig_top, use_container_width=True)


# ----------------------------
# Flik 2: Bygg & Anläggning
# ----------------------------
with tabs[1]:
    st.header("Bygg & Anläggning")
    df_bygg = all_data["MART_BYGG_OCH_ANLAGGNING"]

    # KPIer
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Antal annonser", len(df_bygg))
    col2.metric("Totalt antal tjänster", int(df_bygg["VACANCIES"].sum()))
    col3.metric("Antal unika yrken", df_bygg["OCCUPATION"].nunique())
    top_job = df_bygg.groupby("OCCUPATION")["VACANCIES"].sum().idxmax()
    col4.metric("Mest annonserade yrke", top_job)

    # Diagram 1 - Topp 10 yrken
    st.subheader("Topp 10 yrken")
    top_10 = df_bygg.groupby("OCCUPATION")["VACANCIES"].sum().sort_values(ascending=False).head(10).reset_index()
    fig1 = px.bar(top_10, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig1.update_traces(hovertemplate="<b>Yrke:</b> %{x}<br><b>Antal annonser:</b> %{y}<extra></extra>")
    fig1.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'},
                    xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig1, use_container_width=True)

    # Diagram 2 - Fördelning per yrkesgrupp
    st.subheader("Fördelning per yrkesgrupp")
    group_summary = df_bygg.groupby("OCCUPATION_GROUP")["VACANCIES"].sum().reset_index()
    fig2 = px.bar(group_summary, x="OCCUPATION_GROUP", y="VACANCIES", text="VACANCIES")
    fig2.update_traces(hovertemplate="<b>Yrkesgrupp:</b> %{x}<br><b>Antal annonser:</b> %{y}<extra></extra>")
    fig2.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'},
                    xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig2, use_container_width=True)

    # Diagram 3 - Trend över ansökningsdeadlines
    st.subheader("Trend över ansökningsdeadlines")
    trend = df_bygg.groupby(df_bygg["APPLICATION_DEADLINE"].dt.date)["VACANCIES"].sum().reset_index()
    fig3 = px.line(trend, x="APPLICATION_DEADLINE", y="VACANCIES", markers=True)
    fig3.update_traces(hovertemplate="<b>Datum:</b> %{x}<br><b>Antal annonser:</b> %{y}<extra></extra>")
    fig3.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig3, use_container_width=True)

    # Data
    st.subheader("Rådata")
    st.dataframe(df_bygg)


# ----------------------------
# Flik 3: Kultur/Media/Design
# ----------------------------
with tabs[2]:
    st.header("Kultur / Media / Design")
    df_kultur = all_data["MART_KULTUR_MEDIA_DESIGN"]

    # KPIer
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Antal annonser", len(df_kultur))
    col2.metric("Totalt antal tjänster", int(df_kultur["VACANCIES"].sum()))
    col3.metric("Antal unika yrken", df_kultur["OCCUPATION"].nunique())
    top_job = df_kultur.groupby("OCCUPATION")["VACANCIES"].sum().idxmax()
    col4.metric("Mest annonserade yrke", top_job)

    # Diagram 1 - Topp 10 yrken
    st.subheader("Topp 10 yrken")
    top_10 = df_kultur.groupby("OCCUPATION")["VACANCIES"].sum().sort_values(ascending=False).head(10).reset_index()
    fig1 = px.bar(top_10, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig1.update_traces(hovertemplate="<b>Yrke:</b> %{x}<br><b>Antal annonser:</b> %{y}<extra></extra>")
    fig1.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'},
                    xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig1, use_container_width=True)

    # Diagram 2 - Fördelning per yrkesgrupp
    st.subheader("Fördelning per yrkesgrupp")
    group_summary = df_kultur.groupby("OCCUPATION_GROUP")["VACANCIES"].sum().reset_index()
    fig2 = px.bar(group_summary, x="OCCUPATION_GROUP", y="VACANCIES", text="VACANCIES")
    fig2.update_traces(hovertemplate="<b>Yrkesgrupp:</b> %{x}<br><b>Antal annonser:</b> %{y}<extra></extra>")
    fig2.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'},
                    xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig2, use_container_width=True)

    # Diagram 3 - Trend över ansökningsdeadlines
    st.subheader("Trend över ansökningsdeadlines")
    trend = df_kultur.groupby(df_kultur["APPLICATION_DEADLINE"].dt.date)["VACANCIES"].sum().reset_index()
    fig3 = px.line(trend, x="APPLICATION_DEADLINE", y="VACANCIES", markers=True)
    fig3.update_traces(hovertemplate="<b>Datum:</b> %{x}<br><b>Antal annonser:</b> %{y}<extra></extra>")
    fig3.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig3, use_container_width=True)

    # Data
    st.subheader("Rådata")
    st.dataframe(df_kultur)


# ----------------------------
# Flik 4: Pedagogik
# ----------------------------
with tabs[3]:
    st.header("Pedagogik")
    df_pedagogik = all_data["MART_PEDAGOGIK"]

    # KPIer
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Antal annonser", len(df_pedagogik))
    col2.metric("Totalt antal tjänster", int(df_pedagogik["VACANCIES"].sum()))
    col3.metric("Antal unika yrken", df_pedagogik["OCCUPATION"].nunique())
    top_job = df_pedagogik.groupby("OCCUPATION")["VACANCIES"].sum().idxmax()
    col4.metric("Mest annonserade yrke", top_job)

    # Diagram 1 - Topp 10 yrken
    st.subheader("Topp 10 yrken")
    top_10 = df_pedagogik.groupby("OCCUPATION")["VACANCIES"].sum().sort_values(ascending=False).head(10).reset_index()
    fig1 = px.bar(top_10, x="OCCUPATION", y="VACANCIES", text="VACANCIES")
    fig1.update_traces(hovertemplate="<b>Yrke:</b> %{x}<br><b>Antal annonser:</b> %{y}<extra></extra>")
    fig1.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'},
                    xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig1, use_container_width=True)

    # Diagram 2 - Fördelning per yrkesgrupp
    st.subheader("Fördelning per yrkesgrupp")
    group_summary = df_pedagogik.groupby("OCCUPATION_GROUP")["VACANCIES"].sum().reset_index()
    fig2 = px.bar(group_summary, x="OCCUPATION_GROUP", y="VACANCIES", text="VACANCIES")
    fig2.update_traces(hovertemplate="<b>Yrkesgrupp:</b> %{x}<br><b>Antal annonser:</b> %{y}<extra></extra>")
    fig2.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'},
                    xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig2, use_container_width=True)

    # Diagram 3 - Trend över ansökningsdeadlines
    st.subheader("Trend över ansökningsdeadlines")
    trend = df_pedagogik.groupby(df_pedagogik["APPLICATION_DEADLINE"].dt.date)["VACANCIES"].sum().reset_index()
    fig3 = px.line(trend, x="APPLICATION_DEADLINE", y="VACANCIES", markers=True)
    fig3.update_traces(hovertemplate="<b>Datum:</b> %{x}<br><b>Antal annonser:</b> %{y}<extra></extra>")
    fig3.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig3, use_container_width=True)

    # Data
    st.subheader("Rådata")
    st.dataframe(df_pedagogik)