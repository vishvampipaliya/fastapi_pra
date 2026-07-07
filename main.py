import json
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Path, Query, HTTPException
from typing import Annotated,Literal,Optional
from pydantic import BaseModel, Field,computed_field

class Patient(BaseModel):
    id: Annotated[str,Field(..., description="The ID of the patient", examples=["p001"])]
    name: Annotated[str,Field(..., description="The name of the patient", examples=["John Doe"])]
    age: Annotated[int,Field(..., gt=0, lt=150, description="The age of the patient", examples=[30])]
    gender: Annotated[Literal["Male", "Female"],Field(..., description="The gender of the patient", examples=["Male"])]
    condition: Annotated[str,Field(..., min_length=1, max_length=50, description="The medical condition of the patient", examples=["Hypertension"])]
    weight: Annotated[float,Field(...,gt=0, description="The weight of the patient", examples=[70.5])]
    height: Annotated[float,Field(...,gt=0, description="The height of the patient", examples=[175.0])]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / ((self.height / 100) ** 2), 2)
    
class PatientUpdate(BaseModel):
    name: Optional[Annotated[str,Field(default=None)]]
    gender: Optional[Annotated[Literal["Male", "Female"],Field(default=None)]]
    age: Optional[Annotated[int,Field(default=None, gt=0, lt=150)]]
    condition: Optional[Annotated[str,Field(default=None, min_length=1, max_length=50)]]
    weight: Optional[Annotated[float,Field(default=None,gt=0)]]
    height: Optional[Annotated[float,Field(default=None,gt=0)]]
 
# Initialize FastAPI app
app = FastAPI()


# Helper function to load patient data
def data_load():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data
    
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)



# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Get all patients
@app.get("/patients")
def get_patients():
    data = data_load()
    return {"patients": data}


# Get single patient by ID
@app.get("/patients/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", examples="p001")):
    data = data_load()
    if patient_id in data:
        return {"patient": data[patient_id]}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")


# Define sortable fields
sort_fields = ["name", "age", "condition", "weight", "height"]


# Get sorted patients
@app.get("/sorted_patients")
def get_sorted_patients(
    sort_by: str = Query(..., description="The field to sort by", examples=sort_fields[0]),
    sort_order: str = Query("asc", description="The order to sort by", examples="asc")
):
    data = data_load()

    if sort_by not in sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    if sort_order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order")

    sorted_order = True if sort_order == "asc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by), reverse=not sorted_order)
    return {"sorted_patients": sorted_data}

@app.post("/create_patient")
def add_patient(patient: Patient):
    data = data_load()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    
    patient_data = patient.model_dump(exclude={"id"})
    data[patient.id] = patient_data
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient added successfully", "patient": patient_data}) 

@app.put("/update_patient/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = data_load()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient = data[patient_id]
    updated_data = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        existing_patient[key] = value
        existing_patient['id'] = patient_id  # Ensure the ID remains unchanged
        patient = Patient(**existing_patient)
        existing_patient = patient.model_dump(exclude={"id"})  # Validate the updated patient data

    data[patient_id] = existing_patient
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully", "patient": existing_patient})

@app.delete("/delete_patient/{patient_id}")
def delete_patient(patient_id: str):
    data = data_load()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"}) 