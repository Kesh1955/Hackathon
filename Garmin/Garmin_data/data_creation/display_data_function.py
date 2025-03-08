import json
import pandas as pd
from tabulate import tabulate  # For a nice ASCII table display (pip install tabulate)

def display_5day_aggregate(json_file="garmin_5_days.json"):
    # 1) Load the JSON into a Python dict
    with open(json_file, "r") as f:
        data = json.load(f)

    # 2) Convert dict to a DataFrame
    #    The dict keys (dates) become the index; each value is a sub-dict of metrics
    df = pd.DataFrame.from_dict(data, orient="index")
    
    # Convert index to a column named 'date' for convenience
    df.reset_index(inplace=True)
    df.rename(columns={"index": "date"}, inplace=True)
    
    # 3) Print each day’s data in a table
    #    We'll use 'tabulate' for a nice ASCII table
    print("== Individual Daily Stats (past 5 days) ==\n")
    daily_table = tabulate(df, headers="keys", tablefmt="pretty", showindex=False)
    print(daily_table, "\n")

    # 4) Aggregate view
    #    Compute the mean, min, max, etc. for these numeric columns
    numeric_cols = ["recovery_score", "body_battery", "sleep_hours", "stress_level"]
    
    # Just an example: mean values
    means = df[numeric_cols].mean()
    
    # 5) Display aggregates
    print("== Aggregate Averages for the past 5 days ==\n")
    for col in numeric_cols:
        print(f"Average {col}: {means[col]:.2f}")
    
    # You could also show min, max, sum, etc. as needed
    mins = df[numeric_cols].min()
    maxs = df[numeric_cols].max()
    
    print("\n(Min / Max values)")
    for col in numeric_cols:
        print(f"{col}: min={mins[col]}, max={maxs[col]}")

if __name__ == "__main__":
    display_5day_aggregate("garmin_data_api.json")
