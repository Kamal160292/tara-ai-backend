from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import gzip

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Root Route to confirm API is live
@app.get("/")
def home():
    return {"message": "Tara AI Backend is running 🎉"}

# ✅ Load the optimized JSON file
JSON_FILE_PATH = "PARA_AUM_Production_Ready_KB_Optimized.json.gz"
try:
    with gzip.open(JSON_FILE_PATH, "rt", encoding="utf-8") as file:
        knowledge_base = json.load(file)
    print("Loaded JSON Keys:", knowledge_base.keys())
except Exception as e:
    print(f"Error loading JSON file: {str(e)}")
    knowledge_base = {}

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
        if "Knowledge_Base" not in knowledge_base or "PR" not in knowledge_base["Knowledge_Base"]:
            raise HTTPException(status_code=500, detail="Pricing data not found in JSON")
        
        pricing_data = knowledge_base["Knowledge_Base"]["PR"]
        print("Available Products:", pricing_data.keys())
        if request.product not in pricing_data:
            raise HTTPException(status_code=404, detail="Product not found in JSON")

        pricing_path = pricing_data[request.product]
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
        print("Available Sum Insured Options:", pricing_path.keys())
        if request.sumInsured not in pricing_path:
            raise HTTPException(status_code=404, detail="Sum Insured not found in JSON")

        pricing_path = pricing_path[request.sumInsured]
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
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

# ✅ Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)


