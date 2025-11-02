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
This objective investigates **how sleep duration** and **sleep environment comfort** affect concentration, side effects, and overall well-being.
The visualizations focus on **patterns of discomfort and negative outcomes** among different sleep groups.
""")

# --- Summary Box: Key Findings (Replaced with HTML Cards) ---
st.header("💡 Key Findings Summary")

col1, col2, col3 = st.columns(3)

# Card 1: Comfort & Sleep Duration
with col1:
    st.markdown(
        f"""
        <div style="background-color:#E3F2FD;padding:15px;border-radius:15px;text-align:center;height:100%;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1); border-top: 5px solid #1976D2;">
            <h4 style="color:#1565C0; margin-top:0;">🛌 Comfort & Long Sleep</h4>
            <p style="color:#0D47A1; margin-bottom:0; font-size:14px;">
                Higher **Comfort Ratings** strongly correlate with **Longer Sleep Durations** (7-8 hours).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Card 2: Sleep Duration & Side Effects
with col2:
    st.markdown(
        f"""
        <div style="background-color:#FCE4EC;padding:15px;border-radius:15px;text-align:center;height:100%;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1); border-top: 5px solid #C2185B;">
            <h4 style="color:#AD1457; margin-top:0;">🤕 Short Sleep & Side Effects</h4>
            <p style="color:#880E4F; margin-bottom:0; font-size:14px;">
                **Shorter Sleep** (4-5 hours) leads to a **Significantly Higher Incidence** of side effects (fatigue, headaches).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Card 3: Comfort & Concentration
with col3:
    st.markdown(
        f"""
        <div style="background-color:#FFF3E0;padding:15px;border-radius:15px;text-align:center;height:100%;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1); border-top: 5px solid #F57C00;">
            <h4 style="color:#EF6C00; margin-top:0;'>🧠 Comfort & Focus</h4>
            <p style="color:#E65100; margin-bottom:0; font-size:14px;">
                **Highly Comfortable** environments link to **Less Frequent Difficulty** with concentration.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- End Summary Box ---

st.divider()

# --- Visualization 7: Comfort Ratings vs Average Sleep Hours ---
with st.expander("🛌 Comfort Ratings vs Average Sleep Hours", expanded=True):
    grouped_comfort = df.groupby(['How many hours of sleep do you get on average per night?', 'How would you rate the comfort of your sleeping environment']).size().reset_index(name='Count')
    fig7 = go.Figure()
    for sleep_group in sorted(grouped_comfort['How many hours of sleep do you get on average per night?'].unique()):
        data = grouped_comfort[grouped_comfort['How many hours of sleep do you get on average per night?'] == sleep_group]
        fig7.add_trace(go.Scatter(
            x=data['How would you rate the comfort of your sleeping environment'],
            y=data['Count'],
            mode='lines+markers',
            name=f'{sleep_group} hours'
        ))
    fig7.update_layout(title='Comfort of Sleeping Environment vs Average Hours of Sleep',
                        xaxis_title='Comfort Rating',
                        yaxis_title='Count',
                        legend_title='Sleep Hours')
    st.plotly_chart(fig7, use_container_width=True)

    # 📝 Interpretation for Fig 7
    st.markdown("""
    #### Interpretation: Environmental Impact on Duration
    The visualization demonstrates a positive correlation where groups reporting **longer sleep durations (7-8 hours)** exhibit a stronger preference for and higher count within the **'Very Comfortable'** rating category. This supports the hypothesis that a quality sleep environment, a modifiable factor, is a significant determinant in achieving medically recommended sleep length.
    """)

st.divider()

# --- Visualization 8: Average Sleep Hours vs Side Effects ---
with st.expander("🤕 Average Sleep Hours vs Side Effects from Late Sleeping", expanded=True):
    side_effects_df = df['Do you experience any of the following side effects from late sleeping?'].astype(str).str.get_dummies(sep=';')
    sleep_side_effects_df = pd.concat([df['How many hours of sleep do you get on average per night?'], side_effects_df], axis=1)
    sleep_side_effects_counts = sleep_side_effects_df.groupby('How many hours of sleep do you get on average per night?').sum()
    fig8 = px.imshow(sleep_side_effects_counts,
                      text_auto=True,
                      aspect="auto",
                      color_continuous_scale='Blues',
                      title='Average Sleep Hours vs Side Effects')
    st.plotly_chart(fig8, use_container_width=True)

    # 📝 Interpretation for Fig 8
    st.markdown("""
    #### Interpretation: Dose-Response Relationship
    The heatmap clearly illustrates a **dose-response relationship** between sleep deprivation and negative health outcomes. The highest incidence counts for side effects like **Fatigue, Irritability, and Headaches** are concentrated in the **4-5 hour sleep duration bracket**. This underscores the severe, immediate impact of chronic short sleep on physical and emotional well-being.
    """)

st.divider()

# --- Visualization 9: Concentration vs Comfort ---
with st.expander("🤯 Difficulty Concentrating by Sleep Environment Comfort", expanded=True):
    fig9 = px.bar(df,
                  x='How often do you find it hard to concentrate due to lack of sleep?',
                  facet_col='How would you rate the comfort of your sleeping environment',
                  facet_col_wrap=3,
                  color='How often do you find it hard to concentrate due to lack of sleep?',
                  title='Difficulty Concentrating by Sleep Environment Comfort')
    fig9.update_xaxes(title_text="Difficulty Concentrating", tickangle=-45)
    fig9.update_yaxes(title_text="Count")
    fig9.update_layout(showlegend=False)
    st.plotly_chart(fig9, use_container_width=True)

    # 📝 Interpretation for Fig 9
    st.markdown("""
    #### Interpretation: Environmental Moderation of Cognitive Function
    By comparing the distributions across the comfort facets, it is evident that individuals with **'Very Comfortable'** environments report the lowest frequency of severe concentration difficulty ('Always'). This implies that **improving the sleep environment acts as a moderating factor**, potentially leading to deeper, higher-quality sleep that better preserves cognitive functions necessary for focus and sustained attention.
    """)

st.divider()

## 🌟 Conclusion for Objective 3
st.success("""
The analysis for Objective 3 clearly establishes a link between **adequate sleep, environmental comfort, and better outcomes**.

Respondents who enjoy a **comfortable sleeping environment** generally achieve the recommended 7-8 hours of sleep. Conversely, those with **shorter sleep durations** (under 6 hours) consistently report a higher frequency of negative consequences, including **concentration difficulties** and various **side effects** like fatigue and irritability.

**The overall takeaway is that promoting both sufficient sleep hours and a comfortable sleep setting is crucial for minimizing negative well-being and cognitive outcomes.**
""")
