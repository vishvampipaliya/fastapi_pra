from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import Optional,List,Dict,Annotated

class Patient(BaseModel):
    name:str
    age:int
    weight:float
    height:float
    email:EmailStr
    married:bool
    allergies:List[str]
    contact_info:Dict[str,str]

    @computed_field
    @property
    def bmi(self) -> float:
        return (self.weight / (self.height** 2))

def patient_detail(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.bmi)

patient_info={"name": "John Doe", "age": 30, "weight": 70.5, "height": 175, "email": "john.doe@gmail.com", "married": True, "allergies": ["penicillin"], "contact_info": {"email": "john.doe@hdfc.com"}}   
patient = Patient(**patient_info)
patient_detail(patient)