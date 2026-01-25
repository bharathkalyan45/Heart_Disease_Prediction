from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pickle
import pandas as pd

app = FastAPI()

# Mount static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load trained model
with open("heart_disease.pkl", "rb") as f:
    model = pickle.load(f)

# Mappings
CHEST_PAIN_MAP = {
    "typical anginal": 1,
    "atypical anginal": 2,
    "non-anginal pain": 3,
    "asymptomatic": 4
}

EXERCISE_ANGINA_MAP = {"no": 0, "yes": 1}
ST_SLOPE_MAP = {"upward": 1, "flat": 2, "downward": 3}

# Feature columns in correct order
FEATURES = [
    "age",
    "chest pain type",
    "resting bp s",
    "cholesterol",
    "max heart rate",
    "exercise angina",
    "oldpeak",
    "ST slope"
]


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/predict")
def predict_page(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})


@app.post("/predict")
async def predict(
    request: Request,
    age: int = Form(...),
    restingBps: int = Form(...),
    cholesterol: int = Form(...),
    maxHeartRate: int = Form(...),
    chestPainType: str = Form(...),
    exerciseAngina: str = Form(...),
    oldpeak: float = Form(...),
    stSlope: str = Form(...)
):
    # Prepare input as DataFrame with correct column names
    input_df = pd.DataFrame([[
        age,
        CHEST_PAIN_MAP[chestPainType],
        restingBps,
        cholesterol,
        maxHeartRate,
        EXERCISE_ANGINA_MAP[exerciseAngina],
        oldpeak,
        ST_SLOPE_MAP[stSlope]
    ]], columns=FEATURES)

    prediction = model.predict(input_df)[0]
    confidence = model.predict_proba(input_df)[0][1]

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "prediction": int(prediction),
            "confidence": round(confidence * 100, 2)
        }
    )
