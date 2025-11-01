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
    st.dataframe(df.head())
    
    st.markdown("---")
    
    ## Plotly Visualization
    st.markdown("### Interactive Scatter Plot (e.g., Sleep Duration vs. Quality)")

    # Identify potential numeric columns for the chart (customize as needed)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if 'sleep duration' in numeric_cols and 'quality of sleep' in numeric_cols:
        # Create an interactive scatter plot using Plotly Express
        fig = px.scatter(
            df, 
            x='sleep duration', 
            y='quality of sleep',
            title='Sleep Duration vs. Quality of Sleep',
            hover_data=['person id', 'age'], # Include other columns in the hover tooltip
            color='gender' # Use a categorical column to differentiate points by color
        )
        
        # Display the Plotly figure in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Required numeric columns ('sleep duration' and 'quality of sleep') not found for the default plot.")
        
else:
    st.error("The DataFrame is empty. Please check the URL and CSV file.")
