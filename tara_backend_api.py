from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load AI Knowledge Base JSON
json_path = "/Users/kamalnath/tara-ai-backend/Final_Optimized_FastAPI_JSON_v6.json"
if not os.path.exists(json_path):
    logging.error(f"JSON file not found: {json_path}")
    raise FileNotFoundError(f"JSON file not found: {json_path}")

with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)
    logging.info(f"JSON file loaded successfully from {json_path}")

app = FastAPI()

# Define Request Model
class QueryRequest(BaseModel):
    query_type: str
    product_id: str = None
    sum_insured: str = None
    eldest_adult_age_band: str = None
    pincode: str = None
    family_structure: str = None
    parent_size: str = None
    parent_age_band: str = None
    optional_covers: list = None
    budget_range: str = None
    medical_needs: list = None
    scenario: str = None
    expected_objections: list = None

# Helper function to get zone from pincode
def get_zone(product_id, pincode):
    key = f"{product_id}|{pincode}"
    return data["pincode_zone_mapping"].get(key, "Unknown")

@app.get("/")
def home():
    return {"message": "Welcome to Tara AI Backend!"}

@app.post("/get_quote")
def get_quote(request: QueryRequest):
    zone = get_zone(request.product_id, request.pincode)
    key = f"{request.product_id}|{request.sum_insured}|{request.eldest_adult_age_band}|{zone}|{request.family_structure}|{request.parent_size}|{request.parent_age_band}"
    
    logging.debug(f"Generated Key for Quote: {key}")
    
    if key in data["pricing_index"]:
        return data["pricing_index"][key]
    else:
        logging.warning(f"Quote not found for key: {key}")
        return {"error": "Quote not found", "generated_key": key}

@app.post("/recommend_product")
def recommend_product(request: QueryRequest):
    return {"recommendation": "Product recommendation logic will be implemented here."}

@app.get("/get_product_info/{product_id}/{sum_insured}")
def get_product_info(product_id: str, sum_insured: str):
    key = f"{product_id}|{sum_insured}"
    return {"info": data["benefits_index"].get(key, "No details found")}

@app.get("/get_coverage_exclusions/{product_id}/{disease}")
def get_coverage_exclusions(product_id: str, disease: str):
    key = f"{product_id}|{disease}"
    return data["exclusions_index"].get(key, {"error": "No exclusion data found"})

@app.post("/get_custom_pitch")
def get_custom_pitch(request: QueryRequest):
    return {"pitch": "Custom sales pitch logic will be implemented here."}

@app.post("/ai_roleplay")
def ai_roleplay(request: QueryRequest):
    return {"response": "AI roleplay logic will be implemented here."}

# Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

