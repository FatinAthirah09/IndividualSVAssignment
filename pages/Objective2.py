import streamlit as st
import plotly.express as px
import pandas as pd
from app_helpers import load_data

# --- Load Data ---
df = load_data()
df.columns = df.columns.str.strip()  # clean spaces

# --- Streamlit Page Setup ---
st.title("🧠 Objective 2: Identify the Prevalence and Correlates of Sleep Disruption")
st.markdown("""
This objective aims to measure how common specific sleep problems are and to see if they are linked to other major factors like demographics.
""")

# ------------------------------------------------------------
# 4️⃣ Difficulty Falling Asleep by Gender (Grouped Bar Chart)
# ------------------------------------------------------------
st.header("4️⃣ 💤 Difficulty Falling Asleep by Gender")
sleep_difficulty_gender_counts = df.groupby(['Do you have difficulty falling asleep?', 'What is your gender?']).size().reset_index(name='Count')
sleep_difficulty_gender_counts.columns = ['Sleep Difficulty', 'Gender', 'Count']
fig4 = px.bar(sleep_difficulty_gender_counts,
              x='Sleep Difficulty',
              y='Count',
              color='Gender',
              barmode='group',
              title='Difficulty Falling Asleep by Gender',
              labels={'Sleep Difficulty': 'Difficulty Falling Asleep'})
fig4.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------
# 5️⃣ Concentration Difficulty vs Falling Asleep (Heatmap)
# ------------------------------------------------------------
st.header("5️⃣ 🤔 Concentration vs. Falling Asleep Difficulty")
concentration_difficulty_counts = df.groupby(
    ['How often do you find it hard to concentrate due to lack of sleep?',
     'Do you have difficulty falling asleep?']
).size().unstack(fill_value=0)

fig5 = px.imshow(concentration_difficulty_counts,
                 text_auto=True,
                 aspect="auto",
                 color_continuous_scale='Blues',
                 title='Relationship between Difficulty Concentrating and Difficulty Falling Asleep')
fig5.update_layout(
    xaxis_title='Difficulty Falling Asleep',
    yaxis_title='Difficulty Concentrating due to Lack of Sleep'
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------
# 6️⃣ Main Reasons for Sleeping Late by Age Group (Stacked Bar)
# ------------------------------------------------------------
st.header("6️⃣ ⏰ Main Reasons for Sleeping Late by Age Group")

if 'What are the main reasons you sleep late?' in df.columns and 'Your Age' in df.columns:
    reasons_df = df['What are the main reasons you sleep late?'].astype(str).str.get_dummies(sep=';')
    age_reasons_df = pd.concat([df['Your Age'], reasons_df], axis=1)
    age_reasons_counts = age_reasons_df.groupby('Your Age').sum().reset_index()
    age_reasons_long = age_reasons_counts.melt(id_vars='Your Age', var_name='Reason', value_name='Count')

    fig6 = px.bar(age_reasons_long,
                  x='Your Age',
                  y='Count',
                  color='Reason',
                  title='Main Reasons for Sleeping Late by Age Group',
                  labels={'Your Age': 'Age Group', 'Count': 'Count of Reasons'})
    fig6.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.warning("⚠️ Column 'What are the main reasons you sleep late?' not found in dataset.")

st.markdown("---")

st.success("✅ Objective 2 visualizations loaded successfully!")
