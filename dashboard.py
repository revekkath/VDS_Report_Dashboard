# dashboard.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Load CSV ----
df = pd.read_csv("deaths_clean.csv")

# ---- Streamlit page config ----
st.set_page_config(
    page_title="Mortality Dashboard Cyprus",
    layout="wide"
)

st.title("Mortality Patterns in Cyprus")
st.markdown("""
Interactive dashboard showing mortality trends by cause of death and sex in Cyprus.
Data source: CYSTAT
""")

# ---- Sidebar filters ----
st.sidebar.header("Filters")
cause_options = df['cause'].unique()
selected_cause = st.sidebar.selectbox("Select cause of death:", cause_options)

sex_options = df['sex'].unique()
selected_sex = st.sidebar.selectbox("Select sex:", sex_options)

# Filter data
filtered_df = df[(df['cause'] == selected_cause) & (df['sex'] == selected_sex)]

# ---- Plot 1: Deaths over time ----
st.subheader(f"Deaths over time ({selected_cause}, {selected_sex})")
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=filtered_df, x='year', y='deaths', marker='o', ax=ax)
ax.set_ylabel("Deaths")
ax.set_xlabel("Year")
ax.set_title(f"{selected_cause} deaths ({selected_sex}) over time")
st.pyplot(fig)

# ---- Plot 2: Deaths per 100k population ----
st.subheader(f"Deaths per 100,000 population ({selected_cause}, {selected_sex})")
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.lineplot(data=filtered_df, x='year', y='Deaths_per_100k', marker='o', color='red', ax=ax2)
ax2.set_ylabel("Deaths per 100k")
ax2.set_xlabel("Year")
ax2.set_title(f"{selected_cause} deaths per 100k population ({selected_sex})")
st.pyplot(fig2)

# ---- Plot 3: Total deaths by sex for a selected cause ----
st.subheader(f"Deaths by sex for {selected_cause}")
sex_df = df[df['cause'] == selected_cause].groupby('sex')['deaths'].sum().reset_index()
fig3, ax3 = plt.subplots(figsize=(8,5))
sns.barplot(data=sex_df, x='sex', y='deaths', palette="pastel", ax=ax3)
ax3.set_ylabel("Total deaths")
ax3.set_xlabel("Sex")
ax3.set_title(f"Total deaths by sex ({selected_cause})")
st.pyplot(fig3)

# ---- Plot 4: Comparison of causes for selected year and sex ----
st.subheader(f"Deaths by cause in selected year ({selected_sex})")
year_options = df['year'].unique()
selected_year = st.sidebar.slider("Select year:", int(year_options.min()), int(year_options.max()), int(year_options.max()))

year_df = df[(df['year'] == selected_year) & (df['sex'] == selected_sex)]
fig4, ax4 = plt.subplots(figsize=(10,5))
sns.barplot(data=year_df, x='cause', y='deaths', palette="viridis", ax=ax4)
ax4.set_ylabel("Deaths")
ax4.set_xlabel("Cause of death")
ax4.set_title(f"Deaths by cause ({selected_sex}, {selected_year})")
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig4)

# ---- Optional: Show filtered data ----
if st.checkbox("Show filtered data"):
    st.dataframe(filtered_df)
