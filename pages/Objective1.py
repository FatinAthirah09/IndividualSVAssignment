import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("cleaned_sleep_data_3.csv")

# --- PAGE TITLE ---
st.title("🎯 Objective 1: Understand the Sample Demographics and Baseline Behaviors")
st.markdown("""
This section focuses on understanding the **demographic characteristics** of respondents and their **typical sleep schedules**.
""")

# --- Visualization 1: Gender Distribution ---
st.subheader("1️⃣ Gender Distribution")
gender_counts = df['Gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']
fig1 = px.pie(gender_counts, names='Gender', values='Count', title='Gender Distribution')
st.plotly_chart(fig1, use_container_width=True)

# --- Visualization 2: Age Group Distribution ---
st.subheader("2️⃣ Age Group Distribution")
fig2 = px.histogram(df, x='Your Age', title='Age Group Distribution', color='Your Age')
st.plotly_chart(fig2, use_container_width=True)

# --- Visualization 3: Typical Bedtime ---
st.subheader("3️⃣ Typical Bedtime by Age Group")
if 'What time do you usually go to bed?' in df.columns:
    fig3 = px.box(df, x='Your Age', y='What time do you usually go to bed?',
                  title='Bedtime Patterns by Age Group',
                  color='Your Age')
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("⚠️ Column 'What time do you usually go to bed?' not found in dataset.")
