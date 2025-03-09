from fastapi import FastAPI, HTTPException, Query
import json
import os

# Load AI Knowledge Base JSON
JSON_FILE = "Final_Structured_AUM_Knowledge_Base_With_Pricing_Adjusted.json"
if not os.path.exists(JSON_FILE):
    raise FileNotFoundError(f"Error: {JSON_FILE} not found!")

with open(JSON_FILE, "r") as file:
    knowledge_base = json.load(file)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Tara AI Backend!"}

@app.get("/get_quote")
def get_quote(
    pincode: str, product: str, family_structure: str, parent_size: str, age: str, sum_insured: str
):
    """Retrieve pricing based on user input."""
    zone = knowledge_base["Pincode_Zone_Mapping"].get(pincode, {}).get(product, {}).get("Zone", "Unknown")
    if zone == "Unknown":
        raise HTTPException(status_code=404, detail="Pincode not mapped to a valid zone")

    price_data = (
        knowledge_base["Pricing_Data"]
        .get(product, {})
        .get(zone, {})
        .get(family_structure, {})
        .get(parent_size, {})
        .get(age, {})
        .get(f"Sum_Insured_{sum_insured}", {})
    )

    return {"zone": zone, "pricing_details": price_data}

@app.get("/get_coverage")
def get_coverage(product: str, sum_insured: str):
    """Retrieve coverage details for a product and sum insured."""
    coverage_data = knowledge_base["Benefits_Data"].get(product, {}).get(f"Sum_Insured_{sum_insured}", {})
    if not coverage_data:
        raise HTTPException(status_code=404, detail="Coverage details not found")

    return {"coverage_details": coverage_data}

@app.get("/get_exclusions")
def get_exclusions(product: str):
    """Retrieve exclusions for a product."""
    exclusions = knowledge_base["Exclusions"].get(product, [])
    if not exclusions:
        raise HTTPException(status_code=404, detail="No exclusions found for this product")

    return {"exclusions": exclusions}

@app.get("/compare_plans")
def compare_plans(pincode: str, product1: str, product2: str, sum_insured: str):
    """Compare two insurance plans based on pricing and coverage."""
    zone = knowledge_base["Pincode_Zone_Mapping"].get(pincode, {}).get(product1, {}).get("Zone", "Unknown")

    if zone == "Unknown":
        raise HTTPException(status_code=404, detail="Pincode not mapped to a valid zone")

    price1 = knowledge_base["Pricing_Data"].get(product1, {}).get(zone, {}).get(f"Sum_Insured_{sum_insured}", {})
    price2 = knowledge_base["Pricing_Data"].get(product2, {}).get(zone, {}).get(f"Sum_Insured_{sum_insured}", {})
    coverage1 = knowledge_base["Benefits_Data"].get(product1, {}).get(f"Sum_Insured_{sum_insured}", {})
    coverage2 = knowledge_base["Benefits_Data"].get(product2, {}).get(f"Sum_Insured_{sum_insured}", {})

    return {
        "zone": zone,
        "comparison": {
            "product1": {"pricing": price1, "coverage": coverage1},
            "product2": {"pricing": price2, "coverage": coverage2},
        },
    }


