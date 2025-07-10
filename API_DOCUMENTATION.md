# 🤖 WonderBot API Documentation

## Overview
WonderBot is an AI-powered educational platform that generates kid-friendly explanations, diagrams, and audio for any topic or image.

## Base URL
```
https://your-app-name.railway.app
```

## Endpoints

### POST /generate
Generate educational content for kids.

#### Request Parameters
- `topic` (string, optional): Educational question or topic
- `image` (file, optional): Image to analyze
- `age` (integer, optional): Child's age (3-18)
- `interests` (string, optional): Comma-separated interests

**Note**: Provide either `topic` OR `image`, not both.

#### Example Requests

**Text Question:**
```bash
curl -X POST "https://your-app-name.railway.app/generate" \
  -F "topic=Why do birds sing?" \
  -F "age=7" \
  -F "interests=nature,music"
```

**Image Analysis:**
```bash
curl -X POST "https://your-app-name.railway.app/generate" \
  -F "image=@path/to/image.jpg" \
  -F "age=8" \
  -F "interests=animals"
```

#### Response Format
```json
{
  "outputs": {
    "result": "Kid-friendly explanation with analogy...",
    "diagram_url": "/uploaded_images/diagram_abc123.png",
    "diagram_error": null,
    "audio_url": "/uploaded_images/audio_xyz789.mp3"
  }
}
```

#### Response Fields
- `result`: Kid-friendly text explanation
- `diagram_url`: URL to generated educational diagram
- `diagram_error`: Error message if diagram generation failed
- `audio_url`: URL to text-to-speech audio version

## Web Interface
Visit the base URL to access the user-friendly web interface:
```
https://your-app-name.railway.app
```

## Features
- ✅ **AI-powered explanations** using CrewAI agents
- ✅ **DALL-E generated diagrams** for visual learning
- ✅ **Text-to-speech audio** for accessibility
- ✅ **Image analysis** for uploaded photos
- ✅ **Built-in safety guardrails** for kid-friendly content
- ✅ **Age and interest personalization**

## Error Handling
- **400 Bad Request**: Invalid input (e.g., both topic and image provided)
- **500 Internal Server Error**: API or OpenAI service issues
- **429 Rate Limit**: OpenAI quota exceeded

## Example Topics to Try
- "Why do birds sing?"
- "How do plants grow?"
- "What makes rainbows?"
- "Why do we dream?"
- "How do airplanes fly?"
- "What causes thunder?"
- "How do bees make honey?"

## Security Features
- Content safety validation
- Age-appropriate filtering
- Violence and inappropriate content blocking
- Safe alternatives for blocked content

## Rate Limits
- Depends on your OpenAI API plan
- Free tier: ~3 requests per minute
- Paid plans: Higher limits available

## Support
For issues or questions, check the deployment logs or contact the developer. 