import pandas as pd
import plotly.express as px

# Load dataset
url = 'https://raw.githubusercontent.com/FatinAthirah09/tutosv/refs/heads/main/student_survey_exported%20(1).csv'
df_url = pd.read_csv(url)

# Check column names
print(df_url.columns)

# Create pie chart (replace 'Your Age' with exact column name if different)
age_counts = df_url['Your Age'].value_counts().reset_index()
age_counts.columns = ['Your Age', 'Count']

# Plotly Pie Chart
fig = px.pie(
    age_counts,
    names='Your Age',
    values='Count',
    title='Distribution of Respondent Age',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(showlegend=False)
fig.show()

#Pie Chart

import plotly.express as px

# Count occurrences
age_counts = df['Your Age'].value_counts().reset_index()
age_counts.columns = ['Your Age', 'Count']

# Create Plotly pie chart
fig = px.pie(
    age_counts,
    names='Your Age',
    values='Count',
    title='Distribution of Respondent Age',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Optional: make it look nice
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(showlegend=False)

fig.show()
