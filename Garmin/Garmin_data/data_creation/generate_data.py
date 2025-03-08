import random
import json
import os
from datetime import date, timedelta

def generate_five_days_of_garmin_data():
    """
    Generates 5 days of fake Garmin data (Jan 1 to Jan 5).
    Outer key = date string (YYYY-MM-DD),
    Inner dict = {recovery_score, body_battery, sleep_hours, stress_level}.
    """
    start_date = date(2023, 1, 1)
    end_date = date(2023, 3, 1)
    current_day = start_date
    data_dict = {}

    while current_day <= end_date:
        recovery_score = round(random.uniform(0, 72), 1)
        body_battery = round(random.uniform(0, 100), 1)
        sleep_hours = round(random.uniform(3, 9), 1)
        stress_level = random.randint(0, 100)

        date_str = current_day.strftime("%Y-%m-%d")
        data_dict[date_str] = {
            "recovery_score": recovery_score,
            "body_battery": body_battery,
            "sleep_hours": sleep_hours,
            "stress_level": stress_level
        }

        current_day += timedelta(days=1)

    return data_dict

if __name__ == "__main__":
    # 1) Generate the data (Python dictionary)
    fake_5days_data = generate_five_days_of_garmin_data()

    # 2) Convert the dictionary to JSON (formatted nicely with indent=2)
    json_str = json.dumps(fake_5days_data, indent=2)
    print("JSON output:\n", json_str)

    # 3) Use os.path.join to build an absolute file path
    file_path = os.path.join(os.getcwd(), "garmin_data_api.json")
    print("Writing JSON to:", file_path)

    # 4) Write to that local file
    with open(file_path, "w") as f:
        f.write(json_str)

    # You can now open 'garmin_data_api.json' in any editor
    # and copy/paste the JSON if needed.

