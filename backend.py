import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from typing import List

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI(title="Leftover Alchemy: Modern Logic Edition")

# --- DATA MODELS ---
class IngredientRequest(BaseModel):
    ingredients: str
    meal_type: str
    vibe: str #added back  

# This matches the dropdown we're adding to the frontend

class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    instructions: List[str]
    image_keyword: str

class RecipeResponse(BaseModel):
    recipes: List[Recipe]

# --- API ENDPOINT ---
@app.post("/generate-recipes", response_model=RecipeResponse)
async def generate_recipes(request: IngredientRequest):
    # We update the prompt to include the meal_type constraint
    prompt = (
    f"You are a master chef. Create 3 creative recipes using: {request.ingredients}. "
    f"The recipes MUST be for {request.meal_type} and match a '{request.vibe}' vibe. "
    "Return the response in a structured JSON format..."
)	    

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': RecipeResponse,
            }
        )
        return response.parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



