from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

# Load Optimized JSON
json_path = "Final_Optimized_FastAPI_JSON_v6.json"
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

app = FastAPI()

# Base Model for API Requests
class QueryRequest(BaseModel):
    query_type: str
    product_id: str
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

# Function to get zone from pincode
def get_zone(product_id, pincode):
    key = f"{product_id}|{pincode}"
    return data["pincode_zone_mapping"].get(key, "Unknown")

# API: General Query Handler
@app.post("/query")
def query(request: QueryRequest):
    if request.query_type == "quote_generation":
        return get_quote(request)
    elif request.query_type == "recommend_product":
        return recommend_product(request)
    elif request.query_type == "product_info":
        return get_product_info(request.product_id, request.sum_insured)
    elif request.query_type == "coverage_exclusion":
        return get_coverage_exclusions(request.product_id, request.disease)
    elif request.query_type == "custom_pitch":
        return get_custom_pitch(request)
    elif request.query_type == "ai_roleplay":
        return ai_roleplay(request)
    else:
        raise HTTPException(status_code=400, detail="Invalid query type")

# API: Get Quote
@app.post("/get_quote")
def get_quote(request: QueryRequest):
    zone = get_zone(request.product_id, request.pincode)
    key = f"{request.product_id}|{request.sum_insured}|{request.eldest_adult_age_band}|{zone}|{request.family_structure}|{request.parent_size}|{request.parent_age_band}"
    
    if key in data["pricing_index"]:
        return data["pricing_index"][key]
    else:
        raise HTTPException(status_code=404, detail="Quote not found")

# API: Recommend Product
@app.post("/recommend_product")
def recommend_product(request: QueryRequest):
    return {"recommendation": "Product recommendation logic will be here!"}

# API: Get Product Info
@app.get("/get_product_info/{product_id}/{sum_insured}")
def get_product_info(product_id: str, sum_insured: str):
    key = f"{product_id}|{sum_insured}"
    return {"info": data["benefits_index"].get(key, "No details found")}

# API: Get Coverage & Exclusions
@app.get("/get_coverage_exclusions/{product_id}/{disease}")
def get_coverage_exclusions(product_id: str, disease: str):
    key = f"{product_id}|{disease}"
    return data["exclusions_index"].get(key, {"error": "No exclusion data found"})

# API: Get Custom Sales Pitch
@app.post("/get_custom_pitch")
def get_custom_pitch(request: QueryRequest):
    return {"pitch": "Custom sales pitch logic will be here!"}

# API: AI Roleplay
@app.post("/ai_roleplay")
def ai_roleplay(request: QueryRequest):
    return {"response": "AI roleplay logic will be here!"}

# Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
