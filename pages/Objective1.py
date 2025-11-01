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
    gender_occupation_counts = df.groupby(['What is your occupation?', 'What is your gender?']).size().reset_index(name='Count')
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
    gender_sleep_counts = df.groupby(['What is your gender?', 'How many hours of sleep do you get on average per night?']).size().reset_index(name='Count')
    fig3 = px.bar(gender_sleep_counts,
                  x='What is your gender?',
                  y='Count',
                  color='How many hours of sleep do you get on average per night?',
                  barmode='stack',
                  title='Distribution of Sleep Hours by Gender')
    st.plotly_chart(fig3, use_container_width=True)
