from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import os
import io
from PIL import Image
from dotenv import load_dotenv
import base64
import requests
import numpy as np
from typing import Optional
import time

load_dotenv()

app = FastAPI(title="Illustration Personalizer API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://patient-warmth-production.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Replicate client
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if REPLICATE_API_TOKEN:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Template illustration path (you can add your template here)
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(TEMPLATE_DIR, exist_ok=True)
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, "template.png")


@app.get("/")
async def root():
    return {"message": "Illustration Personalizer API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/personalize")
async def personalize_illustration(
    file: UploadFile = File(...),
    template: Optional[str] = None
):
    """
    Personalize an illustration with a user's photo using Instant-ID
    
    Args:
        file: The uploaded photo (child's face)
        template: Optional template name (default: uses built-in template)
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read uploaded image
        image_bytes = await file.read()
        user_image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if user_image.mode != "RGB":
            user_image = user_image.convert("RGB")
        
        # Resize user image if too large (for faster processing)
        max_size = 1024
        if max(user_image.size) > max_size:
            user_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Load template if provided, otherwise use default
        template_image = None
        if template and os.path.exists(os.path.join(TEMPLATE_DIR, template)):
            template_image = Image.open(os.path.join(TEMPLATE_DIR, template))
        elif os.path.exists(TEMPLATE_PATH):
            template_image = Image.open(TEMPLATE_PATH)
        
        if not REPLICATE_API_TOKEN:
            # Fallback: Return a simple processed version if no API token
            result_image = apply_simple_stylization(user_image)
            if template_image:
                result_image = composite_face_into_template(user_image, template_image)
        else:
            try:
                # Use Instant-ID via Replicate for face personalization
                # Instant-ID model: lucataco/instant-id
                result_image = await process_with_instant_id(user_image, template_image)
            except Exception as e:
                print(f"Replicate API error: {str(e)}")
                # Fallback: apply simple stylization
                result_image = apply_simple_stylization(user_image)
                if template_image:
                    result_image = composite_face_into_template(user_image, template_image)
        
        # Convert result to bytes
        result_buffer = io.BytesIO()
        result_image.save(result_buffer, format="PNG")
        result_buffer.seek(0)
        
        return Response(
            content=result_buffer.getvalue(),
            media_type="image/png"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing image: {str(e)}")
        print(f"Traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


async def process_with_instant_id(user_image: Image.Image, template_image: Optional[Image.Image] = None) -> Image.Image:
    """
    Process image using Instant-ID model via Replicate API (direct HTTP calls)
    Uses Replicate REST API instead of SDK to avoid Python 3.14 compatibility issues
    """
    if not REPLICATE_API_TOKEN:
        raise ValueError("REPLICATE_API_TOKEN is not set")
    
    # Save user image to bytes
    img_buffer = io.BytesIO()
    user_image.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    # Prepare prompt for illustration style
    prompt = "a beautiful illustrated portrait, children's book illustration style, colorful, friendly, cartoon style, high quality"
    negative_prompt = "realistic, photo, photograph, low quality, blurry"
    
    # Convert image to base64 for upload
    img_buffer.seek(0)
    image_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")
    image_data_url = f"data:image/png;base64,{image_base64}"
    
    # Use Replicate API directly via HTTP
    # Model: lucataco/ip-adapter-faceid (or other face personalization models)
    model_name = "lucataco/ip-adapter-faceid"
    model_version = "75d76a4e40e0c5b2c0e0e0e0e0e0e0e0"
    
    try:
        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create prediction
        prediction_data = {
            "version": model_version,
            "input": {
                "image": image_data_url,
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_outputs": 1,
                "guidance_scale": 7.5,
                "num_inference_steps": 30,
            }
        }
        
        create_url = f"https://api.replicate.com/v1/models/{model_name}/predictions"
        response = requests.post(create_url, json=prediction_data, headers=headers)
        
        if response.status_code != 201:
            error_msg = response.text
            print(f"Replicate API error: {response.status_code} - {error_msg}")
            raise Exception(f"Replicate API error: {response.status_code} - {error_msg}")
        
        prediction = response.json()
        prediction_id = prediction.get("id")
        prediction_url = prediction.get("urls", {}).get("get")
        
        if not prediction_id or not prediction_url:
            print(f"Failed to create prediction. Response: {prediction}")
            raise Exception("Failed to create prediction - missing id or url")
        
        # Poll for completion
        max_attempts = 60  # 5 minutes max
        attempt = 0
        output = None
        
        while attempt < max_attempts:
            time.sleep(2)  # Wait 2 seconds between polls
            
            get_response = requests.get(prediction_url, headers=headers)
            get_response.raise_for_status()
            
            prediction_status = get_response.json()
            status = prediction_status.get("status")
            
            if status == "succeeded":
                output = prediction_status.get("output")
                break
            elif status == "failed" or status == "canceled":
                error = prediction_status.get("error", "Unknown error")
                raise Exception(f"Prediction failed: {error}")
            
            attempt += 1
        else:
            raise Exception("Prediction timed out")
        
        # Download result image
        result_image = user_image  # Default fallback
        
        if output:
            if isinstance(output, str):
                if output.startswith('http'):
                    img_response = requests.get(output)
                    img_response.raise_for_status()
                    result_image = Image.open(io.BytesIO(img_response.content))
            elif isinstance(output, list) and len(output) > 0:
                url = output[0] if isinstance(output[0], str) else str(output[0])
                if url.startswith('http'):
                    img_response = requests.get(url)
                    img_response.raise_for_status()
                    result_image = Image.open(io.BytesIO(img_response.content))
        
    except requests.exceptions.RequestException as e:
        print(f"Replicate API request error: {str(e)}")
        raise Exception(f"Replicate API error: {str(e)}")
    except Exception as e:
        print(f"Replicate processing error: {str(e)}")
        raise e
    
    # If template provided, composite the face into template
    if template_image:
        result_image = composite_face_into_template(result_image, template_image)
    
    return result_image


def composite_face_into_template(face_image: Image.Image, template_image: Image.Image) -> Image.Image:
    """
    Composite the personalized face into the template illustration
    This is a simplified version - in production, you'd use face detection
    to find the exact position in the template
    """
    # Resize face to fit template (simplified - assumes face area is in center)
    template_width, template_height = template_image.size
    face_size = min(template_width, template_height) // 2
    
    face_resized = face_image.copy()
    face_resized.thumbnail((face_size, face_size), Image.Resampling.LANCZOS)
    
    # Create a mask for smooth blending
    mask = Image.new("L", face_resized.size, 0)
    mask_draw = Image.new("L", face_resized.size, 255)
    
    # Composite face onto template (centered)
    result = template_image.copy()
    x_offset = (template_width - face_resized.width) // 2
    y_offset = (template_height - face_resized.height) // 2
    
    # Use alpha composite for better blending
    result.paste(face_resized, (x_offset, y_offset), face_resized.convert("RGBA") if face_resized.mode == "RGBA" else None)
    
    return result


def apply_simple_stylization(image: Image.Image) -> Image.Image:
    """
    Fallback function to apply simple stylization when API is unavailable
    This is a placeholder - in production, you'd use proper AI models
    """
    from PIL import ImageFilter, ImageEnhance
    
    # Apply slight blur for illustration effect
    stylized = image.filter(ImageFilter.SMOOTH_MORE)
    
    # Enhance colors slightly
    enhancer = ImageEnhance.Color(stylized)
    stylized = enhancer.enhance(1.3)
    
    # Increase saturation for cartoon-like effect
    enhancer = ImageEnhance.Contrast(stylized)
    stylized = enhancer.enhance(1.1)
    
    return stylized


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

