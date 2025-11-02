import streamlit as st
import plotly.express as px
import pandas as pd
from app_helpers import load_data

# --- Load Data ---
df = load_data()

# --- Page Config ---
st.title("🔍 Objective 2: Identify the Prevalence and Correlates of Sleep Disruption")
st.markdown("""
This objective investigates **how common sleep problems are** and explores their relationship with other factors like **age group** and **gender**.  
By identifying these patterns, we can understand which groups experience more disruption and what behaviors contribute to it.
""")

st.divider()

# --- Summary Box ---
total_respondents = len(df)

# ✅ Improved detection for "yes" answers (handles case, spacing, variations)
sleep_diff_yes = df['Do you have difficulty falling asleep?'] \
    .astype(str).str.lower().str.contains('yes').sum()

sleep_diff_rate = (sleep_diff_yes / total_respondents * 100).round(1)

st.markdown("""
### 🧾 Summary of Findings
""")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Respondents", value=f"{total_respondents}")
with col2:
    st.metric(label="Sleep Difficulty Prevalence", value=f"{sleep_diff_rate} %")

st.info(f"💡 About {sleep_diff_rate}% of respondents report having **difficulty falling asleep**.")

st.divider()

# --- Visualization 4: Difficulty Falling Asleep by Gender ---
with st.expander("💤 Difficulty Falling Asleep by Gender", expanded=True):
    sleep_difficulty_gender_counts = df.groupby(
        ['Do you have difficulty falling asleep?', 'What is your gender?']
    ).size().reset_index(name='Count')
    fig4 = px.bar(sleep_difficulty_gender_counts,
                  x='Do you have difficulty falling asleep?',
                  y='Count',
                  color='What is your gender?',
                  barmode='group',
                  title='Difficulty Falling Asleep by Gender',
                  labels={
                      'Do you have difficulty falling asleep?': 'Difficulty Falling Asleep',
                      'Count': 'Number of Respondents'
                  })
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --- Visualization 5: Concentration vs Falling Asleep Difficulty ---
with st.expander("🤔 Concentration Difficulty vs Falling Asleep", expanded=True):
    concentration_difficulty_counts = df.groupby(
        ['How often do you find it hard to concentrate due to lack of sleep?',
         'Do you have difficulty falling asleep?']
    ).size().unstack(fill_value=0)
    fig5 = px.imshow(concentration_difficulty_counts,
                     text_auto=True,
                     aspect="auto",
                     color_continuous_scale='Blues',
                     title='Relationship Between Concentration Difficulty and Falling Asleep')
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# --- Visualization 6: Reasons for Sleeping Late by Age Group ---
with st.expander("⏰ Main Reasons for Sleeping Late by Age Group", expanded=True):
    reasons_df = df['What are the main reasons you sleep late?'].astype(str).str.get_dummies(sep=';')
    age_reasons_df = pd.concat([df['Your Age'], reasons_df], axis=1)
    age_reasons_counts = age_reasons_df.groupby('Your Age').sum().reset_index()
    age_reasons_long = age_reasons_counts.melt(id_vars='Your Age', var_name='Reason', value_name='Count')
    fig6 = px.bar(age_reasons_long,
                  x='Your Age',
                  y='Count',
                  color='Reason',
                  title='Main Reasons for Sleeping Late by Age Group')
    st.plotly_chart(fig6, use_container_width=True)
