from fastapi import FastAPI, UploadFile, Form, APIRouter, File
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import ollama  #  LLaMA 3.2 for text generation
import spacy
import io

router = APIRouter()
#  Load BLIP Model (for Image-to-Text captioning)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

#  Load spaCy NER Model (for Brand Extraction)
nlp = spacy.load("en_core_web_sm")

def extract_product_details(title):
    """Extracts brand and product type from the title using NLP"""
    doc = nlp(title)
    brand = ""
    product_type = ""
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            brand = ent.text
    # Extract keywords manually if no brand is found
    if not brand:
        brand = title.split()[0]  # First word as fallback
    return brand, title  # Returning title as product_type for now

def generate_description(image, title):
    """Generates SEO-friendly product descriptions from an image and title"""
    
    #  Step 1: Generate Image Caption
    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        generated_ids = model.generate(**inputs)
        image_caption = processor.decode(generated_ids[0], skip_special_tokens=True)

    #  Step 2: Extract Product Details from Title
    brand, product_type = extract_product_details(title)

    # Step 3: Generate a Persuasive Description using LLaMA 3.2
    prompt = f"""
        Generate a compelling, engaging, and SEO-optimized product description for "{title}". 
        - Highlight its key features and benefits.
        - Use persuasive language.
        - Do not include unnecessary sections like "This description includes...".
        - Ensure the text is natural and suitable for an e-commerce listing.
        - Only return the description, nothing else.
        """
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    
    return response["message"]["content"]


@router.post("/generate")
async def get_description(image: UploadFile = File(...), title: str = Form(...)):
    """Endpoint to generate product descriptions based on image + title"""
    try:
        image_data = await image.read()
        image_pil = Image.open(io.BytesIO(image_data))

        # Call description generation function
        description = generate_description(image_pil, title)
        
        return {"description": description}
    
    except Exception as e:
        return {"error": f"Failed to process image: {str(e)}"}