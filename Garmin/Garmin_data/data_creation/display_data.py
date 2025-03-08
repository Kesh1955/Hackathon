## %
import json
import pandas as pd

with open("garmin_data_api.json", "r") as f:
    data = json.load(f)

print(data)



df = pd.DataFrame.from_dict(data, orient="index")
df.reset_index(inplace=True)
df.rename(columns={"index": "date"}, inplace=True)

df.head()
## %


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_garmin_metrics(df):
    """
    Expects a DataFrame with columns:
      - date (YYYY-MM-DD strings or datetime)
      - recovery_score
      - body_battery
      - sleep_hours
      - stress_level
    Creates individual line plots of these metrics over time.
    """

    # 1) Ensure 'date' is recognized as datetime, then sort by date
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date', inplace=True)

    # 2) For each numeric column, create a line plot vs. 'date'
    numeric_cols = ["recovery_score", "body_battery", "sleep_hours", "stress_level"]

    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.lineplot(data=df, x='date', y=col, marker='o')
        plt.title(f"{col.replace('_',' ').title()} Over Time")
        plt.xlabel("Date")
        plt.ylabel(col.replace('_',' ').title())
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


# Example usage:
# if __name__ == "__main__":
#     # Suppose you already loaded your JSON into a DataFrame 'df'
#     # with columns: date, recovery_score, body_battery, sleep_hours, stress_level
#     #
#     # e.g.:
#     # df = pd.DataFrame({
#     #    "date": ["2023-01-01","2023-01-02","2023-01-03","2023-01-04","2023-01-05"],
#     #    "recovery_score": [9.1, 28.7, 56.9, 15.1, 20.6],
#     #    "body_battery": [71.8, 75.4, 2.2, 52.4, 7.1],
#     #    "sleep_hours": [8.1, 7.7, 7.6, 3.7, 4.5],
#     #    "stress_level": [26, 22, 31, 49, 13]
#     # })
#     #
#     # Then just call:
plot_garmin_metrics(df)
