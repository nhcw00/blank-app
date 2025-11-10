import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import kagglehub
from kagglehub import KaggleDatasetAdapter
from io import StringIO

# --- 0. Set Page Configuration ---
# This is the line to add for "wide mode"
st.set_page_config(layout="wide")

# --- 1. Load and Prepare Data (Cached) ---

@st.cache_data  # Cache the data loading for performance
def load_data():
    """
    Loads and prepares the accident data from the Kaggle dataset.
    Returns a tuple: (DataFrame, list_of_states, list_of_years)
    """
    try:
        # Set the path to the file you'd like to load from the dataset
        file_path = "US_Accidents_March23.csv"
        
        # Set pandas keyword arguments
        # Using a smaller sample for faster dashboard loading in this environment
        pandas_kwargs = {"nrows": 500000}

        # For Full dataset:
        # pandas_kwargs = {}

        st.info(f"Loading data from Kaggle dataset 'sobhanmoosavi/us-accidents' (file: {file_path})... (Sampled to 500k rows)")
        
        # Load the latest version using kagglehub
        df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            "sobhanmoosavi/us-accidents",
            file_path,
            pandas_kwargs=pandas_kwargs
        )
        st.success("Data loaded successfully!")

    except Exception as e:
        st.error(f"Error loading data from Kaggle: {e}")
        st.info("Please ensure you have internet connectivity and the 'kagglehub' library is installed (`pip install kagglehub[pandas-datasets]`).")
        return None, [], []

    # Select relevant columns
    columns_to_keep = [
        'State', 'Severity', 'Start_Time', 'Weather_Condition', 
        'Visibility(mi)', 'Temperature(F)', 'Wind_Speed(mph)', 
        'Start_Lat', 'Start_Lng'
    ]
    
    # Filter for columns that actually exist in the loaded data
    existing_columns = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_columns]

    # Clean data
    df.dropna(subset=existing_columns, inplace=True)

    # Convert Start_Time to datetime and extract year/month
    df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
    df.dropna(subset=['Start_Time'], inplace=True) # Drop rows where conversion failed
    df['Year'] = df['Start_Time'].dt.year
    df['Month'] = df['Start_Time'].dt.month
    df['YearMonth'] = df['Start_Time'].dt.to_period('M').astype(str)

    # Get options for filters
    available_states = sorted(df['State'].unique())
    available_years = sorted(df['Year'].unique())
    
    return df, available_states, available_years

# --- Load data ---
df, available_states, available_years = load_data()

# Stop execution if data loading failed
if df is None:
    st.stop()

# --- 2. App Title ---
st.title('US Traffic Accidents Dashboard')
st.markdown('An interactive dashboard to explore traffic accidents across the US.')

# --- 3. Sidebar Filters ---
st.sidebar.header("Filters")

# Check if states and years are available before creating filters
if not available_states or not available_years:
    st.sidebar.warning("No data available to configure filters.")
    st.stop()

# State Filter
selected_state = st.sidebar.selectbox(
    'Select State:',
    options=available_states,
    index=available_states.index('CA') if 'CA' in available_states else 0  # Default to California or first state
)

# Severity Filter
# Get unique severity levels from the dataframe for the options
severity_options = sorted(df['Severity'].unique())
selected_severities = st.sidebar.multiselect(
    'Select Severity Levels:',
    options=severity_options,
    default=severity_options  # Default: all selected
)

# Year Filter
selected_years = st.sidebar.select_slider(
    'Select Year Range:',
    options=available_years,
    value=(available_years[0], available_years[-1]) # Default: full range
)

# --- 4. Filter Data Based on Inputs ---
# This replaces the 'filter_data' callback
df_filtered = df[
    (df['State'] == selected_state) &
    (df['Severity'].isin(selected_severities)) &
    (df['Year'] >= selected_years[0]) &
    (df['Year'] <= selected_years[1])
].copy()

# --- 5. Display Visualizations ---
if df_filtered.empty:
    st.warning("No data found for the selected filters.")
