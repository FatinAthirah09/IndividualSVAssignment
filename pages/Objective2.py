import streamlit as st
import plotly.express as px
import pandas as pd
from app_helpers import load_data

# --- Load Data ---
df = load_data()

# --- Page Config ---
st.title("🔍 Objective 2: Identify the Prevalence and Correlates of Sleep Disruption")
st.markdown("""
This objective examines **how common sleep problems are** and how they relate to other factors like **gender** and **age group**.  
The visualizations below highlight the **frequency and relationships** of major sleep disruptions.
""")

st.divider()

# --- 📊 Summary Overview ---
st.subheader("📈 Summary Overview")

# --- Calculate Key Metrics ---
total_respondents = len(df)
sleep_diff_yes = df['Do you have difficulty falling asleep?'].str.lower().eq('yes').sum()
sleep_diff_rate = (sleep_diff_yes / total_respondents * 100).round(1)

concentration_issues = df['How often do you find it hard to concentrate due to lack of sleep?'].value_counts()
most_common_concentration = concentration_issues.idxmax()
main_reason_col = df['What are the main reasons you sleep late?'].dropna().astype(str)
top_reason = main_reason_col.str.split(';').explode().str.strip().value_counts().idxmax()

# --- Stylish Metric Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style="background-color:#F3E5F5;padding:20px;border-radius:15px;text-align:center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <h4 style="color:#6A1B9A;">💤 Sleep Difficulty Prevalence</h4>
            <h2 style="color:#4A148C;">{sleep_diff_rate}%</h2>
            <p style="color:#6A1B9A;">of respondents report difficulty falling asleep</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="background-color:#E0F7FA;padding:20px;border-radius:15px;text-align:center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <h4 style="color:#006064;">🧠 Common Concentration Issue</h4>
            <h3 style="color:#004D40;">{most_common_concentration}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style="background-color:#FFF8E1;padding:20px;border-radius:15px;text-align:center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <h4 style="color:#F57F17;">⏰ Top Reason for Sleeping Late</h4>
            <h3 style="color:#E65100;">{top_reason}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# --- Visualization 4: Difficulty Falling Asleep by Gender ---
with st.expander("💤 Difficulty Falling Asleep by Gender", expanded=True):
    sleep_difficulty_gender_counts = df.groupby(
        ['Do you have difficulty falling asleep?', 'What is your gender?']
    ).size().reset_index(name='Count')

    fig4 = px.bar(
        sleep_difficulty_gender_counts,
        x='Do you have difficulty falling asleep?',
        y='Count',
        color='What is your gender?',
        barmode='group',
        title='Difficulty Falling Asleep by Gender'
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --- Visualization 5: Concentration vs Falling Asleep Difficulty ---
with st.expander("🤔 Concentration Difficulty vs Falling Asleep", expanded=True):
    concentration_difficulty_counts = df.groupby(
        ['How often do you find it hard to concentrate due to lack of sleep?', 'Do you have difficulty falling asleep?']
    ).size().unstack(fill_value=0)

    fig5 = px.imshow(
        concentration_difficulty_counts,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='Purples',
        title='Relationship between Concentration Difficulty and Falling Asleep'
    )
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# --- Visualization 6: Reasons for Sleeping Late by Age Group ---
with st.expander("⏰ Main Reasons for Sleeping Late by Age Group", expanded=True):
    reasons_df = df['What are the main reasons you sleep late?'].astype(str).str.get_dummies(sep=';')
    age_reasons_df = pd.concat([df['Your Age'], reasons_df], axis=1)
    age_reasons_counts = age_reasons_df.groupby('Your Age').sum().reset_index()
    age_reasons_long = age_reasons_counts.melt(id_vars='Your Age', var_name='Reason', value_name='Count')

    fig6 = px.bar(
        age_reasons_long,
        x='Your Age',
        y='Count',
        color='Reason',
        title='Main Reasons for Sleeping Late by Age Group'
    )
    st.plotly_chart(fig6, use_container_width=True)
