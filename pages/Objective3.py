import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app_helpers import load_data

# --- Load Data ---
df = load_data()

# --- Page Config ---
st.title("📉 Objective 3: Analyze the Relationship Between Sleep Duration, Discomfort, and Negative Outcomes")
st.markdown("""
This objective explores **how sleep duration and sleep environment comfort** impact concentration, side effects, and overall well-being.  
The visualizations provide insights into patterns of **discomfort and negative outcomes** across different sleep groups.
""")

st.divider()

# --- Summary Box ---
total_respondents = len(df)

# Compute average sleep hours
avg_sleep_hours = df['How many hours of sleep do you get on average per night?'].astype(float).mean().round(1)

# Count how many report side effects
side_effect_cols = df['Do you experience any of the following side effects from late sleeping?'].astype(str).str.get_dummies(sep=';')
total_side_effects_reported = (side_effect_cols.sum().sum())

st.markdown("### 🧾 Summary of Findings")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Respondents", value=f"{total_respondents}")
with col2:
    st.metric(label="Average Sleep Hours", value=f"{avg_sleep_hours} hours")
with col3:
    st.metric(label="Total Side Effects Reported", value=f"{total_side_effects_reported}")

st.info("💡 This objective highlights **how sleep quality, comfort, and duration are linked to negative outcomes**, helping identify areas for improvement in sleep habits.")

st.divider()

# --- Visualization 7: Comfort Ratings vs Average Sleep Hours ---
with st.expander("🛌 Comfort Ratings vs Average Sleep Hours", expanded=True):
    grouped_comfort = df.groupby(
        ['How many hours of sleep do you get on average per night?',
         'How would you rate the comfort of your sleeping environment']
    ).size().reset_index(name='Count')

    fig7 = go.Figure()
    for sleep_group in sorted(grouped_comfort['How many hours of sleep do you get on average per night?'].unique()):
        data = grouped_comfort[grouped_comfort['How many hours of sleep do you get on average per night?'] == sleep_group]
        fig7.add_trace(go.Scatter(
            x=data['How would you rate the comfort of your sleeping environment'],
            y=data['Count'],
            mode='lines+markers',
            name=f'{sleep_group} hours'
        ))
    fig7.update_layout(
        title='Comfort of Sleeping Environment vs Average Hours of Sleep',
        xaxis_title='Comfort Rating',
        yaxis_title='Number of Respondents',
        legend_title='Sleep Hours'
    )
    st.plotly_chart(fig7, use_container_width=True)

st.divider()

# --- Visualization 8: Average Sleep Hours vs Side Effects ---
with st.expander("🤕 Average Sleep Hours vs Side Effects from Late Sleeping", expanded=True):
    side_effects_df = df['Do you experience any of the following side effects from late sleeping?'].astype(str).str.get_dummies(sep=';')
    sleep_side_effects_df = pd.concat([df['How many hours of sleep do you get on average per night?'], side_effects_df], axis=1)
    sleep_side_effects_counts = sleep_side_effects_df.groupby('How many hours of sleep do you get on average per night?').sum()

    fig8 = px.imshow(
        sleep_side_effects_counts,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='Blues',
        title='Average Sleep Hours vs Side Effects'
    )
    st.plotly_chart(fig8, use_container_width=True)

st.divider()

# --- Visualization 9: Concentration vs Comfort ---
with st.expander("🤯 Difficulty Concentrating by Sleep Environment Comfort", expanded=True):
    fig9 = px.bar(
        df,
        x='How often do you find it hard to concentrate due to lack of sleep?',
        facet_col='How would you rate the comfort of your sleeping environment',
        facet_col_wrap=3,
        color='How often do you find it hard to concentrate due to lack of sleep?',
        title='Difficulty Concentrating by Sleep Environment Comfort'
    )
    fig9.update_xaxes(title_text="Difficulty Concentrating", tickangle=-45)
    fig9.update_yaxes(title_text="Count")
    fig9.update_layout(showlegend=False)
    st.plotly_chart(fig9, use_container_width=True)
