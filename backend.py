import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI(title="Leftover Alchemy")

# --- DATA MODELS ---
class IngredientRequest(BaseModel):
    ingredients: str
    meal_type: str
    vibe: str

class Recipe(BaseModel):
    title: str
    vibe_description: str
    ingredients: List[str]
    instructions: List[str]

class RecipeResponse(BaseModel):
    recipes: List[Recipe]

# --- 🟢 SAFE ENDPOINT (FOR CRON JOB) ---
# This costs $0 and uses 0 AI quota. It just says "Hello".
@app.get("/")
async def root():
    return {"status": "The Alchemist is awake and ready.", "quota_used": 0}

# --- 🔥 COOKING ENDPOINT (FOR STREAMLIT) ---
@app.post("/generate-recipes", response_model=RecipeResponse)
async def generate_recipes(request: IngredientRequest):
    prompt = (
        f"Role: Master Alchemist Chef. \n"
        f"Context: A user has brought you these raw elements: {request.ingredients}. \n"
        f"Task: Transmute them into 3 distinct recipes for a {request.meal_type}. \n"
        f"Vibe Requirement: The result must embody a '{request.vibe}' energy. \n\n"
        "Instructions: \n"
        "1. For 'vibe_description', write a witty, 2-sentence hook explaining why this dish fits the vibe. \n"
        "2. Ensure the 'title' is creative. \n"
        "3. Provide clear ingredients and instructions. \n"
        "Return ONLY structured JSON."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": RecipeResponse,
            }
        )
        return response.parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
