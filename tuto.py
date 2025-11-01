import streamlit as st
import pandas as pd
import plotly.express as px

# Set a wide layout for better chart viewing
st.set_page_config(layout="wide")

# The URL for the cleaned sleep data CSV
url = 'https://raw.githubusercontent.com/FatinAthirah09/IndividualSVAssignment/refs/heads/main/cleaned_sleep_data%20(3).csv'

## Data Loading and Preparation
# Use Streamlit's caching mechanism for efficient data loading
@st.cache_data 
def load_data(data_url):
    """Loads data from a URL into a DataFrame."""
    try:
        df = pd.read_csv(data_url)
        # Convert column names to lower case for easier access (optional but good practice)
        df.columns = df.columns.str.lower()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(url)

st.title("😴 Sleep Data Visualization")

if not df.empty:
    st.markdown("### Preview of the Data")
    st.dataframe(df)
    
    st.markdown("---")
    
#v1
import pandas as pd
import plotly.express as px

# Example: load your dataset (replace with your own df if already defined)
# df = pd.read_csv('your_dataset.csv')

# Get value counts
age_counts = df['Your Age'].value_counts().reset_index()
age_counts.columns = ['Your Age', 'Count']

# Create Plotly Pie Chart
fig = px.pie(
    age_counts,
    names='Your Age',
    values='Count',
    title='Distribution of Respondent Age',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Customize labels and layout
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(showlegend=False)

# Show interactive chart
fig.show()

