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
    vibe_description: str  # The "Hook"
    ingredients: List[str]
    instructions: List[str]

class RecipeResponse(BaseModel):
    recipes: List[Recipe]

# --- SAFE ENDPOINT FOR CRON JOB (DOES NOT USE AI) ---
@app.get("/")
async def root():
    # This is just a ping. It costs $0 and uses 0 quota.
    return {"status": "The Alchemist is awake and ready."}

# --- COOKING ENDPOINT (USES AI) ---
@app.post("/generate-recipes", response_model=RecipeResponse)
async def generate_recipes(request: IngredientRequest):
    # The "Golden Prompt" logic
    prompt = (
        f"Role: Master Alchemist Chef and Culinary Psychologist who is the whisperer of ideas to food influencers. \n"
        f"Context: A user has brought you these raw elements and is struggling with what to come up with and wants to come up with something that will be instagram worthy and potentially viral: {request.ingredients}. \n"
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
