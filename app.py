import streamlit as st
import requests

# --- CONFIGURATION ---
# Replace this with your actual Render URL
API_URL = "https://leftover-backend-3gdf.onrender.com/generate-recipes"

st.set_page_config(page_title="Leftover Alchemy", page_icon="🍳")

st.title("🍳 Leftover Alchemy")
st.caption("The best meal is the one you don't have to go to the store for.")

# Patience Header
st.warning("⚡ **Note:** If the app has been resting, the 'Chef' takes about 60 seconds to wake up for the first request. Thanks for your patience!")

# --- INPUT SECTION ---
ingredients_input = st.text_input("What's in your fridge?", placeholder="e.g. eggs, spinach, leftover rice")

col1, col2 = st.columns(2)

with col1:
    meal_choice = st.selectbox(
        "What are we making?",
        ["Breakfast", "Lunch", "Dinner", "Snack", "Surprise Me"]
    )

with col2:
    vibe_choice = st.selectbox(
        "What's the vibe?",
        ["Lazy & Simple", "Fancy Date Night", "Healthy & Clean", "High Protein", "Michelin Chef", "Cheat Meal", "Hangover Cure", "Surprise Me"]
    )

# --- EXECUTION ---
if st.button("Generate Recipe"):
    if ingredients_input:
        # Your custom spinner message
        with st.spinner("Performing a little alchemy with what you've got... 🪄"):
            payload = {
                "ingredients": ingredients_input,
                "meal_type": meal_choice,
                "vibe": vibe_choice
            }
            
            try:
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    recipes = data.get("recipes", [])
                    
                    for r in recipes:
                        st.divider()
                        st.subheader(r['title'])
        
                        # Display the new "vibe" description here
                        st.info(f"✨ {r['vibe_description']}") 
        
                        # ... rest of your display logic

                        
                        st.write("**Ingredients:**")
                        st.write(", ".join(r['ingredients']))
                        
                        st.write("**Instructions:**")
                        for step in r['instructions']:
                            st.write(f"- {step}")
                else:
                    st.error(f"The Alchemist is struggling (Error {response.status_code}). Check your Backend logs!")
            
            except Exception as e:
                st.error(f"Connection Error: {e}")
    else:
        st.info("Please enter some ingredients first!")

