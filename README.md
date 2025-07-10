# 🤖 WonderBot - AI Learning Adventure for Kids

WonderBot is an AI-powered educational platform that generates kid-friendly explanations, diagrams, and audio for any topic or image. Built with CrewAI, OpenAI, and FastAPI, WonderBot is designed for curious kids, parents, and teachers who want safe, engaging, and multimodal learning experiences.

---

## ✨ Features

- **🤖 Multi-Agent AI Pipeline**: CrewAI agents for research, safety validation, analogy generation, and presentation
- **📚 Kid-Friendly Explanations**: Age-appropriate, engaging content tailored to children
- **🎨 Visual Diagrams**: DALL-E generated illustrations to enhance learning
- **🔊 Audio Narration**: Text-to-speech audio versions for accessibility
- **🖼️ Image Analysis**: Upload an image and get a fun, educational explanation
- **🛡️ Built-in Guardrails**: Content safety checks for violence, hate, adult, and inappropriate material
- **🌈 Beautiful Web Interface**: Modern, responsive, and colorful frontend
- **🎯 Personalized Learning**: Customize by age and interests

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
https://github.com/your-username/wonderbot.git
cd wonderbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Start the Server

```bash
uvicorn src.kidapp.api:app --host 0.0.0.0 --port 8000
```

### 4. Access the Frontend

Open your browser and go to: **http://localhost:8000**

---

## 🌐 Deployment

See [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) for full instructions.

- **Railway** (Recommended, Free): Deploy from GitHub, set `OPENAI_API_KEY`, and share your public URL.
- **Render**: Free tier, similar process.
- **Heroku**: Paid, but reliable.
- **ngrok**: For quick local sharing.

---

## 📚 How to Use

### Web Interface
1. **Visit the frontend**: Go to your deployed URL or `http://localhost:8000`
2. **Enter a topic**: Ask any educational question (e.g., "Why do birds sing?")
3. **Or upload an image**: Get a fun, kid-friendly explanation of what's in the picture
4. **Customize** (optional): Add age and interests for personalized content
5. **Generate**: Click the button and wait for the AI to create your explanation
6. **Enjoy**: Read the explanation, view the diagram, and listen to the audio!

### API Endpoint
See [`API_DOCUMENTATION.md`](API_DOCUMENTATION.md) for full details.

**Example:**
```bash
curl -X POST "https://your-app-name.railway.app/generate" \
  -F "topic=Why do birds sing?" \
  -F "age=7" \
  -F "interests=nature,music"
```

---

## 🏗️ Architecture

### CrewAI Agents
1. **Educational Content Researcher**: Gathers accurate, age-appropriate information
2. **Content Safety Validator**: Ensures content is safe and appropriate for children
3. **Kid-Friendly Analogy Generator**: Creates memorable analogies and stories
4. **Final Response Presenter**: Combines everything into a cohesive explanation
5. **Guardrails Agent**: Built-in safety checks for violence, hate, adult, and inappropriate content

### Multimodal Output
- **Text**: Comprehensive, kid-friendly explanation
- **Image**: DALL-E generated educational diagram (with error handling)
- **Audio**: OpenAI TTS narration of the explanation

---

## 🛡️ Safety & Guardrails

WonderBot uses CrewAI's built-in guardrails and a dedicated Guardrails Agent to:
- Block or sanitize any content that is violent, hateful, adult, or otherwise inappropriate for children
- Scan all generated text, image prompts, and analogies
- Provide safe alternatives or friendly error messages if content is blocked
- Handle DALL-E errors gracefully with user-friendly feedback

---

## 📁 Project Structure

```
wonderbot/
├── src/kidapp/
│   ├── api.py              # FastAPI server with endpoints
│   ├── crew.py             # CrewAI pipeline configuration
│   ├── agents/             # Individual AI agents (including guardrails)
│   ├── tasks/              # Agent tasks and workflows
│   ├── static/             # Frontend assets (index.html)
│   └── config/             # Configuration files (YAML)
├── uploaded_images/        # Generated diagrams and audio
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version
├── Procfile                # Deployment config (Heroku)
├── DEPLOYMENT_GUIDE.md     # Deployment instructions
├── API_DOCUMENTATION.md    # API usage and examples
└── README.md               # This file
```

---

## 🎨 Example Topics

Try these fun questions:
- "Why do birds sing?"
- "How do plants grow?"
- "What makes rainbows?"
- "Why do we dream?"
- "How do airplanes fly?"
- "What causes thunder?"
- "How do bees make honey?"
- Or upload a photo of an animal, plant, or object!

---

## 🔧 Development & Customization

- **Add new agents**: Place in `src/kidapp/agents/`
- **Add new tasks**: Place in `src/kidapp/tasks/`
- **Edit frontend**: Modify `src/kidapp/static/index.html`
- **Change config**: Edit YAML files in `src/kidapp/config/`

### Testing
- Use the `/docs` endpoint for interactive API testing
- Use `curl` or Postman for API requests

---

## 🛠️ Troubleshooting

- **Build Fails**: Check `requirements.txt` and Python version
- **API Key Error**: Ensure `OPENAI_API_KEY` is set and valid
- **Import Errors**: Check file paths and GitHub commits
- **DALL-E/Image Errors**: User-friendly messages are shown in the UI
- **Quota Exceeded**: Check your OpenAI usage and billing

---

## 📞 Support

- Check the deployment logs for errors
- Review the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) and [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- For further help, open an issue or contact the maintainer

---

## 🎉 Success!

Once deployed, WonderBot is accessible to anyone with the URL!

- ✅ Kid-friendly AI explanations
- ✅ DALL-E generated diagrams
- ✅ Text-to-speech audio
- ✅ Image analysis
- ✅ Built-in guardrails for safety
- ✅ Beautiful, responsive web interface

---

**WonderBot: Making learning magical, safe, and fun for every child!**
