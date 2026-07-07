import json
from fastapi import FastAPI,Path,Query,HTTPException

app = FastAPI()

def data_load():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data 

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/patients")
def get_patients():
    data = data_load()
    return {"patients": data}

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str=Path(..., description="The ID of the patient to retrieve",example="p001")):
    data = data_load()
    if patient_id in data:
        return {"patient": data[patient_id]}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")  

sort_fields = ["name", "age", "condition", "weight", "height"]
@app.get("/sorted_patients")
def get_sorted_patients(sort_by: str = Query(..., description="The field to sort by", example=sort_fields[0]), sort_order: str = Query("asc", description="The order to sort by", example="asc")):

    data = data_load()

    if sort_by not in sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    if sort_order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order")
    
    sorted_order=True if sort_order == "asc" else False
    sorted_data = dict(sorted(data.values(), key=lambda x: x.get(sort_by), reverse=sorted_order))
    return {"sorted_patients": sorted_data}

