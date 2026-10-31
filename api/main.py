from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


from src.inference import predict_category


app = FastAPI(
    title="News Classification API",
    description="Classifies news articles into four categories",
    version="1.0.0"
)

class NewsRequest(BaseModel):
    text: str = Field(min_length=1)



@app.post("/predict")
def predict(request: NewsRequest):
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Article text cannot be empty"
        )
    prediction = predict_category(request.text)

    return {
        "category": prediction
    }