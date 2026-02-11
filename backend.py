import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# Force the client to use the stable version to avoid v1beta snags
client = genai.Client(
    api_key=api_key,
    http_options={'api_version': 'v1'}
)

app = FastAPI(title="Leftover Alchemy: Gemini 3 Edition")

# --- DATA MODELS ---
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

# --- API ENDPOINT ---
@app.post("/generate-recipes", response_model=RecipeResponse)
async def generate_recipes(request: IngredientRequest):
    prompt = (
        f"You are a master chef. Create 3 creative recipes using: {request.ingredients}. "
        f"The recipes MUST be for {request.meal_type} with a '{request.vibe}' vibe. "
        "Return the response in structured JSON with 'title', 'ingredients', "
        "'instructions', and a 1-word 'image_keyword'."
    )

    try:
        # Switching to the officially supported Gemini 3 Flash model
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RecipeResponse,
            )
        )
        return response.parsed
    
    except Exception as e:
        print(f"🔥 ALCHEMIST ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "The Alchemist is online and using Gemini 3 Flash!"}
