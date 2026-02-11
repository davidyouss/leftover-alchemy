import streamlit as st
import requests

# 1. Config
API_URL = "https://leftover-backend-3gdf.onrender.com/generate-recipes"

st.set_page_config(page_title="The Rut Buster", page_icon="🍳")

# 2. The UI Layout
st.title("🍳 Leftover Alchemy")
st.caption("Turn random ingredients into culinary experiments that actually work.")


# --- NEW PATIENCE HEADER ---
st.warning("⚡ **Patience is an Ingredient: Good things take time! If the results don't appear instantly, our AI is just warming up. It'll be worth the wait, I promise.")
# ---------------------------

col1, col2 = st.columns(2)
# ... the rest of your code ...
# Input Section
col1, col2 = st.columns(2)
with col1:
    ingredients = st.text_input("What's in the fridge?", "canned tuna, hot sauce, rice")
with col2:
    meal_choice = st.selectbox("What are we making?", ["Breakfast", "Lunch", "Dinner", "Snack"])
vibe_choice = st.text_input("What's the vibe?", placeholder="e.g. Cozy, Fancy, Lazy, High-Protein")
# 3. The Logic
if st.button("Generate Concepts", type="primary"):
    with st.spinner("Performing a little alchemy with what you've got..."):
        try:
            # Send data to your backend
		payload = {
    "ingredients": ingredients_input,
    "meal_type": meal_choice,
    "vibe": vibe_choice
}
            
payload = {
    "ingredients": ingredients_input,
    "meal_type": meal_choice,
    "vibe": vibe_choice
}
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
            }
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
            }
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                recipes = data.get("recipes", [])
                
                # Display Results
                for r in recipes:
                    with st.expander(f"🏆 {r['title']} (Intrigue: {r['intrigue_score']}/100)", expanded=True):
                        st.markdown(f"_{r['description']}_")
                        st.info(f"**🧠 The Hook:** {r['psychological_hook']}")
                        
                        st.write("### 🔪 The Steps:")
                        for step in r['steps']:
                            st.write(f"- {step}")
            else:
                st.error(f"Kitchen Error: {response.text}")
                
        except Exception as e:
            st.error(f"Connection failed. Is the backend running? ({e})")
