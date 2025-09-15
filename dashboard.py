import streamlit as st
import pandas as pd
import plotly.express as px
from connect_data_warehouse import query_all_job_listings

# ----------------------------
# Ladda data
# ----------------------------
all_data = query_all_job_listings()
df = pd.concat(all_data.values(), ignore_index=True)

# Säkerställ datatyper
df["APPLICATION_DEADLINE"] = pd.to_datetime(df["APPLICATION_DEADLINE"], errors="coerce")

# ----------------------------
# Layout
# ----------------------------
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")
st.title("HR Analytics Dashboard")

tabs = st.tabs(["Översikt", "Annons-sök & arbetsgivare", "Trender & mönster"])

# ----------------------------
# Flik 1: Översikt
# ----------------------------
with tabs[0]:
    st.header("📊 Översikt")
    st.markdown("""
    <div style="background-color:#2c3e50; padding:15px; border-radius:8px; 
                max-width:900px; margin-bottom:20px; color:#ffffff;">
    <p style="font-size:16px; line-height:1.6; text-align:justify;">
    Den här dashboarden ger en översikt över aktuella platsannonser från Arbetsförmedlingen, 
    indelade efter region och yrkesområde. Syftet är att hjälpa 
    rekryterare och talent acquisition-specialister att snabbt få insikter om arbetsmarknaden. 

    Här kan du se nyckeltal för antal annonser, antal tjänster, 
    vanligaste yrken samt topp arbetsgivare inom valt område.
    </p>
    </div>
    """, unsafe_allow_html=True)

    filter_col, spacer, result_col = st.columns([1, 0.3, 3])

    with filter_col:
        regions = sorted(df["WORKPLACE_REGION"].dropna().unique())
        default_region = "Stockholms län" if "Stockholms län" in regions else regions[0]
        selected_region = st.selectbox(
            "📍 Välj region", regions, index=regions.index(default_region), key="region_tab1"
        )
        df_region = df[df["WORKPLACE_REGION"] == selected_region]

        occ_fields = sorted(df_region["OCCUPATION_FIELD"].dropna().unique())
        selected_field = st.selectbox("🗂️ Välj yrkesområde", occ_fields, key="field_tab1")
        df_filtered = df_region[df_region["OCCUPATION_FIELD"] == selected_field]

    with result_col:
        st.subheader(f"KPIer för {selected_field} i {selected_region}")

        if not df_filtered.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("📑 Antal annonser", len(df_filtered))
            col2.metric("👥 Totalt antal tjänster", int(df_filtered["VACANCIES"].sum()))
            col3.metric("🏢 Antal arbetsgivare", df_filtered["EMPLOYER_NAME"].nunique())

            top_job = df_filtered.groupby("OCCUPATION")["VACANCIES"].sum().idxmax()
            st.markdown("**👷 Mest annonserade yrke**")
            st.markdown(
                f"<p style='font-size:25px; font-weight:normal; margin-top:-10px'>{top_job}</p>",
                unsafe_allow_html=True
            )

            top_employer = df_filtered.groupby("EMPLOYER_NAME")["VACANCIES"].sum().idxmax()
            st.markdown("**🏢 Topp arbetsgivare**")
            st.markdown(
                f"<p style='font-size:25px; font-weight:normal; margin-top:-10px'>{top_employer}</p>",
                unsafe_allow_html=True
            )

        else:
            st.info("Ingen data för vald kombination av filter.")

# ----------------------------
# Flik 2: Annons-sök & arbetsgivare
# ----------------------------
with tabs[1]:
    st.header("🔎 Annons-sök & arbetsgivarinformation")
    st.markdown("""
    <div style="background-color:#2c3e50; padding:15px; border-radius:8px; 
                max-width:900px; margin-bottom:20px; color:#ffffff;">
    <p style="font-size:16px; line-height:1.6; text-align:justify;">
    I den här fliken kan du söka dig ner på detaljnivå. 
    Börja med att välja region och yrkesområde, och fortsätt sedan till yrke och arbetsgivare. 
    Du kan därefter granska enskilda annonser med detaljer som tjänstetyp, 
    varaktighet, lön och hela annonstexten.
    </p>
    </div>
    """, unsafe_allow_html=True)

    filter_col, spacer, result_col = st.columns([1, 0.3, 3])

    with filter_col:
        regions = sorted(df["WORKPLACE_REGION"].dropna().unique())
        default_region = "Stockholms län" if "Stockholms län" in regions else regions[0]
        selected_region = st.selectbox(
            "📍 Välj region", regions, index=regions.index(default_region), key="region_tab2"
        )
        df_region = df[df["WORKPLACE_REGION"] == selected_region]

        if not df_region.empty:
            occ_fields = sorted(df_region["OCCUPATION_FIELD"].dropna().unique())
            selected_field = st.selectbox("🗂️ Välj yrkesområde", occ_fields, key="field_tab2")
            df_field = df_region[df_region["OCCUPATION_FIELD"] == selected_field]

            if not df_field.empty:
                occupations = sorted(df_field["OCCUPATION"].dropna().unique())
                selected_occupation = st.selectbox("👷 Välj yrke", occupations, key="occ_tab2")
                df_occ = df_field[df_field["OCCUPATION"] == selected_occupation]

                if not df_occ.empty:
                    employers = sorted(df_occ["EMPLOYER_NAME"].dropna().unique())
                    selected_employer = st.selectbox("🏢 Välj arbetsgivare", employers, key="employer_tab2")
                    df_employer = df_occ[df_occ["EMPLOYER_NAME"] == selected_employer]

    with result_col:
        if not df_region.empty and not df_field.empty and not df_occ.empty and not df_employer.empty:
            num_ads = len(df_employer)
            st.markdown(
                f"### 📋 {num_ads} annons(er) för **{selected_occupation}** i **{selected_region}** – {selected_employer}"
            )

            df_display = df_employer.copy()
            df_display["APPLICATION_DEADLINE"] = df_display["APPLICATION_DEADLINE"].dt.strftime("%Y-%m-%d")
            st.dataframe(
                df_display[["HEADLINE", "EMPLOYMENT_TYPE", "DURATION", "APPLICATION_DEADLINE"]],
                use_container_width=True,
            )

            selected_ad = st.selectbox("📄 Välj annons", df_employer["HEADLINE"].unique(), key="ad_tab2")
            ad_details = df_employer[df_employer["HEADLINE"] == selected_ad].iloc[0]

            st.markdown(f"## {ad_details['HEADLINE']}")

            col1, spacer, col2 = st.columns([1, 0.3, 1])
            with col1:
                st.write(f"**Arbetsgivare:** {ad_details['EMPLOYER_NAME']}")
                st.write(f"**Region:** {ad_details['WORKPLACE_REGION']}")
                st.write(f"**Yrkesområde:** {ad_details['OCCUPATION_FIELD']}")
                st.write(f"**Yrke:** {ad_details['OCCUPATION']}")
            with col2:
                st.write(f"**Anställningstyp:** {ad_details['EMPLOYMENT_TYPE']}")
                st.write(f"**Varaktighet:** {ad_details['DURATION']}")
                st.write(f"**Lön:** {ad_details['SALARY_TYPE']}")
                st.write(
                    f"**Deadline:** {ad_details['APPLICATION_DEADLINE'].strftime('%Y-%m-%d') if pd.notnull(ad_details['APPLICATION_DEADLINE']) else '-'}"
                )

            st.markdown("### 📝 Annonstext")
            st.write(ad_details["JOB_DESCRIPTION"])
        else:
            st.info("Ingen annons finns för vald kombination av filter.")

