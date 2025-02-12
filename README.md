Manufacturing Bottleneck Detection and Forecasting

Overview:
  This project simulates a manufacturing production line to detect bottlenecks—points where delays occur—and forecast future delays. By analyzing production cycles and using predictive modeling, it enables proactive decision-making to optimize efficiency and reduce downtime.
    
Objective:
  1. Simulate a production line with key process steps: Assembly → Quality Check → Packaging → Dispatch.
  2. Identify bottlenecks, particularly in the Quality Check phase, where delays are injected in 30% of cycles.
  3. Forecast future delays using time series modeling, allowing better scheduling and resource allocation.
  4. Build interactive dashboards for real-time monitoring and decision-making.

Key Components and Methodology:
 1. Data Simulation
    Production Cycle Simulation:
    Simulates 500 production cycles, each moving through Assembly → Quality Check → Packaging → Dispatch.
    Injecting Delays:
    The Quality Check step is programmed to experience an extra delay 30% of the time, mimicking real-world bottlenecks.
2. Data Processing & Analysis
    Data Cleaning & Validation:
    Ensures accurate timestamps, cycle durations, and step sequences.
    Exploratory Data Analysis (EDA):
    Computes descriptive statistics and visualizes processing time distributions to detect slow process steps.
    Feature Engineering:
    Generates new metrics like total cycle time and delay flags (indicating if a step exceeds a set threshold).

 3. Predictive Modeling
    Time Series Forecasting:
    Aggregates average processing times per cycle for a selected process step (e.g., Quality Check).
    Fits an ARIMA model to predict future durations.
    User-Defined Forecast Horizon:
    Allows users to forecast processing durations for the next 10, 20, 30, 40, or 50 cycles.

 4. Dashboarding & Deployment
    Streamlit App:
    Interactive web app for data visualization and forecasting.
    Users can select a process step and forecast horizon, view statistics, histograms, and trend predictions.
    Tableau Public Dashboard: https://public.tableau.com/views/BottleneckForecasting/Sheet2?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link
    Interactive visualizations including time series plots and histograms.
    Parameter controls allow users to explore different scenarios.
    Potential JavaScript API integration for dynamic embedding.

Tech Stack:
  Python (Pandas, NumPy, Matplotlib, Seaborn, Statsmodels),
  Time Series Forecasting (ARIMA Model),
  Streamlit (Web App),
  Tableau Public (Data Visualization)


