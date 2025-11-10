# US Traffic Accidents Dashboard

This is an interactive web application built with Plotly and Dash to visualize and explore a large dataset of traffic accidents in the United States. It allows users to filter data and observe trends related to accident severity, location, time, and weather conditions. 

Explore the complete, interactive dashboard hosted on “Streamlit”. The findings and features discussed below are all drawn from this live application:

**Streamlit App** 
    - https://us-accident-hksumaamuuhd4ejcrmejay.streamlit.app/
    
**NOTE**: This live version uses a **500,000-row sample for performance** due to **hosting limitations**.    

## Features

This dashboard provides several interactive visualizations that update based on your filter selections:

    - Accident Map: A scatter map showing the geographic location of accidents, colored by severity.
    - Severity Distribution: A bar chart showing the total number of accidents for each severity level (1-4).
    - Accident Trend: A line chart displaying the total number of accidents over time (grouped by month).
    - Weather Condition Analysis: An interactive scatter plot. Use the "Select Weather Metric" dropdown to switch the chart's x-axis between Visibility, Temperature, and Wind Speed to see how accident frequency changes with each metric.


## Filters

You can dynamically filter the entire dashboard using the controls at the top of the page:

    - Select State: Choose a single US state to focus on.    
    - Select Severity Levels: Toggle severity levels on or off to include or exclude them.    
    - Select Year Range: Use the slider to define a specific range of years.

## Data Source

This dashboard uses the US Accidents (2016 - 2023) dataset from Kaggle, provided by user Sobhan Moosavi.

    - Kaggle Dataset: sobhanmoosavi/us-accidents

The kagglehub library automatically downloads the necessary data file (US_Accidents_March23.csv) when you first run the script. No manual download is required.

