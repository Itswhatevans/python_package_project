import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# BASIC FEATURE HELPERS


def add_country(df):
    df = df.copy()
    df["country"] = df["location"].str.split(",").str[-1].str.strip()
    return df


# DESCRIPTIVE ANALYSIS

def launches_per_year(df):
    return df.groupby("year").size().reset_index(name="launch_count")


def status_by_year(df):
    return (
        df.groupby(["year", "status"])
        .size()
        .reset_index(name="count")
    )


def rocket_usage(df, top_n=10):
    top_rockets = df["rocket_family"].value_counts().head(top_n).index
    
    return (
        df[df["rocket_family"].isin(top_rockets)]
        .groupby(["year", "rocket_family"])
        .size()
        .reset_index(name="count")
    )


def status_by_location(df):
    return (
        df.groupby(["location", "status"])
        .size()
        .reset_index(name="count")
    )


def launches_by_country(df):
    df = add_country(df)
    
    return (
        df.groupby(["country", "year"])
        .size()
        .reset_index(name="launch_count")
    )


def run_failure_model(df):
    df = df.copy()

    # Keep only valid statuses
    valid_status = [
        "Launch Successful",
        "Launch Failure",
        "Launch was a Partial Failure"
    ]
    df = df[df["status"].isin(valid_status)]

    # Map to numeric (ONLY inside function)
    y = df["status"].map({
        "Launch Successful": 0,
        "Launch Failure": 1,
        "Launch was a Partial Failure": 1
    })

    # Features
    features = ["year", "location", "rocket_family"]
    df = df[features + ["status"]].dropna()
    X = df[features]

    # One-hot encode categorical variables
    X = pd.get_dummies(X, drop_first=True)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    return model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)

    return {
        "accuracy": accuracy_score(y_test, preds)
    }
