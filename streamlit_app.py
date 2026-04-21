import streamlit as st
import pandas as pd
import os
# Import analysis functions
from Rocket_Launches.analysis import (
    launches_per_year, 
    run_failure_model, 
    evaluate_model,
    launches_by_country
)

def main():
    st.set_page_config(page_title="Rocket Launch Tracker", page_icon="🚀")
    st.title("🚀 Rocket Launch Dashboard")

    # 1. LOAD DATA FROM BUNDLED CSV
    # Using a relative path to find the CSV inside your package folder
    DATA_PATH = os.path.join("data", "rocket_launches_dataset.csv")

    @st.cache_data
    def load_local_data():
        df = pd.read_csv(DATA_PATH)
        df['year'] = pd.to_numeric(df['year'])
        return df

    try:
        data = load_local_data()
        st.success("Dataset loaded successfully from package!")
    except FileNotFoundError:
        st.error(f"Could not find {DATA_PATH}. Check your file structure.")
        return

    # 2. VISUALIZATION
    st.subheader("Global Launch Activity")
    country_data = launches_by_country(data)
    # Using a built-in streamlit chart
    st.bar_chart(data=country_data, x="year", y="launch_count")

    # 3. ML MODEL SECTION
    st.divider()
    st.subheader("Predictive Analytics")
    st.write("Train a Logistic Regression model to predict launch failure based on year and location.")
    
    if st.button("Train Failure Model"):
        model, X_test, y_test = run_failure_model(data)
        metrics = evaluate_model(model, X_test, y_test)
        st.metric("Model Accuracy", f"{metrics['accuracy']:.2%}")

if __name__ == "__main__":
    main()