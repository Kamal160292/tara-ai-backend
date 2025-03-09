from fastapi import FastAPI, HTTPException, Query
import json
import os

# Load AI Knowledge Base JSON
JSON_FILE = "Final_Para_AUM_Optimized_Complete.json"
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
    pincode: str, product: str, family_structure: str, parent_size: str, eldest_age: str, sum_insured: str,
    parent_1_age: str = None, parent_2_age: str = None, parent_3_age: str = None, parent_4_age: str = None
):
    """Retrieve pricing based on user input."""

    # Fetch Zone from Pincode Mapping
    zone = knowledge_base["Pincode_Zone_Mapping"].get(pincode, {}).get(product, {}).get("Zone", "Unknown")
    if zone == "Unknown":
        raise HTTPException(status_code=404, detail="Pincode not mapped to a valid zone")

    # Debugging: Print Variables to Logs
    print(f"Looking for Pricing: Product={product}, Zone={zone}, Family={family_structure}, Parent Size={parent_size}, Eldest Age={eldest_age}, Sum Insured={sum_insured}")
    
    # Fetch Pricing Data
    price_data = (
        knowledge_base["Pricing_Data"]
        .get(product, {})
        .get(zone, {})
        .get(family_structure, {})
        .get(parent_size, {})
        .get(eldest_age, {})
        .get(parent_1_age, {})
        .get(parent_2_age, {})
        .get(parent_3_age, {})
        .get(parent_4_age, {})
        .get(f"Sum_Insured_{sum_insured}", {})
    )

    if not price_data:
        raise HTTPException(status_code=404, detail="Pricing details not found for the given input")

    return {"zone": zone, "pricing_details": price_data}

@app.get("/get_coverage")
def get_coverage(product: str, sum_insured: str):
    """Retrieve coverage details for a product and sum insured."""
    coverage_data = knowledge_base["Coverage_Data"].get(product, {}).get(f"Sum_Insured_{sum_insured}", {})
    if not coverage_data:
        raise HTTPException(status_code=404, detail="Coverage details not found")

    return {"coverage_details": coverage_data}

@app.get("/get_exclusions")
def get_exclusions(product: str):
    """Retrieve exclusions for a product."""
    exclusions = knowledge_base["Exclusions_Data"].get(product, [])
    if not exclusions:
        raise HTTPException(status_code=404, detail="No exclusions found for this product")

    return {"exclusions": exclusions}

@app.get("/compare_plans")
def compare_plans(pincode: str, product1: str, product2: str, sum_insured: str):
    """Compare two insurance plans based on pricing and coverage."""

    # Fetch Zone
    zone = knowledge_base["Pincode_Zone_Mapping"].get(pincode, {}).get(product1, {}).get("Zone", "Unknown")
    if zone == "Unknown":
        raise HTTPException(status_code=404, detail="Pincode not mapped to a valid zone")

    # Fetch Pricing and Coverage for both products
    price1 = knowledge_base["Pricing_Data"].get(product1, {}).get(zone, {}).get(f"Sum_Insured_{sum_insured}", {})
    price2 = knowledge_base["Pricing_Data"].get(product2, {}).get(zone, {}).get(f"Sum_Insured_{sum_insured}", {})
    coverage1 = knowledge_base["Coverage_Data"].get(product1, {}).get(f"Sum_Insured_{sum_insured}", {})
    coverage2 = knowledge_base["Coverage_Data"].get(product2, {}).get(f"Sum_Insured_{sum_insured}", {})

    return {
        "zone": zone,
        "comparison": {
            "product1": {"pricing": price1, "coverage": coverage1},
            "product2": {"pricing": price2, "coverage": coverage2},
        },
    }

@app.post("/query_para_aum")
def query_para_aum(query_type: str, inputs: dict):
    """Unified API for all PARA AUM queries"""

    if query_type == "get_quote":
    return get_quote(
        pincode=inputs["pincode"],
        product=inputs["product"],
        family_structure=inputs["family_structure"],
        parent_size=inputs["parent_size"],
        eldest_age=inputs["eldest_age"],
        sum_insured=inputs["sum_insured"],
        parent_1_age=inputs.get("parent_1_age", None),
        parent_2_age=inputs.get("parent_2_age", None),
        parent_3_age=inputs.get("parent_3_age", None),
        parent_4_age=inputs.get("parent_4_age", None)
    )


    elif query_type == "get_coverage":
        return get_coverage(**inputs)

    elif query_type == "get_exclusions":
        return get_exclusions(**inputs)

    elif query_type == "compare_plans":
        return compare_plans(**inputs)

    else:
        raise HTTPException(status_code=400, detail="Invalid query type")

