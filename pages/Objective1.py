import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("cleaned_sleep_data_3.csv")
st.write("🧾 Columns in dataset:", df.columns.tolist())

df.rename(columns={
    'What is your gender?': 'Gender',
    'Your Age': 'Age',
    'What is your occupation?': 'Occupation',
    'How many hours of sleep do you get on average per night?': 'Sleep Hours',
    'How would you rate the comfort of your sleeping environment': 'Comfort',
}, inplace=True)



# --- PAGE TITLE ---
st.title("🎯 Objective 1: Understand the Sample Demographics and Baseline Behaviors")
st.markdown("""
This section focuses on understanding the **demographic characteristics** of respondents and their **typical sleep schedules**.
""")

# --- Visualization 1: Gender Distribution ---
st.subheader("1️⃣ Gender Distribution")
gender_counts = df['What is your Gender'].value_counts().reset_index()
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
