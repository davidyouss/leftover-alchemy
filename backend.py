import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# Remove the 'api_version' pinning to allow the modern v1beta features
client = genai.Client(api_key=api_key)

app = FastAPI(title="Leftover Alchemy: Stabilized Edition")

class IngredientRequest(BaseModel):
    ingredients: str
    meal_type: str
    vibe: str

class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    instructions: List[str]
    image_keyword: str

class RecipeResponse(BaseModel):
    recipes: List[Recipe]

@app.post("/generate-recipes", response_model=RecipeResponse)
async def generate_recipes(request: IngredientRequest):
    prompt = (
        f"Role: Master Chef. Task: Create 3 recipes using {request.ingredients}. "
        f"Meal Type: {request.meal_type}. Vibe: {request.vibe}. "
        "Return JSON with 'title', 'ingredients' (list), 'instructions' (list), and 'image_keyword'."
    )

    try:
        # We use the 2.0-flash model which is the 2026 stable standard
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
        print(f"🔥 ALCHEMIST ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
