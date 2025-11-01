import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Data Loading ---
@st.cache_data
def load_data():
    """Loads and returns the cleaned sleep data."""
    url = 'https://raw.githubusercontent.com/FatinAthirah09/IndividualSVAssignment/refs/heads/main/cleaned_sleep_data%20(3).csv'
    df = pd.read_csv(url)
    return df

df = load_data()

# --- Streamlit App Setup ---
st.set_page_config(layout="wide")
st.title("😴 Sleep Data Analysis Dashboard")
st.markdown("Exploring the relationships between sleep habits, demographics, and side effects using Plotly and Streamlit.")

# --- Helper Function for Multi-Select Column Splitting ---
def split_multi_select(df, column_name):
    """Splits a multi-select column and calculates the count of each option."""
    reasons_df = df[column_name].str.get_dummies(sep=';')
    counts = reasons_df.sum().sort_values(ascending=False)
    return counts

# --- Visualizations ---

## 1. Distribution of Respondent Age (Pie Chart)
st.header("1. 🎂 Age Distribution of Respondents")
age_counts = df['Your Age'].value_counts().reset_index()
age_counts.columns = ['Age', 'Count']
fig1 = px.pie(age_counts,
              values='Count',
              names='Age',
              title='Distribution of Respondent Age',
              hole=.3)
fig1.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

## 2. Gender Distribution by Occupation (Grouped Bar Chart)
st.header("2. 🧑‍💼 Gender Distribution by Occupation")
gender_occupation_counts = df.groupby(['What is your occupation?', 'What is your gender?']).size().reset_index(name='Count')
gender_occupation_counts.columns = ['Occupation', 'Gender', 'Count']
fig2 = px.bar(gender_occupation_counts,
              x='Occupation',
              y='Count',
              color='Gender',
              barmode='group',
              title='Gender Distribution by Occupation',
              labels={'Occupation': 'Occupation', 'Count': 'Count'},
              color_discrete_map={'Male': 'blue', 'Female': 'red', 'Other': 'green'}) # Customize colors if needed
fig2.update_layout(xaxis={'categoryorder':'total descending'}, xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

## 3. Distribution of Sleep Hours by Gender (Stacked Bar Chart)
st.header("3. 🌙 Distribution of Average Sleep Hours by Gender")
gender_sleep_counts = df.groupby(['What is your gender?', 'How many hours of sleep do you get on average per night?']).size().reset_index(name='Count')
gender_sleep_counts.columns = ['Gender', 'Sleep Hours', 'Count']
fig3 = px.bar(gender_sleep_counts,
              x='Gender',
              y='Count',
              color='Sleep Hours',
              barmode='stack',
              title='Distribution of Sleep Hours by Gender',
              labels={'Sleep Hours': 'Average Sleep Hours'})
fig3.update_layout(xaxis_tickangle=0)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

## 4. Difficulty Falling Asleep by Gender (Grouped Bar Chart)
st.header("4. 💤 Difficulty Falling Asleep by Gender")
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

## 5. Relationship between Concentration Difficulty and Falling Asleep (Heatmap)
st.header("5. 🤔 Concentration vs. Falling Asleep Difficulty")
concentration_difficulty_counts = df.groupby(['How often do you find it hard to concentrate due to lack of sleep?', 'Do you have difficulty falling asleep?']).size().unstack(fill_value=0)

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

## 6. Main Reasons for Sleeping Late by Age Group (Stacked Bar Chart)
st.header("6. ⏰ Main Reasons for Sleeping Late by Age Group")
# Split the multi-select column and group by age
reasons_df = df['What are the main reasons you sleep late?'].str.get_dummies(sep=';')
age_reasons_df = pd.concat([df['Your Age'], reasons_df], axis=1)
age_reasons_counts = age_reasons_df.groupby('Your Age').sum().reset_index()

# Convert the wide format to long format for Plotly Express
age_reasons_long = age_reasons_counts.melt(id_vars='Your Age', var_name='Reason', value_name='Count')

fig6 = px.bar(age_reasons_long,
              x='Your Age',
              y='Count',
              color='Reason',
              title='Main Reasons for Sleeping Late by Age Group',
              labels={'Your Age': 'Age Group', 'Count': 'Count of Reasons'},
              orientation='v')
fig6.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

## 7. Comfort of Sleeping Environment Ratings by Average Hours of Sleep (Line/Dot Plot)
st.header("7. 🛌 Comfort Ratings vs. Average Sleep Hours")
grouped_comfort = df.groupby(['How many hours of sleep do you get on average per night?', 'How would you rate the comfort of your sleeping environment']).size().reset_index(name='Count')
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
        line={'shape': 'linear'} # 'vlines' style is achieved via scatter plot with ordered x
    ))

fig7.update_layout(
    title='Comfort of Sleeping Environment Ratings by Average Hours of Sleep per Night',
    xaxis_title='Comfort Rating',
    yaxis_title='Count',
    legend_title='Average Hours of Sleep',
    xaxis={'categoryorder':'category ascending'}
)
st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")

## 8. Average Sleep Hours vs. Side Effects from Late Sleeping (Heatmap)
st.header("8. 🤕 Average Sleep Hours vs. Late Sleeping Side Effects")
# Split the multi-select column
side_effects_df = df['Do you experience any of the following side effects from late sleeping?'].str.get_dummies(sep=';')
sleep_side_effects_df = pd.concat([df['How many hours of sleep do you get on average per night?'], side_effects_df], axis=1)
sleep_side_effects_counts = sleep_side_effects_df.groupby('How many hours of sleep do you get on average per night?').sum()

fig8 = px.imshow(sleep_side_effects_counts,
                 text_auto=True,
                 aspect="auto",
                 color_continuous_scale='Blues',
                 title='Relationship between Average Sleep Hours and Side Effects from Late Sleeping')
fig8.update_layout(
    xaxis_title='Side Effects from Late Sleeping',
    yaxis_title='Average Sleep Hours per Night',
    xaxis_tickangle=-45
)
st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

## 9. Difficulty Concentrating by Sleep Environment Comfort (Bar Subplots)
st.header("9. 🤯 Difficulty Concentrating by Sleep Environment Comfort")

# Create a figure with subplots (faceting in Plotly)
fig9 = px.bar(df,
              x='How often do you find it hard to concentrate due to lack of sleep?',
              facet_col='How would you rate the comfort of your sleeping environment',
              facet_col_wrap=3,
              color='How often do you find it hard to concentrate due to lack of sleep?',
              title='Difficulty Concentrating by Sleep Environment Comfort Rating')

# Update layout for better readability
fig9.update_xaxes(title_text="Difficulty Concentrating", tickangle=-45)
fig9.update_yaxes(title_text="Count")
fig9.for_each_annotation(lambda a: a.update(text=f"Comfort Rating: {a.text.split('=')[-1]}"))
fig9.update_layout(showlegend=False)

st.plotly_chart(fig9, use_container_width=True)
