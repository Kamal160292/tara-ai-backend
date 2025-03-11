from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load AI Knowledge Base JSON
json_path = os.getenv("JSON_PATH", "Final_Optimized_FastAPI_JSON_v6.json")

# Check if the JSON file exists in the current directory (for Render)
if not os.path.exists(json_path):
    json_path = "/opt/render/project/src/Final_Optimized_FastAPI_JSON_v6.json"

if not os.path.exists(json_path):
    raise FileNotFoundError(f"JSON file not found: {json_path}")

with open(json_path, "r", encoding="utf-8") as file:
    knowledge_base = json.load(file)

app = FastAPI()

# ✅ Enable CORS with OPTIONS requests to fix preflight errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (can restrict later)
    allow_credentials=True,
    allow_methods=["OPTIONS", "POST", "GET", "PUT", "DELETE"],  # Explicitly allow OPTIONS for preflight
    allow_headers=["*"],  # Allow all headers
)

# ✅ Allow OPTIONS requests for every POST endpoint
@app.options("/{full_path:path}")
async def preflight_handler(full_path: str, request: Request):
    return {}

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

# ✅ Fix: Get Zone Function (Using Correct JSON Structure)
def get_zone(product_id, pincode):
    key = f"{product_id}|{pincode}"
    return knowledge_base["pincode_zone_mapping"].get(key, "Unknown")

@app.get("/")
def home():
    return {"message": "Welcome to Tara AI Backend!"}

@app.post("/get_quote")  
def get_quote(request: QueryRequest):  
    zone = get_zone(request.product_id, request.pincode)
    key = f"{request.product_id}|{request.sum_insured}|{request.eldest_adult_age_band}|{zone}|{request.family_structure}|{request.parent_size}|{request.parent_age_band}"

    logging.debug(f"Generated Key for Quote: {key}")
    
    if key in knowledge_base["pricing_index"]:
        return knowledge_base["pricing_index"][key]
    else:
        logging.warning(f"Quote not found for key: {key}")
        return {"error": "Quote not found", "generated_key": key}

@app.post("/recommend_product")
def recommend_product(request: QueryRequest):
    return {"recommendation": "Product recommendation logic will be implemented here."}

@app.get("/get_product_info/{product_id}/{sum_insured}")
def get_product_info(product_id: str, sum_insured: str):
    key = f"{product_id}|{sum_insured}"
    return {"info": knowledge_base["benefits_index"].get(key, "No details found")}

@app.get("/get_coverage_exclusions/{product_id}/{disease}")
def get_coverage_exclusions(product_id: str, disease: str):
    key = f"{product_id}|{disease}"
    return knowledge_base["exclusions_index"].get(key, {"error": "No exclusion data found"})

@app.post("/get_custom_pitch")
def get_custom_pitch(request: QueryRequest):
    return {"pitch": "Custom sales pitch logic will be implemented here."}

@app.post("/ai_roleplay")
def ai_roleplay(request: QueryRequest):
    return {"response": "AI roleplay logic will be implemented here."}

# ✅ Fix: Ensure Render Runs This Properly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

