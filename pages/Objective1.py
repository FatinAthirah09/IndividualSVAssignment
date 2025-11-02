import streamlit as st
import plotly.express as px
import pandas as pd
from app_helpers import load_data

# --- Load Data ---
df = load_data()

# --- Page Config ---
st.title("🎯 Objective 1: Understand the Sample Demographics and Baseline Behaviors")
st.markdown("""
This objective focuses on identifying **demographic characteristics** and **baseline sleep patterns** among respondents.  
The visualizations below explore participants’ **age, gender, and sleep duration** patterns.
""")

st.divider()

# --- 📊 Summary Metrics Section ---
st.subheader("📈 Summary Overview")

# Basic calculations
total_respondents = len(df)
age_groups = df['Your Age'].nunique()
avg_sleep = df['How many hours of sleep do you get on average per night?'].mode()[0]
gender_counts = df['What is your gender?'].value_counts()

# --- Stylish Metric Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style="background-color:#E8F5E9;padding:20px;border-radius:15px;text-align:center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <h4 style="color:#2E7D32;">👥 Total Respondents</h4>
            <h2 style="color:#1B5E20;">{total_respondents}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="background-color:#FFF3E0;padding:20px;border-radius:15px;text-align:center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <h4 style="color:#E65100;">🎂 Age Groups</h4>
            <h2 style="color:#BF360C;">{age_groups}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style="background-color:#E3F2FD;padding:20px;border-radius:15px;text-align:center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <h4 style="color:#1565C0;">😴 Most Common Sleep Duration</h4>
            <h2 style="color:#0D47A1;">{avg_sleep} hours</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("### 👩‍🦰 Gender Breakdown")
gender_breakdown = pd.DataFrame({
    'Gender': gender_counts.index,
    'Count': gender_counts.values
})
st.dataframe(gender_breakdown, use_container_width=True, hide_index=True)

st.divider()

# --- Visualization 1: Age Distribution ---
with st.expander("🎂 Age Distribution of Respondents", expanded=True):
    age_counts = df['Your Age'].value_counts().reset_index()
    age_counts.columns = ['Age', 'Count']
    fig1 = px.pie(age_counts, values='Count', names='Age',
                  title='Distribution of Respondent Age', hole=.3)
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

st.divider()

# --- Visualization 2: Gender Distribution by Occupation ---
with st.expander("🧑‍💼 Gender Distribution by Occupation", expanded=True):
    gender_occupation_counts = df.groupby(
        ['What is your occupation?', 'What is your gender?']
    ).size().reset_index(name='Count')
    
    fig2 = px.bar(gender_occupation_counts,
                  x='What is your occupation?',
                  y='Count',
                  color='What is your gender?',
                  barmode='group',
                  title='Gender Distribution by Occupation',
                  labels={'What is your occupation?': 'Occupation', 'Count': 'Count'})
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- Visualization 3: Sleep Hours by Gender ---
with st.expander("🌙 Average Sleep Hours by Gender", expanded=True):
    gender_sleep_counts = df.groupby(
        ['What is your gender?', 'How many hours of sleep do you get on average per night?']
    ).size().reset_index(name='Count')
    
    fig3 = px.bar(gender_sleep_counts,
                  x='What is your gender?',
                  y='Count',
                  color='How many hours of sleep do you get on average per night?',
                  barmode='stack',
                  title='Distribution of Sleep Hours by Gender')
    st.plotly_chart(fig3, use_container_width=True)
