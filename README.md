# 📝 StoryCrafter AI  
**Ensemble-Based Long-Form Storytelling Powered by Transfer Learning & GenAI**

StoryCrafter AI is a generative storytelling app that uses *pure model ensembling* and *transfer learning* to craft diverse, vivid, and imaginative 50-line stories. With a sleek dark-themed interface and support for image prompts, tone control, and narration, this project is designed for writers, learners, and creators looking to explore the power of GenAI in storytelling.

---

## ✨ Features

- 🔀 **Pure Ensembling**: Generates parallel stories using GPT-2, GPT-2 Medium, and GPT-Neo 125M — no blending, no voting, just independent imagination.
- 🧠 **Transfer Learning Friendly**: Easily extend the ensemble by adding fine-tuned LLMs for poetic, dramatic, or humorous tones.
- 🖼️ **Image-Driven Inspiration**: Upload an image and let BLIP auto-caption it as part of your story prompt.
- 🎨 **Dark-Themed Streamlit UI**: A stylish, responsive layout with side-by-side story comparisons.
- 🔊 **Text-to-Speech Integration**: Play back your favorite story with built-in audio narration using gTTS.
- 📤 **Editable & Downloadable Output**: Refine stories directly in the app and save original or modified versions.

---

## 🧰 Tech Stack

| Layer           | Tools / Models                                         |
|----------------|--------------------------------------------------------|
| Frontend       | Streamlit (Dark Theme with custom CSS)                |
| Language Models| `gpt2`, `gpt2-medium`, `EleutherAI/gpt-neo-125M`       |
| Image Caption  | `Salesforce/blip-image-captioning-base`               |
| Text-to-Speech | `gTTS` (Google Text-to-Speech)                        |
| Libraries      | `transformers`, `torch`, `pillow`, `accelerate`       |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/storycrafter-ai.git
cd storycrafter-ai
```

2. Install dependencies
   pip install -r requirements.txt

3. Launch the app
   streamlit run app.py

 Folder Structur
 storycrafter-ai/
├── app.py
├── requirements.txt
├── README.md
└── Images

Use Cases
- Creative writing and journaling tools
- Education and storytelling workshops
- Model behavior comparison and GenAI research
- Artistic and narrative experimentation

How It Works

Workflow
The app prompts three independently trained models with the same seed input, generating three complete and uniquely styled stories. Users then compare outputs, edit or download them, and even listen to narrated versions using TTS.




    
