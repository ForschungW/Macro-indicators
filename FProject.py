import streamlit as st
import pandas as pd
import altair as alt
import requests
from dbnomics import fetch_series
from transformers import pipeline

# Title of the Streamlit app
st.title('Combined outlook of selected macroeconomic indicators')

# Define the two data sources
data_sources = {
    "CPI": "https://api.db.nomics.world/v22/series/IMF/CPI?facets=1&format=json&limit=1000&observations=1",
    "PGI": "https://api.db.nomics.world/v22/series/IMF/PGI?facets=1&format=json&limit=1000&observations=1"
}

# Function to fetch and process data
def fetch_data(source):
    response = requests.get(data_sources[source])
    if response.status_code == 200:
        data = response.json()
        frequencies = data.get('dataset', {}).get('dimensions_values_labels', {}).get('FREQ', {})
        ref_areas = data.get('dataset', {}).get('dimensions_values_labels', {}).get('REF_AREA', {})
        indicators = data.get('dataset', {}).get('dimensions_values_labels', {}).get('INDICATOR', {})
        return frequencies, ref_areas, indicators
    else:
        st.write(f"Failed to retrieve data for {source}: {response.status_code}")
        return {}, {}, {}

# Fetch metadata for both sources
freq_cpi, ref_area_cpi, indicator_cpi = fetch_data("CPI")
freq_pgi, ref_area_pgi, indicator_pgi = fetch_data("PGI")

# Create default values
default_freq_cpi = "A: Annual"
default_ref_area_cpi = "US: United States"
default_indicator_cpi = "PCPIA_IX: Consumer Price Index"

default_freq_pgi = "A: Annual"
default_ref_area_pgi = "US: United States"
default_indicator_pgi = "AIPMA_IX: Producer Price Index"

# Create searchable dropdown boxes for CPI with default values
selected_freq_cpi = st.selectbox('Select Frequency (CPI)', options=[f"{code}: {value}" for code, value in freq_cpi.items()], index=list(freq_cpi.keys()).index('A'))
selected_ref_area_cpi = st.selectbox('Select Reference Area (CPI)', options=[f"{code}: {value}" for code, value in ref_area_cpi.items()], index=list(ref_area_cpi.keys()).index('US'))
selected_indicator_cpi = st.selectbox('Select Indicator (CPI)', options=[f"{code}: {value}" for code, value in indicator_cpi.items()], index=list(indicator_cpi.keys()).index('PCPIA_IX'))

# Parse selected values for CPI
freq_code_cpi = selected_freq_cpi.split(":")[0].strip()
ref_area_code_cpi = selected_ref_area_cpi.split(":")[0].strip()
indicator_code_cpi = selected_indicator_cpi.split(":")[0].strip()

# Construct the user choice string for CPI
user_choice_cpi = f"IMF/CPI/{freq_code_cpi}.{ref_area_code_cpi}.{indicator_code_cpi}".upper()

# Create searchable dropdown boxes for PGI with default values
selected_freq_pgi = st.selectbox('Select Frequency (PGI)', options=[f"{code}: {value}" for code, value in freq_pgi.items()], index=list(freq_pgi.keys()).index('A'))
selected_ref_area_pgi = st.selectbox('Select Reference Area (PGI)', options=[f"{code}: {value}" for code, value in ref_area_pgi.items()], index=list(ref_area_pgi.keys()).index('US'))
selected_indicator_pgi = st.selectbox('Select Indicator (PGI)', options=[f"{code}: {value}" for code, value in indicator_pgi.items()], index=list(indicator_pgi.keys()).index('AIPMA_IX'))

# Parse selected values for PGI
freq_code_pgi = selected_freq_pgi.split(":")[0].strip()
ref_area_code_pgi = selected_ref_area_pgi.split(":")[0].strip()
indicator_code_pgi = selected_indicator_pgi.split(":")[0].strip()

# Construct the user choice string for PGI
user_choice_pgi = f"IMF/PGI/{freq_code_pgi}.{ref_area_code_pgi}.{indicator_code_pgi}".upper()

# Fetch and display data for CPI
st.write(f"Fetching data for: {user_choice_cpi}")
df_cpi = fetch_series(user_choice_cpi)
if isinstance(df_cpi, pd.DataFrame) and not df_cpi.empty:
    st.write("CPI Data fetched successfully")
    st.write(df_cpi.head())
else:
    st.write("CPI Data fetched but the DataFrame is empty or not valid")

# Fetch and display data for PGI
st.write(f"Fetching data for: {user_choice_pgi}")
df_pgi = fetch_series(user_choice_pgi)
if isinstance(df_pgi, pd.DataFrame) and not df_pgi.empty:
    st.write("PGI Data fetched successfully")
    st.write(df_pgi.head())
else:
    st.write("PGI Data fetched but the DataFrame is empty or not valid")

# Combine data and create a chart
if not df_cpi.empty and not df_pgi.empty:
    # Merge the data frames on the period column
    df_combined = pd.merge(df_cpi, df_pgi, on='period', suffixes=('_cpi', '_pgi'))
    
    # Let the user refine by selecting a time period
    start_date = st.date_input('Start date', value=pd.to_datetime(df_combined['period'].min()))
    end_date = st.date_input('End date', value=pd.to_datetime(df_combined['period'].max()))
    
    if start_date and end_date:
        mask = (df_combined['period'] >= pd.to_datetime(start_date)) & (df_combined['period'] <= pd.to_datetime(end_date))
        df_combined = df_combined.loc[mask]
    
    # Create the Altair chart
    chart = alt.Chart(df_combined).mark_line().encode(
        x='period:T',
        y='value_cpi',
        color=alt.value('blue')
    ).properties(
        title=f"Data for {indicator_code_cpi} from CPI"
    ) + alt.Chart(df_combined).mark_line().encode(
        x='period:T',
        y='value_pgi',
        color=alt.value('red')
    ).properties(
        title=f"Data for {indicator_code_pgi} from PGI"
    )

    # Display the chart in the Streamlit app
    st.altair_chart(chart, use_container_width=True)
    
# Easter egg joke
if st.button("Click for a surprise!"):
    st.write("Why did Salvador Dali and Einstein never get along? Because Dali was always too surreal for Einstein's reality!")

    # Generate AI analysis using Hugging Face
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    analysis_prompt = f"Analyze the following data trends:\n\n{df_combined[['period', 'value_cpi', 'value_pgi']].to_string(index=False)}"
    response = summarizer(analysis_prompt, max_length=150, min_length=30, do_sample=False)
    
    st.subheader("AI Analysis of the Graphs")
    st.write(response[0]['summary_text'])
else:
    st.write("No valid data to display the combined chart.")
