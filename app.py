import streamlit as st
import openai

st.set_page_config(page_title="Image Generator with OpenAI", layout="centered")

st.title("🎨 OpenAI Image Generator")

# --- Sidebar ---
st.sidebar.title("🔐 Settings")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
model = st.sidebar.selectbox("Model", ["dall-e-3", "dall-e-2"], index=0)

# --- Prompt Templates ---
templates = {
    "Fantasy Landscape": "A mystical forest at sunset with glowing mushrooms and mist.",
    "Futuristic City": "A cyberpunk cityscape at night, neon lights reflecting off wet pavement.",
    "Cartoon Animal": "A cute cartoon-style fox wearing sunglasses and a hoodie.",
    "Abstract Art": "An abstract painting with vivid colors and chaotic brush strokes.",
    "Photoreal Portrait": "A hyper-realistic portrait of a woman with green eyes and freckles, studio lighting."
}

template_choice = st.selectbox("Choose a Prompt Template", list(templates.keys()))
prompt = st.text_area("Edit Your Prompt", templates[template_choice], height=100)

if st.button("🎨 Generate Image"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    else:
        openai.api_key = api_key
        try:
            with st.spinner("Generating image..."):
                response = openai.images.generate(
                    model=model,
                    prompt=prompt,
                    size="1024x1024",
                    quality="hd" if model == "dall-e-3" else "standard",
                    n=1
                )
                image_url = response.data[0].url
                st.image(image_url, caption="Generated Image", use_column_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
