import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
# We use the new client syntax here
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("⚠️ WARNING: GOOGLE_API_KEY not found in environment variables.")

client = genai.Client(api_key=api_key)

app = FastAPI(title="Leftover Alchemy: Modern Logic Edition")

# --- DATA MODELS ---

# We define the strict schema for the output
class RecipeConcept(BaseModel):
    title: str = Field(..., description="The name of the dish")
    description: str = Field(..., description="A short, exciting summary")
    intrigue_score: int = Field(..., description="0-100 score of novelty")
    psychological_hook: str = Field(..., description="Why this solves food boredom")
    steps: list[str] = Field(..., description="3-4 punchy instruction steps")

class RecipeResponse(BaseModel):
    recipes: list[RecipeConcept]

class IngredientInput(BaseModel):
    ingredients: list[str]
    pantry_staples: bool = True
    vibe: str = "experimental" 

# --- THE ENDPOINT ---

@app.post("/generate-recipes")
async def generate_recipes(data: IngredientInput):
    ingredients_str = ", ".join(data.ingredients)
    
    prompt = (
        f"You are a Culinary Psychologist. The user is stuck in a food rut. "
        f"Ingredients available: {ingredients_str}. "
        f"Desired Vibe: {data.vibe}. "
        "Generate 3 recipe concepts. They should be creative but edible. "
        "For 'intrigue_score', rate from 0-100 based on how novel the combination is."
    )

    try:
        # NEW SDK SYNTAX
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=RecipeResponse
            )
        )
        
        # The new SDK parses it into the Pydantic object automatically
        if response.parsed:
            return response.parsed
        else:
            raise ValueError("Failed to parse structured response")

    except Exception as e:
        print(f"Error: {e}") 
        raise HTTPException(status_code=500, detail=str(e))
