# US Traffic Accidents Dashboard

This is an interactive web application built with Plotly and Dash to visualize and explore a large dataset of traffic accidents in the United States. It allows users to filter data and observe trends related to accident severity, location, time, and weather conditions. 

Explore the complete, interactive dashboard hosted on “Streamlit”. The findings and features discussed below are all drawn from this live application:

**Streamlit App** 
    - https://us-accident-u9x8vsxfvnjgfi5iwwvxtk.streamlit.app/
    This live version uses a **500,000-row sample for performance** due to **hosting limitations**.)

## Features

This dashboard provides several interactive visualizations that update based on your filter selections:

    - Accident Map: A scatter map showing the geographic location of accidents, colored by severity.
    - Severity Distribution: A bar chart showing the total number of accidents for each severity level (1-4).
    - Accident Trend: A line chart displaying the total number of accidents over time (grouped by month).    
    - Visibility Distribution: A bar chart showing how many accidents occurred under different visibility conditions (in miles).

## Filters

You can dynamically filter the entire dashboard using the controls at the top of the page:

    - Select State: Choose a single US state to focus on.    
    - Select Severity Levels: Toggle severity levels on or off to include or exclude them.    
    - Select Year Range: Use the slider to define a specific range of years.

## Data Source

This dashboard uses the US Accidents (2016 - 2023) dataset from Kaggle, provided by user Sobhan Moosavi.

    - Kaggle Dataset: sobhanmoosavi/us-accidents

The kagglehub library automatically downloads the necessary data file (US_Accidents_March23.csv) when you first run the script. No manual download is required.

### Note on Data Size

By default, this script is configured to load only the first 500,000 rows of the dataset.

If you want to analyze the entire dataset (over 7.7 million rows), you can change this line to an empty dictionary.

**Warning:** 
Loading the full dataset will require a significant amount of RAM (potentially 10GB+) and will make the dashboard much slower to load and interact with.
