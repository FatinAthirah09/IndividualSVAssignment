import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app_helpers import load_data

# --- Load Data ---
df = load_data()

# --- Convert sleep hours to numeric and drop invalid rows ---
df['Sleep Hours Numeric'] = pd.to_numeric(
    df['How many hours of sleep do you get on average per night?'], errors='coerce'
)
df_sleep_clean = df.dropna(subset=['Sleep Hours Numeric'])

# --- Page Config ---
st.title("📉 Objective 3: Analyze the Relationship Between Sleep Duration, Discomfort, and Negative Outcomes")
st.markdown("""
This objective investigates **how sleep duration** and **sleep environment comfort** affect concentration, side effects, and overall well-being.  
The visualizations focus on **patterns of discomfort and negative outcomes** among different sleep groups.
""")

st.divider()

# --- Summary Box ---
if not df_sleep_clean.empty:
    avg_sleep_hours = df_sleep_clean['Sleep Hours Numeric'].mean().round(1)
else:
    avg_sleep_hours = "Data not available"

st.markdown(f"""
<div style="border: 2px solid #1f77b4; padding: 15px; border-radius: 10px; background-color:#f0f8ff">
<h4>📌 Summary:</h4>
<ul>
<li>The average sleep duration among respondents is <b>{avg_sleep_hours}</b> hours per night.</li>
<li>Sleep environment comfort and sleep duration are linked to concentration and reported side effects.</li>
<li>Visualizations below explore these relationships in detail.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- Visualization 7: Comfort Ratings vs Average Sleep Hours ---
with st.expander("🛌 Comfort Ratings vs Average Sleep Hours", expanded=True):
    grouped_comfort = df_sleep_clean.groupby(
        ['Sleep Hours Numeric', 'How would you rate the comfort of your sleeping environment']
    ).size().reset_index(name='Count')

    fig7 = go.Figure()
    for sleep_group in sorted(grouped_comfort['Sleep Hours Numeric'].unique()):
        data = grouped_comfort[grouped_comfort['Sleep Hours Numeric'] == sleep_group]
        fig7.add_trace(go.Scatter(
            x=data['How would you rate the comfort of your sleeping environment'],
            y=data['Count'],
            mode='lines+markers',
            name=f'{sleep_group} hours'
        ))
    fig7.update_layout(
        title='Comfort of Sleeping Environment vs Average Hours of Sleep',
        xaxis_title='Comfort Rating',
        yaxis_title='Count',
        legend_title='Sleep Hours'
    )
    st.plotly_chart(fig7, use_container_width=True)

st.divider()

# --- Visualization 8: Average Sleep Hours vs Side Effects ---
with st.expander("🤕 Average Sleep Hours vs Side Effects from Late Sleeping", expanded=True):
    side_effects_df = df_sleep_clean['Do you experience any of the following side effects from late sleeping?'].astype(str).str.get_dummies(sep=';')
    sleep_side_effects_df = pd.concat(
        [df_sleep_clean['Sleep Hours Numeric'], side_effects_df], axis=1
    )
    sleep_side_effects_counts = sleep_side_effects_df.groupby('Sleep Hours Numeric').sum()
    fig8 = px.imshow(
        sleep_side_effects_counts,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='Blues',
        title='Average Sleep Hours vs Side Effects'
    )
    st.plotly_chart(fig8, use_container_width=True)

st.divider()

# --- Visualization 9: Difficulty Concentrating by Sleep Environment Comfort ---
with st.expander("🤯 Difficulty Concentrating by Sleep Environment Comfort", expanded=True):
    fig9 = px.bar(
        df_sleep_clean,
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
