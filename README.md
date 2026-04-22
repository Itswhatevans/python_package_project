### Authors: Jordan Evans and Trent Peterson
# 🚀 Rocket Launch Evolution Dashboard

A data-driven exploration of orbital spaceflight, comparing the **Space Race Era** with the **Modern Era**. This project leverages a custom Python package to scrape, clean, and analyze launch data, culminating in a machine-learning-powered reliability prediction dashboard.

## 📊 Project Overview
The primary goal of this analysis is to quantify how rocket launch success rates and provider landscapes have shifted over the last 60 years. By sampling 500 launches from the early Space Race and 500 from the modern commercial era, this tool identifies trends in global reliability and provides predictive insights.

### Key Features
*   **Era Comparison:** Side-by-side metrics comparing 1960s-era mission success vs. 2020s-era efficiency.
*   **Interactive Analytics:** Filter by era or specific launch providers (e.g., NASA, SpaceX, Roscosmos) to see localized performance.
*   **Failure Prediction Model:** A Logistic Regression model trained on historical data to predict the likelihood of launch failure based on year, location, and rocket family.
*   **Automated Pipeline:** Custom cleaning and analysis modules built as a reusable Python package.

## 🛠️ Project Structure
```text
├── streamlit_app.py          # Streamlit Dashboard (UI/UX)
├── requirements.txt           # Python dependencies
├── Rocket_Launches/           # Core Package
│   ├── __init__.py            # Package initialization
│   ├── cleaning.py            # API scraping and data wrangling
│   ├── analysis.py            # ML model and statistical helpers
│   └── rocket_launches_dataset.csv  # Pre-scraped dataset
└── README.md
```

## Installation and Usage
### Clone the Repository
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

### Install dependencies
pip install -r requirements.txt

### Run the Dashboard
stramlit run streamlit_app.py

## 🧪 Machine Learning Methodology
The "Predictive Analytics" section utilizes a Logistic Regression model.
- Features (X): Year, Launch Site, Rocket Family, and Era.
- Target (y): Binary outcome (0 = Success, 1 = Failure/Partial Failure).
- Processing: Categorical variables are converted via One-Hot Encoding to allow the model to weight the reliability of specific locations and rocket families.

## 🛰️ Data Source 
Data is sourced from the [https://ll.thespacedevs.com/2.2.0/launch/](The Space Devs (Launch Library 2)), a comprehensive API for historical and upcoming spaceflight data