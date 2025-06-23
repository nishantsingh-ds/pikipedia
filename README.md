# 🎓 KidApp - Educational AI for Kids

KidApp is an AI-powered educational platform that uses CrewAI agents to generate kid-friendly, multimodal explanations for any topic. Perfect for curious minds aged 6-12!

## ✨ Features

- **🤖 Multi-Agent AI Pipeline**: Uses CrewAI with specialized agents for research, safety validation, analogy generation, and presentation
- **📚 Kid-Friendly Explanations**: Age-appropriate, engaging content tailored to children
- **🎨 Visual Diagrams**: DALL-E generated illustrations to enhance learning
- **🔊 Audio Narration**: Text-to-speech audio versions for accessibility
- **🌐 Beautiful Web Interface**: Modern, responsive frontend for easy testing
- **🎯 Personalized Learning**: Customize by age and interests

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd kidapp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Configure API Keys

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Start the Server

```bash
python -m uvicorn src.kidapp.api:app --host 0.0.0.0 --port 8000
```

### 4. Access the Frontend

Open your browser and go to: **http://localhost:8000**

## 🎯 How to Use

### Web Interface (Recommended)

1. **Visit the frontend**: Go to `http://localhost:8000`
2. **Enter a topic**: Ask any educational question (e.g., "Why do birds sing?")
3. **Customize** (optional): Add age and interests for personalized content
4. **Generate**: Click the button and wait for the AI to create your explanation
5. **Enjoy**: Read the explanation, view the diagram, and listen to the audio!

### API Endpoint

You can also use the API directly:

```bash
curl -X POST "http://localhost:8000/generate" \
  -F "topic=Why do birds sing?" \
  -F "age=7" \
  -F "interests=nature,music"
```

**Response includes:**
- `result`: Kid-friendly explanation with analogy
- `diagram_url`: URL to the generated diagram
- `audio_url`: URL to the audio narration

## 🏗️ Architecture

### CrewAI Agents

1. **Educational Content Researcher**: Gathers accurate, age-appropriate information
2. **Content Safety Validator**: Ensures content is safe and appropriate for children
3. **Kid-Friendly Analogy Generator**: Creates memorable analogies and stories
4. **Final Response Presenter**: Combines everything into a cohesive explanation

### Multimodal Output

- **Text**: Comprehensive, kid-friendly explanation
- **Image**: DALL-E generated educational diagram
- **Audio**: OpenAI TTS narration of the explanation

## 📁 Project Structure

```
kidapp/
├── src/kidapp/
│   ├── api.py              # FastAPI server with endpoints
│   ├── crew.py             # CrewAI pipeline configuration
│   ├── agents/             # Individual AI agents
│   ├── tasks/              # Agent tasks and workflows
│   ├── static/             # Frontend assets
│   │   └── index.html      # Web interface
│   └── config/             # Configuration files
├── uploaded_images/        # Generated diagrams and audio
├── pyproject.toml          # Project dependencies
└── README.md              # This file
```

## 🎨 Example Topics

Try these fun questions:
- "Why do birds sing?"
- "How do plants grow?"
- "What makes rainbows?"
- "Why do we dream?"
- "How do airplanes fly?"
- "What causes thunder?"
- "How do bees make honey?"

## 🔧 Development

### Adding New Features

1. **New Agents**: Add to `src/kidapp/agents/`
2. **New Tasks**: Add to `src/kidapp/tasks/`
3. **Frontend**: Modify `src/kidapp/static/index.html`

### Testing

```bash
# Test the API
curl -X POST "http://localhost:8000/generate" -F "topic=Why do birds sing?"

# Test the frontend
# Open http://localhost:8000 in your browser
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **CrewAI**: For the multi-agent framework
- **OpenAI**: For GPT-4, DALL-E, and TTS capabilities
- **FastAPI**: For the web framework
- **All contributors**: For making education more accessible and fun!

---

**Made with ❤️ for curious kids everywhere!**
