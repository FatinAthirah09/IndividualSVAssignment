import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# Load dataset function
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_sleep_data_3.csv")  # change to your dataset name
    return df

df = load_data()

# ------------------------------
# Page configuration
# ------------------------------
st.set_page_config(
    page_title="Sleep Study Dashboard",
    page_icon="😴",
    layout="wide",
)

# ------------------------------
# Header section
# ------------------------------
st.title("😴 Sleep Pattern and Behavior Analysis Dashboard")
st.markdown("""
Welcome to the **Sleep Study Dashboard**, a data-driven analysis designed to explore patterns, 
behaviors, and outcomes related to sleep among participants.

This dashboard is divided into **three main objectives**, each addressing a specific aspect of sleep health:
""")

# ------------------------------
# Overview of objectives
# ------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.info("""
    ### 🎯 Objective 1  
    **Understand the Sample Demographics and Baseline Behaviors**  
    - Explore participants’ age, gender, and sleep duration.  
    - Understand basic lifestyle and sleeping trends.
    """)

with col2:
    st.info("""
    ### 🔍 Objective 2  
    **Identify the Prevalence and Correlates of Sleep Disruption**  
    - Examine common sleep problems.  
    - Analyze how disruptions relate to demographics.
    """)

with col3:
    st.info("""
    ### 📉 Objective 3  
    **Analyze Sleep Duration, Discomfort, and Negative Outcomes**  
    - Study how sleep duration and comfort influence side effects.  
    - Reveal relationships with concentration and well-being.
    """)

st.divider()

# ------------------------------
# Dataset Overview Section
# ------------------------------
st.header("📊 Dataset Overview")

with st.expander("Click to view dataset preview and summary", expanded=False):
    st.write("Here’s a glimpse of the dataset used for analysis:")
    st.dataframe(df)

    st.markdown("### 🧾 Columns in the Dataset")
    st.write(list(df.columns))

    st.markdown("### 📈 Dataset Statistics")
    st.write(df.describe())

st.divider()

# ------------------------------
# Visualization Summary (Optional teaser)
# ------------------------------
st.header("🌐 Overall Snapshot: Sleep Hours Distribution")
st.markdown("An overview of how many hours participants sleep on average each night.")

fig = px.histogram(df,
                   x='How many hours of sleep do you get on average per night?',
                   color='What is your gender?',
                   barmode='group',
                   title='Sleep Duration by Gender')
fig.update_layout(xaxis_title="Average Hours of Sleep", yaxis_title="Count")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ------------------------------
# Credits / Footer
# ------------------------------
st.markdown("""
---
👩‍💻 **Developed by:** [FATIN NUR ATHIRAH BT ABDUL AZIM]  
📚 **Course:** Data Visualization Assignment  
🏫 **Institution:** [Universiti Malaysia Kelantan]  
🗓️ **Year:** 2025  

> *This Streamlit dashboard was created as part of an academic project to analyze sleep behavior and its effects on wellbeing.*
""")
