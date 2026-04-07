import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

url_early = 'https://ll.thespacedevs.com/2.2.0/launch/?limit=100'
url_modern = "https://ll.thespacedevs.com/2.2.0/launch/?limit=200&net__gte=2015-01-01"

# Pull about 1000 launches:
headers = {"User-Agent": "Stat386RocketDataset"}

def get_launches(url, max_rows=1000):

    launches = []

    while url and len(launches) < max_rows:

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(response.status_code, response.text)
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

        time.sleep(2)

    return pd.DataFrame(launches)

# pull both datasets
df_early = get_launches(url_early, max_rows=500)
time.sleep(30)
df_modern = get_launches(url_modern, max_rows=500)

# clean both
def clean_launch_data(df):

    if df.empty:
        print("Warning: dataframe is empty")
        return df

    # Only split if name column exists
    if "name" in df.columns:
        df[["rocket_family", "mission"]] = df["name"].str.split(r"\|", n=1, expand=True)
        df["rocket_family"] = df["rocket_family"].str.strip()
        df["mission"] = df["mission"].str.strip()
        df = df.drop(columns=["name"])

    # Ensure launch_date is datetime
    if "launch_date" in df.columns:
        df["launch_date"] = pd.to_datetime(df["launch_date"])
        df["year"] = df["launch_date"].dt.year

    # Reorder columns only if they exist
    cols = [
        "rocket_family",
        "mission",
        "rocket",
        "provider",
        "year",
        "launch_site",
        "location",
        "status"
    ]
    
    # clean improper launch_site names
    df["launch_site"] = df["launch_site"].replace(r"^\d+/\d+$", pd.NA, regex=True)

    df = df[[c for c in cols if c in df.columns]]

    return df

# apply the cleaning functions
df_early = clean_launch_data(df_early)
df_modern = clean_launch_data(df_modern)

df_early.shape, df_modern.shape
df_early.columns, df_modern.columns

# Label the era
df_early["era"] = "Space Race"
df_modern["era"] = "Modern"

# combine
df = pd.concat([df_early, df_modern], ignore_index=True)

# Save final dataset
df.to_csv("rocket_launches_dataset.csv", index=False)

# Summary stats
df["year"].describe()
df["provider"].value_counts().head()
df.groupby("year").size()

print(df_early.shape)
print(df_modern.shape)

print(df["year"].unique())

df_early.shape, df_modern.shape
df_early.columns, df_modern.columns

# Set of summary stats
df.shape 
df.sample(5, random_state=1) 
df.isna().sum()

# Isolate country from location:
df["country"] = df["location"].str.split(",").str[-1].str.strip()

df.groupby(["country","year"]).size().unstack(fill_value=0)




def main():
    # pull both datasets
    df_early = get_launches(url_early, max_rows=500)
    time.sleep(30)
    df_modern = get_launches(url_modern, max_rows=500)

    # clean both
    df_early = clean_launch_data(df_early)
    df_modern = clean_launch_data(df_modern)

    # Label the era
    df_early["era"] = "Space Race"
    df_modern["era"] = "Modern"

    # combine
    df = pd.concat([df_early, df_modern], ignore_index=True)

    # Isolate country from location:
    df["country"] = df["location"].str.split(",").str[-1].str.strip()

    # Save final dataset
    df.to_csv("rocket_launches_dataset.csv", index=False)

    # Optional: summary stats
    print(df_early.shape)
    print(df_modern.shape)
    print(df["year"].unique())
    print(df.sample(5, random_state=1))
    print(df.isna().sum())

    return df


if __name__ == "__main__":
    main()