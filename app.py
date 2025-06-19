import streamlit as st
import openai
from io import BytesIO
from PIL import Image
import requests

st.set_page_config(page_title="🎨 AI Image & Video Generator", layout="centered")

def page_image_generator():
    st.title("🎨 OpenAI Image Generator with Upload & Effects")

    # Sidebar controls for this page
    api_key = st.sidebar.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    model = st.sidebar.selectbox(
        "Image Model",
        ["dall-e-3", "dall-e-2"],
        index=0,
        help="Choose DALL·E model version"
    )
    size = st.sidebar.selectbox("Image Size", ["256x256", "512x512", "1024x1024"], index=2)
    num_images = st.sidebar.slider("Number of Images", 1, 4, 1)
    
    st.sidebar.markdown("### Upload Reference Image (optional)")
    uploaded_file = st.sidebar.file_uploader(
        "Upload an image to influence generation",
        type=["png", "jpg", "jpeg"]
    )

    st.sidebar.markdown("### 🎭 Effects & Styles")
    effects_list = [
        "None",
        "Ghibli-style animation frame",
        "Toy camera effect",
        "Watercolor painting",
        "Cyberpunk neon glow",
        "Vintage film photo",
        "Pixar-style 3D render",
        "Hand-drawn sketch",
        "Surreal dreamscape"
    ]
    effect = st.sidebar.selectbox("Select Effect", effects_list)

    templates = {
        "Fantasy Landscape": "A mystical forest at sunset with glowing mushrooms and mist.",
        "Futuristic City": "A cyberpunk cityscape at night, neon lights reflecting off wet pavement.",
        "Cartoon Animal": "A cute cartoon-style fox wearing sunglasses and a hoodie.",
        "Abstract Art": "An abstract painting with vivid colors and chaotic brush strokes.",
        "Photoreal Portrait": "A hyper-realistic portrait of a woman with green eyes and freckles, studio lighting.",
        "Toy Photography": "A whimsical toy train set on a miniature track with warm lighting.",
        "Studio Ghibli Inspired": "A lush green meadow with a small cottage, in the style of Studio Ghibli animation.",
        "Vintage Toy Store": "A cozy vintage toy store filled with colorful wooden toys and soft natural light.",
        "Sci-Fi Space Station": "A futuristic space station orbiting a distant planet with stars and nebulae.",
        "Cute Anime Character": "A cheerful anime girl with pink hair and big sparkling eyes, in a school uniform."
    }

    template_choice = st.selectbox("Choose a Prompt Template", list(templates.keys()))
    base_prompt = templates[template_choice]

    def build_prompt(base, effect_name):
        if effect_name == "None":
            return base
        if effect_name.lower() not in base.lower():
            return base.strip() + f", {effect_name.lower()}"
        return base

    prompt = st.text_area(
        "Edit Your Prompt",
        value=build_prompt(base_prompt, effect),
        height=120,
        help="You can customize or combine prompt templates here"
    )

    def display_uploaded_image(file):
        try:
            img = Image.open(file)
            st.sidebar.image(img, caption="Uploaded Reference Image", use_column_width=True)
            return img
        except Exception:
            st.sidebar.error("Failed to load the uploaded image.")
            return None

    if uploaded_file is not None:
        display_uploaded_image(uploaded_file)

    if st.button("🎨 Generate Image(s)"):
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
        elif not prompt.strip():
            st.error("Please enter a prompt for image generation.")
        else:
            openai.api_key = api_key
            final_prompt = build_prompt(prompt, effect)

            try:
                with st.spinner("Generating image(s)..."):
                    response = openai.images.generate(
                        model=model,
                        prompt=final_prompt,
                        size=size,
                        n=num_images,
                    )
                    urls = [img_data.url for img_data in response.data]

                st.markdown(f"### Generated Image(s) - Effect: **{effect}**")
                for i, url in enumerate(urls, 1):
                    st.image(url, use_column_width=True, caption=f"Image {i}")
                    st.markdown(f"[📥 Download Image {i}]({url})", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("""
    ---
    💡 *Tips:*  
    - Upload an image to influence generation (conceptual).  
    - Try mixing multiple prompt templates with effects for unique art.  
    - Adjust number of images and size for faster generation or higher quality.
    """)

def page_video_generator():
    st.title("🎬 Runway Gen2 Video Generator (Text-to-Video)")

    runway_api_key = st.sidebar.text_input("Runway API Key", type="password", placeholder="Enter your Runway API Key here")
    
    prompt = st.text_area("Enter a description for the video", height=120, placeholder="A calm beach at sunrise, waves gently rolling")
    
    video_length = st.slider("Video Length (seconds)", 2, 10, 4, help="Duration of generated video")
    
    if st.button("▶️ Generate Video"):
        if not runway_api_key:
            st.error("Please enter your Runway API key.")
        elif not prompt.strip():
            st.error("Please enter a video prompt.")
        else:
            headers = {
                "Authorization": f"Bearer {runway_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": prompt,
                "length_seconds": video_length,
                # add other parameters if Runway Gen2 API requires them
            }
            
            try:
                with st.spinner("Generating video... This may take a minute or two."):
                    # Example endpoint - update with actual Runway Gen2 endpoint
                    response = requests.post(
                        "https://api.runwayml.com/v1/gen2/generate",
                        headers=headers,
                        json=payload,
                        timeout=120
                    )
                    response.raise_for_status()
                    data = response.json()

                    video_url = data.get("video_url") or data.get("output") or None
                    if not video_url:
                        st.error("Failed to get video URL from the response.")
                        return

                    st.video(video_url)
                    st.markdown(f"[📥 Download Video]({video_url})", unsafe_allow_html=True)
            except requests.exceptions.RequestException as err:
                st.error(f"API request error: {err}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# --- Multi-page navigation ---
page = st.sidebar.radio("Navigate", ["Image Generator", "Video Generator"])

if page == "Image Generator":
    page_image_generator()
elif page == "Video Generator":
    page_video_generator()

