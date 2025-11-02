import streamlit as st
import plotly.express as px
import pandas as pd
from app_helpers import load_data

# --- Load Data ---
df = load_data()

# --- Page Config ---
st.title("🎯 Objective 1: Understand the Sample Demographics and Baseline Behaviors")
st.markdown("""
This objective focuses on identifying **demographic characteristics** and **baseline sleep patterns** among respondents.
The visualizations below explore participants’ **age, gender, and sleep duration** patterns.
""")

st.divider()

# --- 📊 Key Demographic Metrics Section (Original Stylish HTML Cards Restored) ---
st.header("📈 Key Demographic Metrics")

# Basic calculations
total_respondents = len(df)
age_groups = df['Your Age'].nunique()
# Calculate the mode of sleep hours
avg_sleep = df['How many hours of sleep do you get on average per night?'].mode()[0]
gender_counts = df['What is your gender?'].value_counts()
main_gender = gender_counts.index[0] # Get the most frequent gender
main_gender_count = gender_counts.values[0]

# --- Stylish Metric Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style="background-color:#E8F5E9;padding:20px;border-radius:15px;text-align:center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <h4 style="color:#2E7D32;">👥 Total Respondents</h4>
            <h2 style="color:#1B5E20;">{total_respondents}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="background-color:#FFF3E0;padding:20px;border-radius:15px;text-align:center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <h4 style="color:#E65100;">🎂 Distinct Age Groups</h4>
            <h2 style="color:#BF360C;">{age_groups}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style="background-color:#E3F2FD;padding:20px;border-radius:15px;text-align:center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <h4 style="color:#1565C0;">😴 Most Common Sleep Duration</h4>
            <h2 style="color:#0D47A1;">{avg_sleep} hours</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("### 👩‍🦰 Gender Breakdown Table")
gender_breakdown = pd.DataFrame({
    'Gender': gender_counts.index,
    'Count': gender_counts.values
})
st.dataframe(gender_breakdown, use_container_width=True, hide_index=True)

st.divider()

# --- Visualization 1: Age Distribution ---
with st.expander("🎂 Age Distribution of Respondents (Pie Chart)", expanded=True):
    age_counts = df['Your Age'].value_counts().reset_index()
    age_counts.columns = ['Age', 'Count']
    fig1 = px.pie(age_counts, values='Count', names='Age',
                  title='Distribution of Respondent Age Groups', hole=.3)
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)
    
    # 📝 Interpretation for Fig 1
    st.markdown("""
    #### Interpretation: Sample Focus
    The dominant presence of respondents from specific age groups (e.g., 18-25 years) indicates that the subsequent findings regarding sleep habits and issues will be **most representative of the behavior and challenges faced by young adults/students**. This demographic focus should be acknowledged when generalizing results.
    """)

st.divider()

# --- Visualization 2: Gender Distribution by Occupation ---
with st.expander("🧑‍💼 Gender Distribution across Occupations", expanded=True):
    gender_occupation_counts = df.groupby(
        ['What is your occupation?', 'What is your gender?']
    ).size().reset_index(name='Count')

    fig2 = px.bar(gender_occupation_counts,
                  x='What is your occupation?',
                  y='Count',
                  color='What is your gender?',
                  barmode='group',
                  title='Gender Distribution by Occupation',
                  labels={'What is your occupation?': 'Occupation', 'Count': 'Count'})
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)
    
    # 📝 Interpretation for Fig 2
    st.markdown("""
    #### Interpretation: Potential Bias
    The clear imbalance in representation across occupation and gender categories (e.g., higher participation from one gender within the 'Student' category) suggests a **sampling bias**. This implies that differences observed in sleep patterns might be attributable to lifestyle factors inherent to the over-represented groups rather than just biological gender or occupational stress.
    """)

st.divider()

# --- Visualization 3: Sleep Hours by Gender ---
with st.expander("🌙 Sleep Duration Patterns by Gender", expanded=True):
    gender_sleep_counts = df.groupby(
        ['What is your gender?', 'How many hours of sleep do you get on average per night?']
    ).size().reset_index(name='Count')

    # Ensure sleep hours are ordered correctly for better visual presentation
    sleep_order = sorted(gender_sleep_counts['How many hours of sleep do you get on average per night?'].unique())
    gender_sleep_counts['How many hours of sleep do you get on average per night?'] = pd.Categorical(
        gender_sleep_counts['How many hours of sleep do you get on average per night?'],
        categories=sleep_order,
        ordered=True
    )
    gender_sleep_counts = gender_sleep_counts.sort_values('How many hours of sleep do you get on average per night?')

    fig3 = px.bar(gender_sleep_counts,
                  x='What is your gender?',
                  y='Count',
                  color='How many hours of sleep do you get on average per night?',
                  barmode='stack',
                  title='Distribution of Sleep Hours by Gender',
                  labels={'How many hours of sleep do you get on average per night?': 'Sleep Hours'})
    st.plotly_chart(fig3, use_container_width=True)
    
    # 📝 Interpretation for Fig 3
    st.markdown("""
    #### Interpretation: Baseline Risk
    While **{avg_sleep} hours** is the most common duration (suggesting a majority meet the minimum recommended sleep), the visual presence of many respondents in the **5 hours or less** categories across all genders highlights a significant minority already engaging in chronic sleep deprivation. This establishes a high-risk baseline that needs further investigation in Objectives 2 and 3.
    """.format(avg_sleep=avg_sleep))

st.divider()

## 🌟 Conclusion for Objective 1: Sample Demographics and Baseline Behaviors
st.success(f"""
The analysis for Objective 1 provides a clear profile of the survey participants and their **baseline sleep habits**:

* **Sample Characteristics:** The survey successfully captured data across **{age_groups} distinct age groups**. The sample is dominated by **{main_gender}** respondents, who account for the largest share of the dataset ({main_gender_count} respondents).
* **Occupational Distribution:** The gender breakdown varies significantly across occupations, which may introduce biases that need to be considered in later, deeper analysis.
* **Baseline Sleep:** The **modal (most common) average sleep duration** among all respondents is **{avg_sleep} hours**. While this suggests a central tendency around the recommended sleep range, the full distribution of the stacked bar chart shows significant portions of the sample are falling both below and above this mode.
""")
