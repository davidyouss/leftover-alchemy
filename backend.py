import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from typing import List

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI()

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
        f"Role: Master Chef. Task: Create 3 recipes.\n"
        f"Ingredients available: {request.ingredients}\n"
        f"Meal Type: {request.meal_type}\n"
        f"Vibe/Style: {request.vibe}\n"
        f"Format: Return JSON with title, ingredients (list), instructions (list), and a 1-word image_keyword."
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
        # This will print the REAL error to your Render logs
        print(f"ALCHEMIST ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))
