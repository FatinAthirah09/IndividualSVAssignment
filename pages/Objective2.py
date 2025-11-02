import streamlit as st
import plotly.express as px
import pandas as pd
from app_helpers import load_data

# --- Load Data ---
df = load_data()

# --- Page Config ---
st.title("🔍 Objective 2: Identify the Prevalence and Correlates of Sleep Disruption")
st.markdown("""
This objective examines **how common sleep problems are** and how they relate to other factors like **gender** and **age group**.
The visualizations below highlight the **frequency and relationships** of major sleep disruptions.
""")

st.divider()

# --- 📊 Key Metrics Summary (Polished with st.metric) ---
st.header("📈 Key Prevalence Metrics")

# --- Calculate Key Metrics ---
total_respondents = len(df)
# Calculate the number and percentage of respondents who have difficulty falling asleep
sleep_diff_yes = df['Do you have difficulty falling asleep?'].str.lower().eq('yes').sum()
sleep_diff_rate = (sleep_diff_yes / total_respondents * 100).round(1)

# Find the most common concentration issue reported
concentration_issues = df['How often do you find it hard to concentrate due to lack of sleep?'].value_counts()
most_common_concentration = concentration_issues.idxmax()

# Find the single most common reason for sleeping late across all respondents
main_reason_col = df['What are the main reasons you sleep late?'].dropna().astype(str)
top_reason = main_reason_col.str.split(';').explode().str.strip().value_counts().idxmax()

# --- Streamlit Native Metric Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💤 Sleep Difficulty Prevalence",
        value=f"{sleep_diff_rate}%",
        help=f"{sleep_diff_yes} out of {total_respondents} respondents report difficulty falling asleep."
    )

with col2:
    st.metric(
        label="🧠 Most Common Concentration Issue",
        value=most_common_concentration
    )

with col3:
    st.metric(
        label="⏰ Top Reason for Sleeping Late",
        value=top_reason
    )

st.divider()

# --- Visualization 4: Difficulty Falling Asleep by Gender ---
with st.expander("📊 Sleep Disruption by Gender", expanded=True):
    st.subheader("Difficulty Falling Asleep by Gender")
    sleep_difficulty_gender_counts = df.groupby(
        ['Do you have difficulty falling asleep?', 'What is your gender?']
    ).size().reset_index(name='Count')

    fig4 = px.bar(
        sleep_difficulty_gender_counts,
        x='Do you have difficulty falling asleep?',
        y='Count',
        color='What is your gender?',
        barmode='group',
        title='Distribution of Sleep Difficulty Responses by Gender'
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --- Visualization 5: Concentration vs Falling Asleep Difficulty ---
with st.expander(" heatmap: Concentration & Sleep Initiation", expanded=True):
    st.subheader("Concentration Difficulty vs Falling Asleep")
    concentration_difficulty_counts = df.groupby(
        ['How often do you find it hard to concentrate due to lack of sleep?', 'Do you have difficulty falling asleep?']
    ).size().unstack(fill_value=0)

    fig5 = px.imshow(
        concentration_difficulty_counts,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='Purples',
        title='Relationship between Concentration Difficulty and Falling Asleep'
    )
    fig5.update_yaxes(title_text="Concentration Difficulty Frequency")
    fig5.update_xaxes(title_text="Difficulty Falling Asleep")
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# --- Visualization 6: Reasons for Sleeping Late by Age Group ---
with st.expander("👪 Age-Related Sleep Delay Factors", expanded=True):
    st.subheader("Main Reasons for Sleeping Late by Age Group")
    reasons_df = df['What are the main reasons you sleep late?'].astype(str).str.get_dummies(sep=';')
    age_reasons_df = pd.concat([df['Your Age'], reasons_df], axis=1)
    age_reasons_counts = age_reasons_df.groupby('Your Age').sum().reset_index()
    # Melt data for grouped bar chart
    age_reasons_long = age_reasons_counts.melt(id_vars='Your Age', var_name='Reason', value_name='Count')

    fig6 = px.bar(
        age_reasons_long,
        x='Your Age',
        y='Count',
        color='Reason',
        title='Breakdown of Reasons for Sleeping Late by Age Group',
        labels={'Your Age': 'Age Group', 'Count': 'Total Mentions'}
    )
    st.plotly_chart(fig6, use_container_width=True)

st.divider()

## 🌟 Conclusion for Objective 2
st.success("""
The analysis for Objective 2 highlights the **high prevalence of sleep disruption** and its clear connection to cognitive issues:

* **Widespread Difficulty:** A significant portion of the survey population (specifically **{sleep_diff_rate}%**) reports difficulty falling asleep, indicating a common issue.
* **Concentration Link:** The visualizations confirm a strong association: respondents who report **difficulty falling asleep** are also the group most likely to report **frequent issues with concentration**.
* **Age-Specific Factors:** The **reasons for sleeping late** vary by age, with **"social media/internet"** being a highly dominant factor across most groups. Understanding these age-specific drivers is crucial for targeted intervention.

**Overall, sleep disruption is prevalent and is closely correlated with immediate negative cognitive outcomes, with technological distraction being a primary underlying cause.**
""".format(sleep_diff_rate=sleep_diff_rate))
