# WonderBot - AI-Powered Educational Web App for Kids

WonderBot is an intelligent educational application that uses AI agents to explain topics and analyze images in a kid-friendly way. Built with FastAPI, CrewAI, and OpenAI, it provides multimodal responses including text explanations, visual diagrams, and audio narration.

## 🌟 Features

- **Multi-Agent AI Collaboration**: Uses CrewAI agents (Researcher, Validator, Analogy, Presenter) for comprehensive explanations
- **Image Analysis**: Upload images and get kid-friendly explanations using OpenAI's GPT-4 Vision
- **Text Q&A**: Ask questions and receive age-appropriate answers
- **Multimodal Output**: Get text explanations, visual diagrams (DALL-E), and audio narration (TTS)
- **Content Safety**: Built-in guardrails ensure all content is safe and appropriate for children
- **Personalization**: Specify age and interests for tailored explanations
- **Fast Path**: Quick responses for simple questions to reduce latency
- **Caching**: In-memory caching for improved performance

## 🚀 Quick Start

### Prerequisites
- Python 3.10-3.13
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd wonderbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   uvicorn src.kidapp.api:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**
   - Web interface: http://localhost:8000
   - API documentation: http://localhost:8000/docs

## 🏗️ Project Structure

```
wonderbot/
├── src/
│   └── kidapp/
│       ├── __init__.py
│       ├── api.py                 # Main FastAPI application
│       ├── crew.py                # CrewAI agents and tasks
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── image_analyzer.py  # Image analysis agent
│       │   └── guardrails_agent.py # Content safety agent
│       ├── tasks/
│       │   ├── __init__.py
│       │   ├── task_analogy.py    # Analogy generation task
│       │   ├── task_image_analysis.py # Image analysis task
│       │   ├── task_present.py    # Presentation task
│       │   ├── task_research.py   # Research task
│       │   ├── task_validate.py   # Validation task
│       │   ├── task_image_present.py # Image presentation task
│       │   └── task_guardrails.py # Safety validation task
│       ├── tools/
│       │   └── __init__.py
│       └── static/
│           └── index.html         # Frontend web interface
├── uploaded_images/               # Generated diagrams and audio
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline
├── pyproject.toml                 # Project configuration
├── requirements.txt               # Python dependencies
├── Procfile                      # Deployment configuration
├── runtime.txt                   # Python version specification
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── API_DOCUMENTATION.md          # API documentation
├── DEPLOYMENT.md                 # Deployment guide
├── criteria.yaml                 # Quality assurance criteria
├── test_questions.csv            # Test questions for CI/CD
└── generate_answers.py           # Test data generation script
```

## 🤖 AI Agents Architecture

### CrewAI Agents
1. **Image Analyzer**: Analyzes uploaded images using OpenAI GPT-4 Vision
2. **Researcher**: Gathers information and facts about topics
3. **Validator**: Ensures factual accuracy and appropriateness
4. **Analogy Agent**: Creates relatable analogies for kids
5. **Presenter**: Formats content for optimal kid-friendly delivery
6. **Guardrails Agent**: Ensures content safety and moderation

### Workflow
1. **Input Processing**: Determines if input is image or text
2. **Fast Path Check**: For simple text questions, uses direct LLM call
3. **CrewAI Pipeline**: For complex requests, orchestrates multiple agents
4. **Multimodal Generation**: Creates text, diagrams, and audio
5. **Safety Validation**: Ensures all content is kid-appropriate

## 📡 API Endpoints

### POST `/generate`
Main endpoint for generating explanations.

**Parameters:**
- `topic` (optional): Text question or topic
- `image` (optional): Uploaded image file
- `age` (optional): Child's age for personalization
- `interests` (optional): Comma-separated interests

**Response:**
```json
{
  "outputs": {
    "result": "Kid-friendly explanation",
    "diagram_url": "/uploaded_images/diagram_xxx.png",
    "audio_url": "/uploaded_images/audio_xxx.mp3"
  }
}
```

### GET `/`
Serves the web interface.

## 🚀 Deployment

### Render Deployment
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn src.kidapp.api:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `OPENAI_API_KEY`

## 🧪 Testing

### Local Testing
```bash
# Test the API
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "topic=Why do birds sing?"

# Test with image
curl -X POST "http://localhost:8000/generate" \
  -F "image=@path/to/image.jpg"
```

### CI/CD Testing
The project includes automated testing via GitHub Actions:
- Runs quality assurance checks using Judgeval
- Tests kid-friendliness, analogy usage, and factual correctness
- Sends notifications to Slack on build status

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Required for AI functionality
- `PORT`: Port for the web server (set by deployment platform)

### Customization
- Modify agent roles in `src/kidapp/crew.py`
- Adjust safety patterns in `src/kidapp/agents/guardrails_agent.py`
- Update frontend styling in `src/kidapp/static/index.html`

## 🛡️ Safety Features

- **Content Moderation**: Automatic filtering of inappropriate content
- **Age-Appropriate Language**: Tailored explanations for different age groups
- **Factual Validation**: Ensures accuracy of information
- **Safe Image Generation**: DALL-E prompts designed for kid-friendly content

## 📊 Performance

- **Fast Path**: Simple questions answered in <2 seconds
- **Caching**: In-memory cache for repeated queries
- **Async Processing**: Non-blocking API responses
- **Optimized Dependencies**: Minimal, focused dependency tree

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the API documentation in `API_DOCUMENTATION.md`
- Review deployment guide in `DEPLOYMENT.md`
- Open an issue on GitHub

---

**WonderBot** - Making learning fun and accessible for every child! 🎓✨
