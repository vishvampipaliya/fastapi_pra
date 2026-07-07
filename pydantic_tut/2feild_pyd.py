
from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import Optional,List,Dict,Annotated

class Patient(BaseModel):
    name:str
    age:int
    weight:float
    email:EmailStr
    married:bool
    allergies:List[str]
    contact_info:Dict[str,str]

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        vaild_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        domain = value.split("@")[-1]
        if domain not in vaild_domains:
            raise ValueError(f"Invalid email domain. Allowed domains are: {', '.join(vaild_domains)}")
        return value
    
    @field_validator("name",mode="before")#defult=after
    @classmethod
    def transform_name(cls, value):
        return value.upper()
     

def patient_detail(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)

patient_info={"name": "John Doe", "age": 30, "weight": 70.5, "email": "john.doe@gmail.com", "married": True, "allergies": ["penicillin"], "contact_info": {"email": "john.doe@hdfc.com"}}   
patient = Patient(**patient_info)
patient_detail(patient)