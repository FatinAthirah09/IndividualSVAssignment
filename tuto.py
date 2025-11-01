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
