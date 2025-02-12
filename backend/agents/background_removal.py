from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import io
from PIL import Image
import numpy as np
from rembg import remove

router = APIRouter()

@router.post("/remove_background")
async def remove_background(image: UploadFile = File(...)):
    """API Endpoint to remove background from a product image using U²-Net via `rembg`."""

    # Read uploaded image
    image_data = await image.read()
    image_pil = Image.open(io.BytesIO(image_data))

    # Convert image to RGBA (ensures proper transparency)
    image_pil = image_pil.convert("RGBA")

    # Process image using rembg (U²-Net)
    processed_image = remove(image_pil)

    # Convert back to bytes for response
    img_bytes = io.BytesIO()
    processed_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/png")  #  Return as file response
