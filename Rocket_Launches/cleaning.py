import requests
import pandas as pd
import time

# --- CONSTANTS ---
# Keeping these at the top allows your other files to reference 
# the API targets if you ever decide to add a "Refresh Data" button.
URL_EARLY = 'https://ll.thespacedevs.com/2.2.0/launch/?limit=100'
URL_MODERN = "https://ll.thespacedevs.com/2.2.0/launch/?limit=200&net__gte=2015-01-01"
HEADERS = {"User-Agent": "Stat386RocketDataset"}

def get_launches(url, max_rows=1000):
    """
    Fetches raw launch data from The Space Devs API.
    """
    launches = []
    while url and len(launches) < max_rows:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            break

        data = response.json()
        for launch in data.get("results", []):
            launches.append({
                "name": launch["name"],
                "launch_date": launch["net"],
                "provider": launch["launch_service_provider"]["name"],
                "rocket": launch["rocket"]["configuration"]["name"],
                "launch_site": launch["pad"]["name"],
                "location": launch["pad"]["location"]["name"],
                "status": launch["status"]["name"]
            })

        url = data.get("next")
        # Respectful delay for API rate limits
        time.sleep(2)
        
    return pd.DataFrame(launches)

def clean_launch_data(df):
    """
    Applies logic to split strings, format dates, and filter columns.
    """
    if df.empty:
        print("Warning: DataFrame is empty.")
        return df

    # Split mission from rocket name
    if "name" in df.columns:
        df[["rocket_family", "mission"]] = df["name"].str.split(r"\|", n=1, expand=True)
        df["rocket_family"] = df["rocket_family"].str.strip()
        df["mission"] = df["mission"].str.strip()
        df = df.drop(columns=["name"])

    # Convert dates and extract year
    if "launch_date" in df.columns:
        df["launch_date"] = pd.to_datetime(df["launch_date"])
        df["year"] = df["launch_date"].dt.year

    # Standardize column set
    cols = [
        "rocket_family", "mission", "rocket", "provider", 
        "year", "launch_site", "location", "status"
    ]
    
    # Handle edge cases in launch site naming
    df["launch_site"] = df["launch_site"].replace(r"^\d+/\d+$", pd.NA, regex=True)

    # Filter to only existing columns from our list
    df = df[[c for c in cols if c in df.columns]]

    return df

def main():
    """
    ORCHESTRATOR: This logic ONLY runs when you execute this file directly.
    It will NOT run when Streamlit imports the functions above.
    """
    print("Initiating data collection...")
    
    # 1. Pull datasets
    df_early = get_launches(URL_EARLY, max_rows=500)
    print(f"Retrieved {len(df_early)} early records. Waiting for API cooldown...")
    time.sleep(10) 
    
    df_modern = get_launches(URL_MODERN, max_rows=500)
    print(f"Retrieved {len(df_modern)} modern records.")

    # 2. Clean and Label Eras
    df_early = clean_launch_data(df_early)
    df_modern = clean_launch_data(df_modern)
    df_early["era"] = "Space Race"
    df_modern["era"] = "Modern"

    # 3. Combine and Feature Engineering
    df = pd.concat([df_early, df_modern], ignore_index=True)
    df["country"] = df["location"].str.split(",").str[-1].str.strip()

    # 4. Export
    output_file = "rocket_launches_dataset.csv"
    df.to_csv(output_file, index=False)
    
    print("-" * 30)
    print(f"SUCCESS: {output_file} created.")
    print(f"Total Records: {df.shape[0]}")
    print(f"Years covered: {df['year'].min()} to {df['year'].max()}")
    print("-" * 30)

    return df

# This is the "Safety Switch" for Streamlit deployment
if __name__ == "__main__":
    main()