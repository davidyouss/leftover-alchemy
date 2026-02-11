import streamlit as st
import requests

# --- CONFIG ---
st.set_page_config(page_title="Leftover Alchemy", page_icon="🍳")
BACKEND_URL = "https://leftover-backend-3gdf.onrender.com/generate-recipes" 

# --- STYLING ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🍳 Leftover Alchemy")
st.caption("Turning fridge sadness into belly happiness. 😋")

# --- INPUTS ---
with st.form("alchemy_form"):
    col1, col2 = st.columns([2, 1])
    with col1:
        ingredients = st.text_input("What's in the fridge?", placeholder="e.g., 2 eggs, stale bread, cheese")
    with col2:
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
        
        # Free-Text Vibe Input
        vibe_input = st.text_input(
            "Current Vibe", 
            placeholder="e.g., Michelin Star, Hangover Cure..."
        )
    
    submitted = st.form_submit_button("Generate Concepts")

# --- LOGIC ---
if submitted and ingredients:
    # Logic to handle empty vibe
    if vibe_input:
        vibe = vibe_input
    else:
        vibe = "General Creative Cooking"

    with st.spinner("Transmuting elements..."):
        try:
            payload = {"ingredients": ingredients, "meal_type": meal_type, "vibe": vibe}
            
            response = requests.post(BACKEND_URL, json=payload)
            response.raise_for_status() # This triggers the HTTPError block below if it fails
            data = response.json()
            
            # --- THE MICHELIN STAR UI ---
            if "recipes" in data:
                for r in data["recipes"]:
                    with st.expander(f"🏆 {r['title']}", expanded=True):
                        st.info(f"🧠 **The Hook:** {r.get('vibe_description', 'A perfect match.')}")
                        
                        st.markdown("### 🔪 The Steps:")
                        for step in r['instructions']:
                            st.write(f"* {step}")
                            
                        st.divider()
                        st.caption(f"**Ingredients:** {', '.join(r['ingredients'])}")
            else:
                st.error("The Alchemist returned empty-handed.")

        # --- ERROR HANDLING ---
        except requests.exceptions.HTTPError as http_err:
            # This captures the 500 error text from the backend
            st.error(f"🔥 Backend Crash: {response.text}")
        except Exception as e:
            st.error(f"Connection failed: {e}")
