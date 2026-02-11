import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types # Added for safety settings
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
    # Print what the backend received to verify the connection
    print(f"DEBUG: Received request for {request.meal_type} with {request.ingredients}")

    prompt = (
        f"Role: Master Chef. Create 3 recipes.\n"
        f"Ingredients: {request.ingredients}\n"
        f"Meal Type: {request.meal_type}\n"
        f"Vibe: {request.vibe}\n"
        "Return JSON with title, ingredients, instructions, and image_keyword."
    )

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=RecipeResponse,
                # This helps prevent the AI from 'choking' on weird ingredient names
                safety_settings=[
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                ]
            )
        )
        return response.parsed
    except Exception as e:
        # THIS IS THE MOST IMPORTANT LINE: Check Render logs for this!
        print(f"🔥 CRITICAL ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
