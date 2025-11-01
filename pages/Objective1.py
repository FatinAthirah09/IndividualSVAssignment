import streamlit as st
import plotly.express as px
from app_helpers import load_data

# --- Load Data ---
df = load_data()
df.columns = df.columns.str.strip()  # clean spaces just in case

# --- Streamlit Page Setup ---
st.title("🎯 Objective 1: Understand the Sample Demographics and Baseline Behaviors")
st.markdown("""
This section focuses on understanding the demographic characteristics of respondents and their typical sleep schedules.
""")

# ------------------------------------------------------------
# 1️⃣ Age Distribution of Respondents (Pie Chart)
# ------------------------------------------------------------
st.header("1️⃣ 🎂 Age Distribution of Respondents")
age_counts = df['Your Age'].value_counts().reset_index()
age_counts.columns = ['Age', 'Count']
fig1 = px.pie(age_counts,
              values='Count',
              names='Age',
              title='Distribution of Respondent Age',
              hole=.3)
fig1.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------
# 2️⃣ Gender Distribution by Occupation (Grouped Bar Chart)
# ------------------------------------------------------------
st.header("2️⃣ 🧑‍💼 Gender Distribution by Occupation")
gender_occupation_counts = df.groupby(['What is your occupation?', 'What is your gender?']).size().reset_index(name='Count')
gender_occupation_counts.columns = ['Occupation', 'Gender', 'Count']
fig2 = px.bar(gender_occupation_counts,
              x='Occupation',
              y='Count',
              color='Gender',
              barmode='group',
              title='Gender Distribution by Occupation',
              labels={'Occupation': 'Occupation', 'Count': 'Count'},
              color_discrete_map={'Male': 'blue', 'Female': 'red', 'Other': 'green'})
fig2.update_layout(xaxis={'categoryorder': 'total descending'}, xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------
# 3️⃣ Distribution of Sleep Hours by Gender (Stacked Bar Chart)
# ------------------------------------------------------------
st.header("3️⃣ 🌙 Distribution of Average Sleep Hours by Gender")
gender_sleep_counts = df.groupby(['What is your gender?', 'How many hours of sleep do you get on average per night?']).size().reset_index(name='Count')
gender_sleep_counts.columns = ['Gender', 'Sleep Hours', 'Count']
fig3 = px.bar(gender_sleep_counts,
              x='Gender',
              y='Count',
              color='Sleep Hours',
              barmode='stack',
              title='Distribution of Sleep Hours by Gender',
              labels={'Sleep Hours': 'Average Sleep Hours'})
fig3.update_layout(xaxis_tickangle=0)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

st.success("✅ Objective 1 visualizations loaded successfully!")
