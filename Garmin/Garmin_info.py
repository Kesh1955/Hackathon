from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
import uvicorn


# Define request model
class RecoveryScoreRequest(BaseModel):
    recovery_score: float = Field(..., description="Recovery score from Garmin watch (0-72 hours)")

# Define response model
class TrainingResponse(BaseModel):
    training_status: str
    recovery_hours: float
    message: str


# Initialize FastAPI app
app = FastAPI(
    title="Recovery Score API",
    description="API that determines training status based on Garmin watch recovery score data",
    version="1.0.0"
)


@app.post("/training-status", response_model=TrainingResponse)
async def get_training_status(request: RecoveryScoreRequest):
    """
    Determines whether training should continue or be cancelled based on the recovery score.
    
    - If recovery score > 20 hours: Training is cancelled
    - If recovery score <= 20 hours: Training continues
    """
    # Validate input range
    if request.recovery_score < 0 or request.recovery_score > 72:
        raise HTTPException(status_code=400, detail="Recovery score must be between 0 and 72 hours")
    
    # Determine training status
    if request.recovery_score > 20:
        training_status = "cancelled"
        message = "No training tomorrow, all training will be cancelled."
    else:
        training_status = "continue"
        message = "Training will continue as scheduled."
    
    return TrainingResponse(
        training_status=training_status,
        recovery_hours=request.recovery_score,
        message=message
    )

# Add GET endpoint for easier testing through browsers
@app.get("/training-status", response_model=TrainingResponse)
async def get_training_status_get(recovery_score: float = Query(..., description="Recovery score from Garmin watch (0-72 hours)")):
    """
    GET endpoint version for determining training status based on recovery score.
    
    - If recovery score > 20 hours: Training is cancelled
    - If recovery score <= 20 hours: Training continues
    """
    # Reuse the same logic from the POST endpoint
    request = RecoveryScoreRequest(recovery_score=recovery_score)
    return await get_training_status(request)

@app.get("/")
async def root():
    """Root endpoint that provides information about the API."""
    return {
        "api": "Recovery Score API",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "This information page"},
            {"path": "/training-status", "method": "POST", "description": "Get training status based on recovery score (POST)"},
            {"path": "/training-status", "method": "GET", "description": "Get training status based on recovery score (GET)"}
        ],
        "usage": "Send a POST request to /training-status with a JSON body containing 'recovery_score' or a GET request to /training-status?recovery_score=value"
    }


# Run the application if executed directly
if __name__ == "__main__":
    uvicorn.run("Garmin_info:app", host="0.0.0.0", port=8000, reload=True)