# ----------------------------
# Flik 3: Trender & mönster
# ----------------------------
with tabs[2]:
    st.header("📈 Trender & Mönster")
    st.markdown("""
    <div style="background-color:#2c3e50; padding:15px; border-radius:8px; 
                max-width:900px; margin-bottom:20px; color:#ffffff;">
    <p style="font-size:16px; line-height:1.6; text-align:justify;">
    Här kan du utforska trender i arbetsmarknaden. 
    Se vilka arbetsgivare som dominerar, hur tjänsterna fördelas över olika anställningstyper, 
    och följa utvecklingen över tid med hjälp av ansökningsdeadlines.
    </p>
    </div>
    """, unsafe_allow_html=True)

    filter_col, spacer, result_col = st.columns([1, 0.3, 3])

    with filter_col:
        regions = sorted(df["WORKPLACE_REGION"].dropna().unique())
        default_region = "Stockholms län" if "Stockholms län" in regions else regions[0]
        selected_region = st.selectbox(
            "📍 Välj region", regions, index=regions.index(default_region), key="region_tab3"
        )
        df_region = df[df["WORKPLACE_REGION"] == selected_region]

        if not df_region.empty:
            occ_fields = sorted(df_region["OCCUPATION_FIELD"].dropna().unique())
            selected_field = st.selectbox("🗂️ Välj yrkesområde", occ_fields, key="field_tab3")
            df_filtered = df_region[df_region["OCCUPATION_FIELD"] == selected_field]
        else:
            df_filtered = pd.DataFrame()

    with result_col:
        if not df_filtered.empty:
            st.subheader(f"Analyser för {selected_field} i {selected_region}")

            # 1. Topp arbetsgivare
            top_employers = (
                df_filtered.groupby("EMPLOYER_NAME")["VACANCIES"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            fig1 = px.bar(
                top_employers,
                x="EMPLOYER_NAME",
                y="VACANCIES",
                text="VACANCIES",
                title="🏢 Topp arbetsgivare",
            )
            fig1.update_traces(
                textposition="outside",
                hovertemplate="<b>Arbetsgivare:</b> %{x}<br><b>Tjänster:</b> %{y}<extra></extra>"
            )
            fig1.update_layout(xaxis_tickangle=-45, xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig1, use_container_width=True)

            # 2. Fördelning av anställningstyper
            type_dist = df_filtered.groupby("EMPLOYMENT_TYPE")["VACANCIES"].sum().reset_index()
            fig2 = px.pie(
                type_dist,
                names="EMPLOYMENT_TYPE",
                values="VACANCIES",
                hole=0.4,
                title="📝 Fördelning av anställningstyper",
            )
            fig2.update_traces(
                hovertemplate="<b>Anställningstyp:</b> %{label}<br><b>Tjänster:</b> %{value}<extra></extra>"
            )
            st.plotly_chart(fig2, use_container_width=True)

            # 3. Antal tjänster över deadlines
            trend = (
                df_filtered.groupby(df_filtered["APPLICATION_DEADLINE"].dt.date)["VACANCIES"]
                .sum()
                .reset_index()
            )
            fig3 = px.line(
                trend,
                x="APPLICATION_DEADLINE",
                y="VACANCIES",
                markers=True,
                title="📅 Antal tjänster över ansökningsdeadlines",
            )
            fig3.update_traces(
                hovertemplate="<b>Datum:</b> %{x}<br><b>Tjänster:</b> %{y}<extra></extra>"
            )
            fig3.update_layout(xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig3, use_container_width=True)

        else:
            st.info("Ingen data för vald kombination av filter.")