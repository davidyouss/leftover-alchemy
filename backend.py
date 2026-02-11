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
if not api_key:
    print("⚠️ WARNING: GOOGLE_API_KEY not found in environment variables.")

# The new Client object is the entry point for all Gemini API calls
client = genai.Client(api_key=api_key)

app = FastAPI(title="Leftover Alchemy: Modern Edition")

# --- DATA MODELS ---
# This ensures FastAPI knows exactly what to expect from your Streamlit frontend
class IngredientRequest(BaseModel):
    ingredients: str
    meal_type: str
    vibe: str

# These models define the structured JSON the AI MUST return
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
    # We explicitly tell the AI to use the meal_type and vibe
    prompt = (
        f"You are a master chef. Create 3 creative recipes using: {request.ingredients}. "
        f"The recipes MUST be appropriate for a {request.meal_type} and match a '{request.vibe}' vibe. "
        "Return the response in structured JSON with 'title', 'ingredients', "
        "'instructions', and a 1-word 'image_keyword' for a food photo search."
    )

    try:
        # Use the standard stable model ID for reliability
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RecipeResponse, # Forces valid JSON output
            )
        )
        return response.parsed # Directly returns the validated Pydantic object
    
    except Exception as e:
        # This will show up in your Render logs if things go wrong
        print(f"🔥 ALCHEMIST ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Alchemist Backend is bubbling away!"}
