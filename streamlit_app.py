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
        
    st.header("⏳ The Evolution of Spaceflight")
    # Create two columns for side-by-side metrics
    col1, col2 = st.columns(2)

    with col1:
        space_race_data = data[data['era'] == 'Space Race']
        sr_success = (space_race_data['status'] == 'Launch Successful').mean()
        st.metric("Space Race Success Rate", f"{sr_success:.1%}")

    with col2:
        modern_data = data[data['era'] == 'Modern']
        mod_success = (modern_data['status'] == 'Launch Successful').mean()
        st.metric("Modern Success Rate", f"{mod_success:.1%}", delta=f"{mod_success - sr_success:.1%}")

    # Era-based Volume Chart
    st.subheader("Annual Launch Volume by Era")
    st.area_chart(data.groupby(['year', 'era']).size().unstack(fill_value=0))
    
    st.sidebar.header("Filter Analytics")

    # 1. Select Era
    era_choice = st.sidebar.multiselect("Select Era:", options=data['era'].unique(), default=data['era'].unique())

    # 2. Select Provider (Dynamic based on selected Era)
    filtered_df = data[data['era'].isin(era_choice)]
    providers = sorted(filtered_df['provider'].unique())
    selected_provider = st.sidebar.selectbox("Select Launch Provider:", ["All"] + providers)

    if selected_provider != "All":
        filtered_df = filtered_df[filtered_df['provider'] == selected_provider]

    # Now, use 'filtered_df' for all your charts below this point!
    st.write(f"Displaying {len(filtered_df)} launches for {selected_provider}")

if __name__ == "__main__":
    main()