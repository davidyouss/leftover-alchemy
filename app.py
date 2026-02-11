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
st.caption("Turning fridge sadness into belly happiness.")

# --- INPUTS ---
with st.form("alchemy_form"):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ingredients = st.text_input(
            "What's in the fridge?", 
            placeholder="e.g., 2 eggs, stale bread, cheese"
        )
        
    with col2:
        # The "Pre-populated" choices
        vibe_options = [
            "Lazy & Quick", 
            "Healthy & Clean", 
            "Michelin Chef", 
            "Hangover Cure", 
            "High Protein", 
            "✨ Custom Vibe..."  # The "Escape Hatch"
        ]
        
        # User picks from the list
        selected_vibe = st.selectbox("Vibe Check", vibe_options)
        
        # Logic: If they picked 'Custom', show a text box. 
        # Otherwise, use what they picked.
        if selected_vibe == "✨ Custom Vibe...":
            custom_vibe = st.text_input("Describe your vibe", placeholder="e.g. 1950s Diner")
            final_vibe = custom_vibe
        else:
            final_vibe = selected_vibe

    # The button now submits the 'final_vibe'
    submitted = st.form_submit_button("Generate Concepts")

# --- LOGIC ---
if submitted and ingredients:
    # Use 'final_vibe' instead of 'vibe' in your payload
    payload = {
        "ingredients": ingredients, 
        "meal_type": "Dinner",  # You can hardcode this or keep the selectbox
        "vibe": final_vibe      # <--- IMPORTANT CHANGE
    } 
            # --- THE MICHELIN STAR UI ---
            if "recipes" in data:
                for r in data["recipes"]:
                    # The Expander creates the dropdown card effect
                    with st.expander(f"🏆 {r['title']}", expanded=True):
                        
                        # The Blue Box for "The Hook"
                        st.info(f"🧠 **The Hook:** {r.get('vibe_description', 'A perfect match.')}")
                        
                        st.markdown("### 🔪 The Steps:")
                        for step in r['instructions']:
                            st.write(f"* {step}")
                            
                        st.divider()
                        st.caption(f"**Ingredients:** {', '.join(r['ingredients'])}")
            else:
                st.error("The Alchemist returned empty-handed.")
                
        except Exception as e:
            st.error(f"Connection failed: {e}")
