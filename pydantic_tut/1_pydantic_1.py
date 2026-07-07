from typing import Optional,List,Dict,Annotated
from pydantic import BaseModel,EmailStr,AnyUrl,Field

class Patient(BaseModel):
    name : Annotated[str, Field(max_length=50, title="Name of the patient", description ="Full name of the patient", example=["John Doe"])]
    age: int =  Field(..., ge=0, lt=150, description="Age of the patient in years")
    instagram: Optional[AnyUrl] = None
    weight: float = Annotated[float, Field( gt=0,strict=True)]
    height: float =  Field( gt=10)
    married: Annotated[bool, Field(default=False, description="Marital status of the patient", example=True)]
    email: EmailStr
    allergies: Optional[List[str]] = None
    contact_info: Optional[Dict[str, str]] = None



def patient_detail(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.email)
    print(patient.instagram)
    print(patient.allergies)
    print(patient.contact_info)
    print(patient.married)

patient_info={"name": "John Doe", "age": 30, "weight": 70.5, "height": 175.0, "email": "john.doe@example.com", "instagram": "https://www.instagram.com/johndoe", "allergies": ["penicillin"], "contact_info": {"email": "john.doe@example.com"}, "married": True}
patient_1=Patient(**patient_info)
patient_detail(patient_1)