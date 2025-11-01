import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app_helpers import load_data

# --- Load data ---
df = load_data()
df.columns = df.columns.str.strip()

# --- Page setup ---
st.title("🧠 Objective 3: Analyze the Relationship Between Sleep Duration, Discomfort, and Negative Outcomes")
st.markdown("""
This objective analyzes the relationship between sleep duration, comfort levels, and the negative outcomes 
that result from poor sleep quality.
""")

st.markdown("---")

## 7️⃣ Comfort of Sleeping Environment Ratings by Average Hours of Sleep (Line/Dot Plot)
st.header("7️⃣ 🛌 Comfort Ratings vs. Average Sleep Hours")

grouped_comfort = df.groupby(
    ['How many hours of sleep do you get on average per night?',
     'How would you rate the comfort of your sleeping environment']
).size().reset_index(name='Count')

grouped_comfort.columns = ['Sleep Hours', 'Comfort Rating', 'Count']

# Order the Sleep Hours for better visualization
sleep_order = sorted(grouped_comfort['Sleep Hours'].unique())

fig7 = go.Figure()

# Create a line and marker trace for each average sleep hour group
for sleep_group in sleep_order:
    data = grouped_comfort[grouped_comfort['Sleep Hours'] == sleep_group]
    fig7.add_trace(go.Scatter(
        x=data['Comfort Rating'],
        y=data['Count'],
        mode='lines+markers',
        name=f'{sleep_group} hours',
        line={'shape': 'linear'}
    ))

fig7.update_layout(
    title='Comfort of Sleeping Environment Ratings by Average Hours of Sleep per Night',
    xaxis_title='Comfort Rating',
    yaxis_title='Count',
    legend_title='Average Hours of Sleep',
    xaxis={'categoryorder': 'category ascending'}
)
st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")

## 8️⃣ Average Sleep Hours vs. Side Effects from Late Sleeping (Heatmap)
st.header("8️⃣ 🤕 Average Sleep Hours vs. Late Sleeping Side Effects")

# Split the multi-select column
side_effects_df = df['Do you experience any of the following side effects from late sleeping?'].str.get_dummies(sep=';')
sleep_side_effects_df = pd.concat(
    [df['How many hours of sleep do you get on average per night?'], side_effects_df],
    axis=1
)
sleep_side_effects_counts = sleep_side_effects_df.groupby(
    'How many hours of sleep do you get on average per night?'
).sum()

fig8 = px.imshow(
    sleep_side_effects_counts,
    text_auto=True,
    aspect="auto",
    color_continuous_scale='Blues',
    title='Relationship between Average Sleep Hours and Side Effects from Late Sleeping'
)
fig8.update_layout(
    xaxis_title='Side Effects from Late Sleeping',
    yaxis_title='Average Sleep Hours per Night',
    xaxis_tickangle=-45
)
st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

## 9️⃣ Difficulty Concentrating by Sleep Environment Comfort (Bar Subplots)
st.header("9️⃣ 🤯 Difficulty Concentrating by Sleep Environment Comfort")

fig9 = px.bar(
    df,
    x='How often do you find it hard to concentrate due to lack of sleep?',
    facet_col='How would you rate the comfort of your sleeping environment',
    facet_col_wrap=3,
    color='How often do you find it hard to concentrate due to lack of sleep?',
    title='Difficulty Concentrating by Sleep Environment Comfort Rating'
)

# Update layout for better readability
fig9.update_xaxes(title_text="Difficulty Concentrating", tickangle=-45)
fig9.update_yaxes(title_text="Count")
fig9.for_each_annotation(lambda a: a.update(text=f"Comfort Rating: {a.text.split('=')[-1]}"))
fig9.update_layout(showlegend=False)

st.plotly_chart(fig9, use_container_width=True)

st.markdown("---")

st.success("✅ Objective 3 visualizations displayed successfully!")
