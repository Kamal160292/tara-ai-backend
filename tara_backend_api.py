from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import gzip

# Initialize FastAPI app
app = FastAPI()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import gzip

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Add this root route to fix the 404 error
@app.get("/")
def home():
    return {"message": "Tara AI Backend is running 🎉"}

# ✅ Load the optimized JSON file
JSON_FILE_PATH = "PARA_AUM_Production_Ready_KB_Optimized.json.gz"
with gzip.open(JSON_FILE_PATH, "rt", encoding="utf-8") as file:
    knowledge_base = json.load(file)

# ✅ Debug: Print loaded JSON keys
print("Loaded JSON Keys:", knowledge_base.keys())

# ✅ Define Request Model
class QuoteRequest(BaseModel):
    product: str
    zone: str
    familyStructure: str
    parentSize: str
    sumInsured: str

# ✅ Add Debugging to Check If Keys Exist
@app.post("/get_quote")
def get_quote(request: QuoteRequest):
    try:
        print(f"Received request: {request.dict()}")
        print("Available Products:", knowledge_base["Knowledge_Base"]["PR"].keys())

        if request.product not in knowledge_base["Knowledge_Base"]["PR"]:
            raise HTTPException(status_code=404, detail="Product not found in JSON")

        pricing_path = knowledge_base["Knowledge_Base"]["PR"][request.product]
        print("Available Zones:", pricing_path.keys())

        if request.zone not in pricing_path:
            raise HTTPException(status_code=404, detail="Zone not found in JSON")

        pricing_path = pricing_path[request.zone]
        print("Available Family Structures:", pricing_path.keys())

        if request.familyStructure not in pricing_path:
            raise HTTPException(status_code=404, detail="Family Structure not found in JSON")

        pricing_path = pricing_path[request.familyStructure]
        print("Available Parent Sizes:", pricing_path.keys())

        if request.parentSize not in pricing_path:
            raise HTTPException(status_code=404, detail="Parent Size not found in JSON")

        pricing_path = pricing_path[request.parentSize]
        print("Available Sum Insured:", pricing_path.keys())

        if request.sumInsured not in pricing_path:
            raise HTTPException(status_code=404, detail="Sum Insured not found in JSON")

        print("Retrieved Pricing Data:", pricing_path)  # Debug log

if "FP" not in pricing_path:
    raise HTTPException(status_code=404, detail=f"Missing 'FP' in JSON Data: {pricing_path}")

return {
    "finalPremium": pricing_path["FP"],
    "optionalCovers": {k: v for k, v in pricing_path.items() if k not in ["FP"]}
}

    
    except KeyError as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Missing key in JSON: {str(e)}")


# ✅ Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

