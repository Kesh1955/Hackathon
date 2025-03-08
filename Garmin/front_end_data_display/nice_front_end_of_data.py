# main.py

# Import necessary packages
# FastAPI - Modern, fast web framework for building APIs
# HTTPException - For returning proper HTTP error responses
# Query - For adding metadata to query parameters
from fastapi import FastAPI, HTTPException, Query

# HTMLResponse - For returning HTML content instead of JSON
from fastapi.responses import HTMLResponse

# Pydantic - For data validation and settings management
# BaseModel - The base class for all Pydantic models
# Field - For adding metadata and validation to model fields
from pydantic import BaseModel, Field

# List - For type hinting lists
from typing import List

# datetime - For formatting dates in the UI
from datetime import datetime

# Define Pydantic models for data validation and serialization
# Why: Using Pydantic models gives us automatic validation, documentation,
# and helps ensure our data is correctly structured throughout the application
class FitnessMetrics(BaseModel):
    """
    Data model for fitness metrics
    
    Why: This creates a clear, self-documenting contract for what fitness data should contain.
    How: By inheriting from BaseModel, we get automatic validation and serialization.
    """
    # Field() adds metadata and validation rules to each field
    recovery_score: float = Field(..., description="Recovery score between 0-100")
    body_battery: float = Field(..., description="Body battery level between 0-100")
    sleep_hours: float = Field(..., description="Hours of sleep")
    stress_level: int = Field(..., description="Stress level between 0-100")
    # Note: The '...' means the field is required

class FitnessDataResponse(BaseModel):
    """
    Response model for fitness data requests
    
    Why: Having a response model ensures consistent API output and enables auto-documentation.
    How: We compose this from a date string and our FitnessMetrics model.
    """
    date: str  # The date for this fitness data
    data: FitnessMetrics  # The actual metrics, using our defined model

# Initialize FastAPI app
# Why: FastAPI provides modern API functionality with automatic OpenAPI documentation
app = FastAPI(title="Fitness Data API")

# Sample fitness tracking data
# Why: In a real app, this would come from a database, but for demo purposes
# we're using a simple dictionary.
# How: Using a dictionary with date strings as keys and metric dictionaries as values
SAMPLE_DATA = {
    "2023-01-01": {"recovery_score": 9.1, "body_battery": 71.8, "sleep_hours": 8.1, "stress_level": 26},
    "2023-01-02": {"recovery_score": 28.7, "body_battery": 75.4, "sleep_hours": 7.7, "stress_level": 22},
    "2023-01-03": {"recovery_score": 56.9, "body_battery": 2.2, "sleep_hours": 7.6, "stress_level": 31},
    "2023-01-04": {"recovery_score": 15.1, "body_battery": 52.4, "sleep_hours": 3.7, "stress_level": 49},
    "2023-01-05": {"recovery_score": 20.6, "body_battery": 7.1, "sleep_hours": 4.5, "stress_level": 13},
    "2023-01-06": {"recovery_score": 5.3, "body_battery": 12.2, "sleep_hours": 5.4, "stress_level": 78},
    "2023-01-07": {"recovery_score": 65.6, "body_battery": 32.5, "sleep_hours": 5.8, "stress_level": 70}
}

# API endpoint to get all available dates
# Why: This provides the frontend with a list of dates that have data available
# How: We define an async handler that returns the dictionary keys as a list
@app.get("/api/dates", response_model=List[str])
async def get_dates():
    """
    Get all dates with available fitness data
    
    Why: The frontend needs to know which dates have data for the dropdown menu.
    How: We extract and return the keys from our data dictionary.
    
    Returns:
        List[str]: A list of date strings in YYYY-MM-DD format
    """
    return list(SAMPLE_DATA.keys())

# API endpoint to get data for a specific date
# Why: This is the main data endpoint that provides metrics for visualization
# How: We look up the date in our data and return it wrapped in our response model
@app.get("/api/data/{date}", response_model=FitnessDataResponse)
async def get_data_for_date(date: str):
    """
    Get fitness data for a specific date
    
    Why: The frontend needs detailed metrics for the selected date.
    How: We look up the date in our data dictionary and return a structured response.
    
    Args:
        date (str): Date string in YYYY-MM-DD format
        
    Returns:
        FitnessDataResponse: Object containing date and fitness metrics
        
    Raises:
        HTTPException: 404 error if date is not found
    """
    # Check if the requested date exists in our data
    if date not in SAMPLE_DATA:
        # Return a proper HTTP 404 error with a helpful message
        # Why: This gives the client clear feedback on what went wrong
        raise HTTPException(status_code=404, detail=f"No data found for date {date}")
    
    # Return the data wrapped in our response model structure
    # FastAPI automatically validates this against our Pydantic model
    return {"date": date, "data": SAMPLE_DATA[date]}

