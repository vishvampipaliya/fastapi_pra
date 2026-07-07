from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator
from typing import Optional,List,Dict,Annotated

class Patient(BaseModel):
    name:str
    age:int
    weight:float
    email:EmailStr
    married:bool
    allergies:List[str]
    contact_info:Dict[str,str]

    @model_validator(mode="after")
    def valident_emg_contact(cls,model):
        if model.age > 60 and "emergency" not in model.contact_info:
            raise ValueError("Emergency contact is required in contact_info")
        return model


def patient_detail(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)

patient_info={"name": "John Doe", "age": 55, "weight": 70.5, "email": "john.doe@gmail.com", "married": True, "allergies": ["penicillin"], "contact_info": {"email": "john.doe@hdfc.com"}}   
patient = Patient(**patient_info)
patient_detail(patient)