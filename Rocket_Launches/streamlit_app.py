import streamlit as st
from Rocket_Launches.analysis import run_failure_model
from Rocket_Launches.cleaning import clean_launch_data

def main():
    st.title("Rocket Launch Dashboard")
    
    # 1. Scrape/Clean
    cleaner = clean_launch_data()
    data = cleaner.get_launch_data()
    
    # 2. Analyze
    analyzer = run_failure_model(data)
    results = analyzer.run_stats()
    
    # 3. Display
    st.write(results)

if __name__ == "__main__":
    main()
    
    