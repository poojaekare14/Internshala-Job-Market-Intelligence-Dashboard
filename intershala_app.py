import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.write("Current Folder:", os.getcwd())
st.write("Files:", os.listdir())
st.set_page_config(
    page_title="Internshala Job Intelligence Dashboard",
    page_icon="💼",
    layout="wide"
)

@st.cache_data
def load_data():

    df = pd.read_csv(
       "dataset/internshala_jobs.csv"
    )

    df = df.drop_duplicates()

    return df

df = load_data()

st.title("💼 Internshala Job Intelligence Dashboard")

st.markdown(
"""
Analyze hiring trends, salaries, locations,
companies and skill demand from Internshala jobs.
"""
)

st.sidebar.header("Filters")
company = st.sidebar.multiselect(
    "Select Company",
    options=df["Company"].dropna().unique(),
    default=df["Company"].dropna().unique()
)
location = st.sidebar.multiselect(
    "Select Location",
    options=df["Location"].dropna().unique(),
    default=df["Location"].dropna().unique()
)
experience = st.sidebar.multiselect(
    "Select Experience",
    options=df["Experience"].dropna().unique(),
    default=df["Experience"].dropna().unique()
)
filtered_df = df[
    (df["Company"].isin(company)) &
    (df["Location"].isin(location)) &
    (df["Experience"].isin(experience))
]
total_jobs = len(filtered_df)

total_companies = filtered_df["Company"].nunique()

total_locations = filtered_df["Location"].nunique()

salary_numeric = (
    filtered_df["Salary"]
    .astype(str)
    .str.extract(r'(\d+)')[0]
)

salary_numeric = pd.to_numeric(
    salary_numeric,
    errors="coerce"
)

avg_salary = round(
    salary_numeric.mean(),
    0
)
c1,c2,c3,c4 = st.columns(4)

c1.metric("Total Jobs", total_jobs)

c2.metric("Companies", total_companies)

c3.metric("Locations", total_locations)

c4.metric("Avg Salary", f"{avg_salary}")
tabs = st.tabs([
    "📋 App Information",
    "📊 Overview",
    "🏢 Company Analysis",
    "🛠 Skills Analysis",
    "📍 Location Analysis",
    "💰 Salary Analysis",
    "📈 Experience Analysis",
    "💼 Job Role Analysis",
    "⬇ Download Center"
])
with tabs[0]:

    st.header("📋 App Information")

    st.subheader("Dataset Shape")
    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")

    st.markdown("---")

    st.subheader("Dataset Head")
    st.dataframe(df.head())

    st.markdown("---")

    st.subheader("Dataset Columns")
    st.write(df.columns.tolist())

    st.markdown("---")

    st.subheader("Missing Values")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(missing_df)

    st.markdown("---")

    st.subheader("Data Types")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })

    st.dataframe(dtype_df)

    st.markdown("---")

    st.subheader("Dataset Statistics")

    st.dataframe(df.describe(include="all"))

    st.markdown("---")

    st.subheader("Duplicate Records")

    st.write(f"Duplicate Rows: {df.duplicated().sum()}")

