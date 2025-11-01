import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- CONFIGURATION (First st command) ---
st.set_page_config(layout="wide", page_title="Sleep Survey Data Analysis")
st.header("Scientific Visualization", divider="gray")
st.title("🎓 Sleep Survey and Performance Analysis")
st.markdown("---")

import plotly.express as px
import pandas as pd # Import pandas if not already imported

# --- Assumes the following lines from your original code are executed ---
# age_counts = df['Your Age'].value_counts()

# 1. Convert the age_counts Series into a DataFrame suitable for plotly.express
# The index (ages) becomes a column, and the values (counts) become another.
age_df = age_counts.reset_index()
age_df.columns = ['Age', 'Count']

# 2. Create the Plotly pie chart figure
fig = px.pie(
    age_df,
    values='Count',          # The column to use for slice sizes
    names='Age',             # The column to use for slice labels
    title='Distribution of Respondent Age',
    hole=0.3,                # Optional: Make it a donut chart
    # Optional: Customize the percentage format on the slices
    custom_data=['Count']
)

# Optional: Improve text formatting (shows percentage and count on hover)
fig.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))