# Main endpoint that serves the HTML visualization
# Why: For demo purposes, we're serving a complete visualization directly from the API
# In a production app, this would typically be separated into a frontend application
@app.get("/", response_class=HTMLResponse)
async def get_visualization(date: str = Query("2023-01-01", description="Date in format YYYY-MM-DD")):
    """
    Render HTML visualization for the selected date
    
    Why: This provides a complete, self-contained demo in a single endpoint.
    How: We generate HTML with embedded CSS that displays the fitness metrics.
    
    Args:
        date (str): Date to display, from query parameter (defaults to 2023-01-01)
        
    Returns:
        HTMLResponse: Complete HTML page with the visualization
    """
    # Default to first date if requested date is not available
    # Why: This ensures we always show something, even if the date is invalid
    if date not in SAMPLE_DATA:
        date = list(SAMPLE_DATA.keys())[0]
    
    # Get data for selected date
    data = SAMPLE_DATA[date]
    
    # Format date for display (e.g., "January 01, 2023")
    # Why: Makes the date more readable in the UI
    display_date = datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")
    
    # Build HTML content
    # Why: For a simple demo, embedding HTML directly is the most straightforward approach
    # How: We use an f-string to insert dynamic data into our HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Score Today</title>
        <style>
            /* Base styling for the page */
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f7f9fc;
                color: #333;
            }}
            /* Container to center and constrain the content width */
            .container {{
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }}
            /* Page title styling */
            h1 {{
                text-align: center;
                color: #2c3e50;
                margin-bottom: 5px;
            }}
            /* Date display styling */
            .subtitle {{
                text-align: center;
                color: #7f8c8d;
                margin-bottom: 30px;
                font-size: 1.1em;
            }}
            /* Container for the date selector */
            .date-selector {{
                margin: 20px 0;
                text-align: center;
            }}
            /* Grid layout for the four metric cards */
            .metrics {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);  /* Two columns */
                gap: 20px;
                margin-top: 30px;
            }}
            /* Individual metric card styling */
            .metric-card {{
                background-color: #f8fafc;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            }}
            /* Metric name styling */
            .metric-title {{
                font-size: 1.1em;
                color: #7f8c8d;
                margin-bottom: 10px;
                font-weight: 500;
            }}
            /* Metric value (number) styling */
            .metric-value {{
                font-size: 2.5em;
                font-weight: 700;
                margin: 10px 0;
            }}
            /* Metric description text styling */
            .metric-desc {{
                font-size: 0.9em;
                color: #7f8c8d;
            }}
            /* Color coding for different metrics and values */
            /* Base colors (poor values) */
            .recovery {{ color: #e74c3c; }}  /* Red */
            .battery {{ color: #e74c3c; }}
            .sleep {{ color: #e74c3c; }}
            .stress {{ color: #e74c3c; }}
            
            /* Good value modifiers (green) */
            .recovery.good {{ color: #27ae60; }}
            .battery.good {{ color: #27ae60; }}
            .sleep.good {{ color: #27ae60; }}
            .stress.good {{ color: #27ae60; }}
            
            /* Medium value modifiers (orange) */
            .recovery.medium {{ color: #f39c12; }}
            .battery.medium {{ color: #f39c12; }}
            .sleep.medium {{ color: #f39c12; }}
            .stress.medium {{ color: #f39c12; }}
            
            /* Date selector dropdown styling */
            select {{
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ddd;
                font-size: 1em;
                background-color: white;
                cursor: pointer;
                min-width: 200px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Page title -->
            <h1>Your Score Today</h1>
            <!-- Current date display -->
            <div class="subtitle">{display_date}</div>
            
            <!-- Date selector dropdown -->
            <div class="date-selector">
                <select id="date-select" onchange="window.location.href='/?date=' + this.value">
                    <!-- Generate options for each available date -->
                    {"".join([f'<option value="{d}" {"selected" if d == date else ""}>{datetime.strptime(d, "%Y-%m-%d").strftime("%B %d, %Y")}</option>' for d in SAMPLE_DATA])}
                </select>
            </div>
            
            <!-- Grid layout for the four metric cards -->
            <div class="metrics">
                <!-- Recovery Score Card -->
                <div class="metric-card">
                    <div class="metric-title">Recovery Score</div>
                    <!-- Value with conditional color class based on the score -->
                    <div class="metric-value recovery {'good' if data['recovery_score'] > 50 else 'medium' if data['recovery_score'] > 25 else ''}">{data['recovery_score']}</div>
                    <!-- Description text based on the score value -->
                    <div class="metric-desc">
                        {'Excellent recovery' if data['recovery_score'] > 50 else 'Average recovery' if data['recovery_score'] > 25 else 'Poor recovery'}
                    </div>
                </div>
                
                <!-- Body Battery Card -->
                <div class="metric-card">
                    <div class="metric-title">Body Battery</div>
                    <div class="metric-value battery {'good' if data['body_battery'] > 50 else 'medium' if data['body_battery'] > 25 else ''}">{data['body_battery']}</div>
                    <div class="metric-desc">
                        {'High energy levels' if data['body_battery'] > 50 else 'Moderate energy' if data['body_battery'] > 25 else 'Low energy levels'}
                    </div>
                </div>
                
                <!-- Sleep Hours Card -->
                <div class="metric-card">
                    <div class="metric-title">Sleep Hours</div>
                    <div class="metric-value sleep {'good' if data['sleep_hours'] > 7 else 'medium' if data['sleep_hours'] > 5 else ''}">{data['sleep_hours']}</div>
                    <div class="metric-desc">
                        {'Well rested' if data['sleep_hours'] > 7 else 'Adequate sleep' if data['sleep_hours'] > 5 else 'Sleep deficit'}
                    </div>
                </div>
                
                <!-- Stress Level Card -->
                <div class="metric-card">
                    <div class="metric-title">Stress Level</div>
                    <div class="metric-value stress {'good' if data['stress_level'] < 30 else 'medium' if data['stress_level'] < 60 else ''}">{data['stress_level']}</div>
                    <div class="metric-desc">
                        {'Low stress' if data['stress_level'] < 30 else 'Moderate stress' if data['stress_level'] < 60 else 'High stress'}
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# This allows the script to be run directly with "python main.py"
# Why: For convenience during development
# At the bottom of your script
if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except OSError:
        # If port 8000 is busy, try port 8001
        print("Port 8000 is in use, trying port 8001...")
        uvicorn.run(app, host="0.0.0.0", port=8001)