with tabs[1]:

    st.subheader("Job Distribution by Location")

    loc = (
        filtered_df["Location"]
        .value_counts()
        .reset_index()
    )

    fig = px.bar(
        loc,
        x="Location",
        y="count",
        title="Jobs by Location"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    top_companies = (
    filtered_df["Company"]
    .value_counts()
    .head(10)
    .reset_index()
    )

    fig2 = px.bar(
    top_companies,
    x="Company",
    y="count",
    title="Top Hiring Companies"
    )
    st.plotly_chart(
    fig2,
    use_container_width=True
    )
    st.info("""
    Observation:

    • Certain cities dominate job opportunities.

    • Few companies are hiring aggressively.

    • Opportunities are concentrated in specific regions.
    """)
    st.success("""
    Business Insights:

    • Job seekers should target high-demand cities.

    • Top hiring companies offer maximum opportunities.

    • Recruiters can benchmark hiring activity.
    """)
with tabs[2]:

    st.subheader("🏢 Company Analysis")

    comp = filtered_df["Company"].value_counts().head(15).reset_index()
    comp.columns = ["Company", "Jobs"]

    fig = px.bar(
        comp,
        x="Company",
        y="Jobs",
        title="Top Hiring Companies"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    Observation:
    • A few companies contribute a large share of job postings.
    • Hiring activity is concentrated among top recruiters.
    """)

    st.success("""
    Business Insight:
    • Students should prioritize applications to actively hiring companies.
    • Recruiters can benchmark their hiring volume against competitors.
    """)
with tabs[3]:

    st.subheader("🛠 Skills Analysis")

    skills_series = (
        filtered_df["Skills"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    skill_count = skills_series.value_counts().head(15).reset_index()
    skill_count.columns = ["Skill", "Count"]

    fig = px.bar(
        skill_count,
        x="Skill",
        y="Count",
        title="Most Demanded Skills"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    Observation:
    • Certain technical skills appear repeatedly across jobs.
    • Employers seek candidates with industry-relevant skill sets.
    """)

    st.success("""
    Business Insight:
    • Learning high-demand skills increases employability.
    • Training institutes can align courses with market demand.
    """)
with tabs[4]:

    st.subheader("📍 Location Analysis")

    location_count = (
        filtered_df["Location"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    location_count.columns = ["Location", "Jobs"]

    fig = px.pie(
        location_count,
        names="Location",
        values="Jobs",
        title="Jobs by Location",
        hole=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    Observation:
    • Job opportunities are concentrated in specific cities.
    • Major tech and business hubs dominate hiring.
    """)

    st.success("""
    Business Insight:
    • Job seekers can target cities with stronger job markets.
    • Companies can compare regional hiring trends.
    """)
salary_df = filtered_df.copy()

salary_df["Salary_Num"] = (
    salary_df["Salary"]
    .astype(str)
    .str.extract(r'(\d+)')[0]
)

salary_df["Salary_Num"] = pd.to_numeric(
    salary_df["Salary_Num"],
    errors="coerce"
)
with tabs[5]:

    st.subheader("💰 Salary Analysis")

    fig = px.histogram(
        salary_df,
        x="Salary_Num",
        nbins=20,
        title="Salary Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    top_salary = (
        salary_df
        .sort_values("Salary_Num", ascending=False)
        .head(10)
    )

    fig2 = px.bar(
        top_salary,
        x="Job Title",
        y="Salary_Num",
        title="Highest Paying Roles"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.info("""
    Observation:
    • Salary offerings vary significantly across roles.
    • Some positions command premium compensation.
    """)

    st.success("""
    Business Insight:
    • Candidates can focus on high-paying career paths.
    • Employers can benchmark salary competitiveness.
    """)
with tabs[6]:

    st.subheader("📈 Experience Analysis")

    exp = (
        filtered_df["Experience"]
        .value_counts()
        .reset_index()
    )

    exp.columns = ["Experience", "Jobs"]

    fig = px.bar(
        exp,
        x="Experience",
        y="Jobs",
        title="Experience Requirement Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    Observation:
    • Entry-level opportunities dominate the dataset.
    • Some jobs require prior industry experience.
    """)

    st.success("""
    Business Insight:
    • Freshers have a strong presence in the market.
    • Professionals can identify growth-oriented roles.
    """)
with tabs[7]:

    st.subheader("💼 Job Role Analysis")

    jobs = (
        filtered_df["Job Title"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    jobs.columns = ["Job Title", "Count"]

    fig = px.bar(
        jobs,
        x="Job Title",
        y="Count",
        title="Most Common Job Roles"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    Observation:
    • Certain job roles dominate hiring demand.
    • Market demand is concentrated around specific positions.
    """)

    st.success("""
    Business Insight:
    • Students can focus on high-demand roles.
    • Companies can understand market competition for talent.
    """)
with tabs[8]:

    st.subheader("⬇ Download Center")

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download Filtered Dataset",
        data=csv,
        file_name="internshala_jobs.csv",
        mime="text/csv"
    )

    st.success("Download the filtered dataset for further analysis.")
