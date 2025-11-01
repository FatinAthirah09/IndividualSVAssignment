import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Load the cleaned sleep dataset from the repo.
    Caching keeps it from reloading each time a page reruns.
    """
    df = pd.read_csv("cleaned_sleep_data_3.csv")
    return df


def split_multi_select(df, column_name):
    """
    Splits a multi-select column (with ';' separators)
    and counts how many times each option appears.
    """
    reasons_df = df[column_name].str.get_dummies(sep=';')
    counts = reasons_df.sum().sort_values(ascending=False)
    return counts

