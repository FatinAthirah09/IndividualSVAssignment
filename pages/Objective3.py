import streamlit as st
import plotly.express as px
import pandas as pd
from app_helpers import load_data

# --- Load data ---
df = load_data()
df.columns = df.columns.str.strip()  # Clean up any spaces

# --- Page setup ---
st.title("😴 Objective 3: Analyze the Relationship Between Sleep Duration, Discomfort, and Negative Outcomes")
st.markdown("""
This objective explores how sleep duration and comfort affect concentration and negative outcomes such as side effects from poor sleep.
""")

# ------------------------------------------------------------
# 7️⃣ Sleep Duration vs. Side Effects
# ------------------------------------------------------------
st.header("7️⃣ 🌙 Sleep Duration vs. Side Effects")

if 'How many hours of sleep do you get on average per night?' in df.columns and 'Do you experience any of the following side effects from late sleeping?' in df.columns:
    fig7 = px.box(df,
                  x='Do you experience any of the following side effects from late sleeping?',
                  y='How many hours of sleep do you get on average per night?',
                  color='Do you experience any of the following side effects from late sleeping?',
                  title='Sleep Duration vs. Reported Side Effects',
                  labels={
                      'Do you experience any of the following side effects from late sleeping?': 'Side Effects',
                      'How many hours of sleep do you get on average per night?': 'Hours of Sleep'
                  })
    fig7.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig7, use_container_width=True)
else:
    st.warning("⚠️ Required columns for this visualization are missing.")

st.markdown("---")

# ------------------------------------------------------------
# 8️⃣ Sleep Environment Comfort vs. Side Effects
# ------------------------------------------------------------
st.header("8️⃣ 🛏️ Sleep Environment Comfort vs. Side Effects")

if 'How would you rate the comfort of your sleeping environment' in df.columns and 'Do you experience any of the following side effects from late sleeping?' in df.columns:
    comfort_side_effects = df.groupby(
        ['How would you rate the comfort of your sleeping environment',
         'Do you experience any of the following side effects from late sleeping?']
    ).size().reset_index(name='Count')

    fig8 = px.bar(comfort_side_effects,
                  x='How would you rate the comfort of your sleeping environment',
                  y='Count',
                  color='Do you experience any of the following side effects from late sleeping?',
                  barmode='group',
                  title='Comfort of Sleep Environment vs. Side Effects',
                  labels={'How would you rate the comfort of your sleeping environment': 'Comfort Level'})
    fig8.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig8, use_container_width=True)
else:
    st.warning("⚠️ Required columns for this visualization are missing.")

st.markdown("---")

# ------------------------------------------------------------
# 9️⃣ Sleep Duration vs. Difficulty Concentrating (Heatmap)
# ------------------------------------------------------------
st.header("9️⃣ 🧠 Sleep Duration vs. Difficulty Concentrating")

if 'How many hours of sleep do you get on average per night?' in df.columns and 'How often do you find it hard to concentrate due to lack of sleep?' in df.columns:
    cross_tab = pd.crosstab(
        df['How many hours of sleep do you get on average per night?'],
        df['How often do you find it hard to concentrate due to lack of sleep?']
    )

    fig9 = px.imshow(cross_tab,
                     text_auto=True,
                     aspect='auto',
                     color_continuous_scale='Purples',
                     title='Relationship Between Sleep Duration and Concentration Difficulty')
    fig9.update_layout(
        xaxis_title='Difficulty Concentrating',
        yaxis_title='Hours of Sleep'
    )
    st.plotly_chart(fig9, use_container_width=True)
else:
    st.warning("⚠️ Required columns for this visualization are missing.")

st.markdown("---")

st.success("✅ Objective 3 visualizations loaded successfully!")
