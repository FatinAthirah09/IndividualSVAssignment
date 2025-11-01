import streamlit as st
from app_helpers import load_data
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Sleep Data Exploration")

# --- Load data ---
df = load_data()

st.write("### Preview of Data")
st.dataframe(df.head())

st.markdown("---")

st.header("🎂 Age Distribution of Respondents")
age_counts = df['Your Age'].value_counts().reset_index()
age_counts.columns = ['Age', 'Count']
fig = px.pie(age_counts, values='Count', names='Age', hole=.3)
st.plotly_chart(fig, use_container_width=True)
