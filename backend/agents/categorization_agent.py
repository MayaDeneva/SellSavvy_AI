from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import pickle
from fastapi import APIRouter, Form
import os
from pydantic import BaseModel

router = APIRouter()
#  Define Request Schema
class PredictionRequest(BaseModel):
    title: str
# Define paths
#  Get absolute path to the backend folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Moves up from `backend/agents`
#  Define model paths relative to backend root
MODEL_DIR = os.path.join(BASE_DIR, "../models", "bert_product_classifier")
model_path = MODEL_DIR
label_encoder_path = os.path.join(MODEL_DIR, "label_encoder.pkl")

# Load trained model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)


# Load label encoder with explicit binary mode
try:
    with open(label_encoder_path, "rb") as f:
        label_encoder = pickle.load(f)
    print("Label encoder loaded successfully!")
except Exception as e:
    print(f"❌ Error loading label_encoder: {e}")


# Function to predict category
@router.post("/predict")
async def predict_category(request: PredictionRequest):
    """Predicts the product category using BERT"""
    inputs = tokenizer(request.title, return_tensors="pt", padding="max_length", truncation=True, max_length=128)
    outputs = model(**inputs)
    predicted_label = torch.argmax(outputs.logits, dim=1).item()
    category = label_encoder.inverse_transform([predicted_label])[0]
    return {"category": category}  #  Ensure response is a proper JSON object

# # Example Prediction
# product_title = "Protein Powder"
# predicted_category = predict_category(product_title)
# print(f"Predicted Category: {predicted_category}")
