import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from datetime import datetime, timedelta


process_steps = ['Assembly', 'Quality Check', 'Packaging', 'Dispatch']

df = pd.read_csv('simulated_production_data.csv', parse_dates=['start_time', 'end_time'])


# Streamlit app begins here

st.title("Manufacturing Bottleneck Analysis Dashboard")

# Sidebar: Process step selection
process_choice = st.sidebar.selectbox("Select Process Step", process_steps)

# Sidebar: Forecast horizon selection (number of future cycles to forecast)
forecast_horizon = st.sidebar.selectbox("Select Forecast Horizon (in cycles)", [10, 20, 30, 40, 50])

# Filter data for the selected process step
selected_data = df[df['process_step'] == process_choice]

st.subheader(f"Descriptive Statistics for {process_choice}")
st.write(selected_data['duration_minutes'].describe())

# Plot histogram for the selected process step
fig_hist, ax_hist = plt.subplots(figsize=(6, 4))
sns.histplot(selected_data['duration_minutes'], bins=15, kde=True, ax=ax_hist)
ax_hist.set_title(f"{process_choice} Duration Distribution")
ax_hist.set_xlabel("Duration (min)")
st.pyplot(fig_hist)

# Show overall cycle time distribution for the entire production line
cycle_times = df.groupby('cycle_id')['duration_minutes'].sum().reset_index()
cycle_times.rename(columns={'duration_minutes': 'total_cycle_time'}, inplace=True)

st.subheader("Total Cycle Time Distribution")
fig_cycle, ax_cycle = plt.subplots(figsize=(6, 4))
sns.histplot(cycle_times['total_cycle_time'], bins=20, kde=True, ax=ax_cycle)
ax_cycle.set_title("Total Cycle Time per Cycle")
ax_cycle.set_xlabel("Total Cycle Time (min)")
st.pyplot(fig_cycle)

# ------------------------------------------
# PREDICTIVE MODELING SECTION
# ------------------------------------------
st.subheader(f"Forecast for {process_choice} Duration")

# Prepare time-series data: For each cycle, calculate the average duration for the chosen step.
# We assume cycle_id orders correspond to time.
time_series = selected_data.groupby('cycle_id')['duration_minutes'].mean()

st.write("Time series of average durations:")
st.line_chart(time_series)

# Fit an ARIMA model to the time series data.
# For simplicity, we use an ARIMA(1,0,1) model; in practice, you might perform parameter tuning.
try:
    model = sm.tsa.ARIMA(time_series, order=(1, 0, 1))
    model_fit = model.fit()
    
    # Forecast for the number of cycles chosen by the user
    forecast_result = model_fit.get_forecast(steps=forecast_horizon)
    forecast_values = forecast_result.predicted_mean
    forecast_conf_int = forecast_result.conf_int()

    st.write(f"Forecasted average duration for {forecast_horizon} future cycles:")
    st.write(forecast_values)

    # Plot the forecast along with confidence intervals
    fig_forecast, ax_forecast = plt.subplots(figsize=(8, 4))
    time_series.plot(ax=ax_forecast, label='Historical Data', marker='o')
    
    # Create forecast index
    forecast_index = np.arange(time_series.index.max() + 1, time_series.index.max() + forecast_horizon + 1)
    ax_forecast.plot(forecast_index, forecast_values, label='Forecast', marker='o', color='red')
    ax_forecast.fill_between(forecast_index, 
                             forecast_conf_int.iloc[:, 0], 
                             forecast_conf_int.iloc[:, 1], 
                             color='pink', alpha=0.3, label='Confidence Interval')
    ax_forecast.set_title(f"Forecast of {process_choice} Duration for Next {forecast_horizon} Cycles")
    ax_forecast.set_xlabel("Cycle ID")
    ax_forecast.set_ylabel("Duration (min)")
    ax_forecast.legend()
    st.pyplot(fig_forecast)
except Exception as e:
    st.error(f"Forecasting failed: {e}")

# ------------------------------------------
# Reporting: Show a sample of the raw data for transparency
#st.subheader("Raw Data Sample")
#st.write(df.head())
