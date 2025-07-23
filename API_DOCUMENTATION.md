# WonderBot API Documentation

## Overview

WonderBot is an AI-powered educational web application that provides kid-friendly explanations for topics and images. This API allows you to interact with the WonderBot system programmatically.

## Base URL

For deployed applications:
```
https://your-app-name.onrender.com
```

For local development:
```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. However, you need to set the `OPENAI_API_KEY` environment variable for the application to function.

## Endpoints

### 1. Generate Explanation

**Endpoint:** `POST /generate`

**Description:** Generate a kid-friendly explanation for either a text topic or an uploaded image.

**Request Format:** `multipart/form-data`

**Parameters:**
- `topic` (optional, string): The text question or topic to explain
- `image` (optional, file): An image file to analyze and explain
- `age` (optional, integer): The child's age for personalized content
- `interests` (optional, string): Comma-separated list of interests

**Example Request (Text):**
```bash
curl -X POST "https://your-app-name.onrender.com/generate" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "topic=Why do birds sing?&age=7&interests=nature,music"
```

**Example Request (Image):**
```bash
curl -X POST "https://your-app-name.onrender.com/generate" \
  -F "image=@path/to/image.jpg" \
  -F "age=8" \
  -F "interests=animals,science"
```

**Response Format:**
```json
{
  "outputs": {
    "result": "Kid-friendly explanation text",
    "diagram_url": "/uploaded_images/diagram_xxx.png",
    "audio_url": "/uploaded_images/audio_xxx.mp3"
  }
}
```

### 2. Web Interface

**Endpoint:** `GET /`

**Description:** Serves the web interface for WonderBot.

**Response:** HTML page with the WonderBot interface.

### 3. API Documentation

**Endpoint:** `GET /docs`

**Description:** Interactive API documentation (Swagger UI).

## Features

### Multi-Modal Output
- **Text**: Comprehensive, age-appropriate explanations
- **Visual Diagrams**: DALL-E generated educational illustrations
- **Audio**: Text-to-speech narration of explanations

### Content Safety
- Built-in guardrails ensure all content is kid-appropriate
- Automatic filtering of inappropriate content
- Age-appropriate language and explanations

### Personalization
- Age-based content customization
- Interest-based topic selection
- Adaptive explanation complexity

## Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "error": "Please provide either a question or an image, but not both."
}
```

**500 Internal Server Error:**
```json
{
  "error": "Error message describing the issue"
}
```

## Rate Limits

Currently, no rate limits are enforced. However, please be mindful of API usage to ensure fair access for all users.

## Security Notes

- All content is filtered for kid-appropriate material
- No user data is stored permanently
- Generated images and audio are temporary and may be cleaned up

## Support

For API-related issues or questions:
- Check the interactive documentation at `/docs`
- Review the deployment guide in `DEPLOYMENT.md`
- Open an issue on the project's GitHub repository 