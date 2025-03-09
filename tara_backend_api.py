@app.get("/")
def home():
    return {"message": "Tara AI Backend is running 🎉"}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import gzip

# Load the optimized JSON file
JSON_FILE_PATH = "PARA_AUM_Production_Ready_KB_Optimized.json.gz"
with gzip.open(JSON_FILE_PATH, "rt", encoding="utf-8") as file:
    knowledge_base = json.load(file)

app = FastAPI()

class QuoteRequest(BaseModel):
    product: str
    zone: str
    familyStructure: str
    parentSize: str
    sumInsured: str

@app.post("/get_quote")
def get_quote(request: QuoteRequest):
    try:
        pricing_path = knowledge_base["Knowledge_Base"]["PR"][request.product][request.zone][request.familyStructure][request.parentSize][request.sumInsured]
        return {
            "finalPremium": pricing_path["FP"],
            "optionalCovers": {k: v for k, v in pricing_path.items() if k not in ["FP"]}
        }
    except KeyError:
        raise HTTPException(status_code=404, detail="No pricing found for the selected criteria.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