else:
    # Create two columns for the first row of charts
    col1, col2 = st.columns(2)
    
    # --- Map Visualization (in col1) ---
    with col1:
        st.subheader(f'Accident Locations in {selected_state}')
        
        # Sample data for map performance if too large
        if len(df_filtered) > 10000:
            df_sample = df_filtered.sample(n=10000, random_state=1)
            st.info(f"Showing a random sample of 10,000 accidents out of {len(df_filtered):,}.")
        else:
            df_sample = df_filtered

        fig_map = px.scatter_mapbox(
            df_sample,
            lat="Start_Lat",
            lon="Start_Lng",
            color="Severity",
            color_continuous_scale=px.colors.diverging.Picnic,
            size_max=15,
            zoom=5,
            mapbox_style="open-street-map"
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    # --- Severity Distribution (in col2) ---
    with col2:
        st.subheader('Accident Severity Distribution')
        severity_counts = df_filtered['Severity'].value_counts().sort_index()
        fig_sev = px.bar(
            x=severity_counts.index,
            y=severity_counts.values,
            labels={'x': 'Severity Level', 'y': 'Number of Accidents'}
        )
        fig_sev.update_layout(xaxis=dict(tickmode='linear'), title_x=0.5, title_text='Accident Severity Distribution')
        st.plotly_chart(fig_sev, use_container_width=True)

    # Create two columns for the second row of charts
    col3, col4 = st.columns(2)
    
    # --- Accident Trend Over Time (in col3) ---
    with col3:
        st.subheader('Accident Trend Over Time (Monthly)')
        monthly_counts = df_filtered.groupby('YearMonth').size().reset_index(name='Accident Count')
        monthly_counts = monthly_counts.sort_values(by='YearMonth')

        fig_time = px.line(
            monthly_counts,
            x='YearMonth',
            y='Accident Count',
            markers=True
        )
        fig_time.update_layout(title_x=0.5, title_text='Accident Trend Over Time (Monthly)')
        st.plotly_chart(fig_time, use_container_width=True)

    # --- Weather Conditions (in col4) ---
    # This section applies the binned/rounded scatter plot logic
    with col4:
        st.subheader('Weather Condition Analysis')
        
        # Add the selectbox to choose the metric
        selected_metric_label = st.selectbox(
            'Select Weather Metric:',
            options=['Visibility', 'Temperature', 'Wind Speed'],
            index=0  # Default to 'Visibility'
        )

        # Map labels to actual column names
        metric_map = {
            'Visibility': 'Visibility(mi)',
            'Temperature': 'Temperature(F)',
            'Wind Speed': 'Wind_Speed(mph)'
        }
        selected_metric_col = metric_map[selected_metric_label]

        # --- NEW LOGIC: Bin, Count, and Scatter ---
        
        # 1. Clean data (filter outliers) based on selected metric
        if selected_metric_col == 'Wind_Speed(mph)':
            # Filter outliers for a better view
            dff_clean = df_filtered[df_filtered['Wind_Speed(mph)'] < 100].copy()
            xaxis_title = 'Wind Speed (mph, Rounded to nearest mph)'
        elif selected_metric_col == 'Visibility(mi)':
            # Filter to 20 miles to see the <10mi range better
            dff_clean = df_filtered[df_filtered['Visibility(mi)'] <= 20].copy()
            xaxis_title = 'Visibility (mi, Rounded to nearest mile)'
        else: # Temperature
            dff_clean = df_filtered.copy()
            xaxis_title = 'Temperature (F, Rounded to nearest degree)'

        if dff_clean.empty:
            st.warning("No data for this metric after cleaning outliers.")
        else:
            # 2. Bin the data by rounding to the nearest integer
            binned_col = f"{selected_metric_col}_Rounded"
            dff_clean[binned_col] = dff_clean[selected_metric_col].round()

            # 3. Aggregate to find frequency (Count)
            freq_data = dff_clean.groupby(binned_col).size().reset_index(name='Accident Frequency')

            # 4. Create the scatter plot
            chart_title = f'Accident Frequency by {selected_metric_label}'
            
            fig = px.scatter(
                freq_data,
                x=binned_col,
                y='Accident Frequency',
                title=chart_title,
                size='Accident Frequency', # Makes points with higher frequency larger
                hover_data={binned_col: True, 'Accident Frequency': True}
            )

            fig.update_layout(
                xaxis_title=xaxis_title,
                yaxis_title='Accident Frequency (Count)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
