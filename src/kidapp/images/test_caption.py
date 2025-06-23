# src/kidapp/images/test_caption.py

import os, sys
from huggingface_hub import InferenceClient

if len(sys.argv) != 2:
    print("Usage: python test_caption.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]
hf_token   = os.getenv("HF_API_TOKEN")
if not hf_token:
    print("❌ HF_API_TOKEN not set.")
    sys.exit(1)

# 1) build the InferenceClient
client = InferenceClient(token=hf_token)

# 2) read your image bytes
with open(image_path, "rb") as f:
    image_bytes = f.read()

# 3) call image_to_text with `inputs=…`
result = client.image_to_text(
    model="Salesforce/blip-image-captioning-base",
    inputs=image_bytes
)

print("Raw result:", result)
print("Caption   :", result[0]["generated_text"])
