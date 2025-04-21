from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Union
import pandas as pd
import joblib
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure allowed origins
origins = ["https://findyourcarprice.streamlit.app", "http://localhost:8501/"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # or use ["*"] to allow all origins (not recommended for prod)
    allow_credentials=True,
    allow_methods=["GET", "POST"],     
    allow_headers=["*"],              # allows all request headers
)


# Load environment variables from .env
load_dotenv()

# --- 🔐 API Key Auth Setup ---
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

# --- 🚀 FastAPI App ---
app = FastAPI(title="Car Price Prediction & CSV API")

# --- 🔍 Load Model ---
model = joblib.load("gb_pipeline.pkl")

# --- 📦 Input Schema ---
class InputData(BaseModel):
    horsePower: float
    mileage: float
    mpgCity: float
    mpgHighway: float
    evRange: float
    evMpgeCity: float
    evMpgeHighway: float
    seats: int
    numOfOwners: int
    age: int
    bodyType: str
    fuelType: str
    driveTrain: str
    transmission: str
    hasReportedAccident: bool
    make: str
    model: str

# --- 🌐 Routes ---

@app.get("/")
def index():
    return {"message": "CSV & Prediction API is running 🚀"}


@app.get("/get-data")
def get_data(_: str = Depends(verify_api_key)):
    df = pd.read_csv("cleaned_data.csv")
    return JSONResponse(content=df.to_dict(orient="records"))


@app.get("/get-filtered-data")
def get_filtered_data(_: str = Depends(verify_api_key)):
    df = pd.read_csv("filter_data.csv")
    return JSONResponse(content=df.to_dict(orient="records"))


@app.post("/predict")
def predict(
    input_data: Union[InputData, List[InputData]],
    _: str = Depends(verify_api_key)
):
    input_dict = [input_data.dict()] if isinstance(input_data, InputData) else [i.dict() for i in input_data]
    input_df = pd.DataFrame(input_dict)
    prediction = model.predict(input_df)

    return {
        "predicted_price": float(prediction[0]) if len(prediction) == 1 else prediction.tolist()
    }
