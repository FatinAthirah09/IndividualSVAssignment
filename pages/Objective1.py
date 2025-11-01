import streamlit as st
import plotly.express as px
import pandas as pd
from app_helpers import load_data

# --- Load Data ---
df = load_data()

st.title("🎯 Objective 1: Understand the Sample Demographics and Baseline Behaviors")
st.markdown("""
This section focuses on understanding the demographic characteristics of respondents and their typical sleep schedules.
""")

# Clean column names (in case there are spaces)
df.columns = df.columns.str.strip()

# ------------------------------------------------------------
# 1️⃣ Gender Distribution
# ------------------------------------------------------------
st.subheader("1️⃣ Gender Distribution of Respondents")

gender_counts = df['What is your gender?'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']

fig1 = px.pie(gender_counts,
              values='Count',
              names='Gender',
              title='Distribution of Respondent Gender',
              hole=0.3)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------
# 2️⃣ Age Distribution
# ------------------------------------------------------------
st.subheader("2️⃣ Age Distribution of Respondents")

age_counts = df['Your Age'].value_counts().reset_index()
age_counts.columns = ['Age', 'Count']

fig2 = px.bar(age_counts,
              x='Age',
              y='Count',
              color='Age',
              title='Distribution of Respondent Age')
fig2.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------
# 3️⃣ Typical Sleep Schedule
# ------------------------------------------------------------
st.subheader("3️⃣ Typical Sleep Schedule on Working Days vs Weekends")

sleep_times = df[['What time do you usually go to bed?', 'What time do you usually wake up on working days?',
                  'What time do you usually go to bed on weekends?', 'What time do you usually wake up on weekends?']]

# For better visualization, we can show average or just count frequency
bed_counts = df['What time do you usually go to bed?'].value_counts().reset_index()
bed_counts.columns = ['Bed Time', 'Count']

fig3 = px.bar(bed_counts,
              x='Bed Time',
              y='Count',
              title='Most Common Bed Times on Working Days')
fig3.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("📊 These visualizations provide a clear overview of the respondents’ demographics and general sleep routines.")
