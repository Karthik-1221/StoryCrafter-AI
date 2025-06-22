import streamlit as st
from PIL import Image
from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
from gtts import gTTS
import uuid, os


# -------------------------
# Load Models
# -------------------------
@st.cache_resource
def load_generators():
    return {
        "GPT-2": pipeline("text-generation", model="gpt2"),
        "GPT-2 Medium": pipeline("text-generation", model="gpt2-medium"),
        "GPT-Neo 125M": pipeline("text-generation", model="EleutherAI/gpt-neo-125M")
    }


@st.cache_resource
def load_caption_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model


# -------------------------
# Core Functions
# -------------------------
def get_image_caption(image):
    processor, model = load_caption_model()
    image = image.convert("RGB")
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)


def generate_long_story(generator, prompt):
    output = generator(
        prompt,
        max_length=1024,
        do_sample=True,
        temperature=0.9,
        top_k=50,
        top_p=0.95,
        pad_token_id=50256  # GPT-2's padding token
    )
    return output[0]['generated_text']


def narrate_text_gtts(text):
    tts = gTTS(text)
    filename = f"temp_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return filename


# -------------------------
# Streamlit Interface
# -------------------------
st.set_page_config(page_title="StoryCrafter AI", layout="wide")

st.markdown("""
    <style>
    body, .block-container {
        background-color: #121212;
        color: #e0e0e0;
    }
    h1, h2, h3, .stTextInput label, .stSelectbox label, .stFileUploader label {
        color: #fafafa !important;
    }
    .story-box {
        background-color: #1e1e1e;
        padding: 1.2rem;
        margin-top: 1rem;
        border-left: 5px solid #5e60ce;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        height: 600px;
        overflow-y: auto;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #ffffff;
    }
    .stButton>button, .stDownloadButton>button {
        background-color: #5e60ce;
        color: white;
        border-radius: 5px;
        padding: 0.6rem 1rem;
        border: none;
    }
    .stTextArea textarea {
        background-color: #1c1c1c !important;
        color: #e0e0e0 !important;
    }
    .stRadio > div {
        flex-direction: row;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>📝 StoryCrafter AI</h1>", unsafe_allow_html=True)
st.caption(
    "✨ Generate a 50-line creative story from three independent AI models. Upload an image or describe your idea!")

uploaded_image = st.file_uploader("📷 Upload an image (optional)", type=["jpg", "png"])
user_input = st.text_area("💡 Enter your story idea (a sentence or paragraph)", height=100)
tone = st.selectbox("🎭 Choose a tone", ["dramatic", "humorous", "poetic"])

if "stories" not in st.session_state:
    st.session_state.stories = []

if st.button("🧠 Generate Stories"):
    if user_input.strip() or uploaded_image:
        full_prompt = user_input
        if uploaded_image:
            image = Image.open(uploaded_image)
            caption = get_image_caption(image)
            st.image(image, caption=f"🖼 Caption: {caption}")
            full_prompt = f"{caption}. {user_input}"

        tone_style = {
            "dramatic": "Write a long dramatic story about: ",
            "humorous": "Write a long funny story about: ",
            "poetic": "Write a long poetic narrative based on: "
        }
        final_prompt = tone_style.get(tone, "") + full_prompt

        generators = load_generators()
        st.session_state.stories = [
            (model_name, generate_long_story(gen, final_prompt))
            for model_name, gen in generators.items()
        ]
    else:
        st.warning("Please enter a story idea or upload an image to begin!")

# Display Results
if st.session_state.stories:
    st.markdown("### 🧾 Generated Stories from Ensemble Models")
    cols = st.columns(len(st.session_state.stories))

    for i, (model_name, story) in enumerate(st.session_state.stories):
        with cols[i]:
            st.markdown(f"#### ✨ {model_name}")
            st.markdown(f"<div class='story-box'>{story}</div>", unsafe_allow_html=True)
            st.markdown(f"📏 **Line Count:** {story.count('. ')}")

    selected_idx = st.radio("🏆 Select your favorite story to refine:",
                            options=list(range(len(st.session_state.stories))),
                            format_func=lambda i: st.session_state.stories[i][0])

    selected_story = st.session_state.stories[selected_idx][1]
    st.markdown("### 🔍 Selected Story")
    st.markdown(selected_story)

    if st.button("🔊 Read Aloud"):
        audio_file = narrate_text_gtts(selected_story)
        st.audio(open(audio_file, "rb").read(), format="audio/mp3")
        os.remove(audio_file)

    edited = st.text_area("✏️ Edit your story below (optional)", value=selected_story, height=250)
    st.download_button("📥 Download Original", data=selected_story, file_name="ensemble_story.txt", mime="text/plain")
    st.download_button("📤 Download Edited", data=edited, file_name="edited_story.txt", mime="text/plain")