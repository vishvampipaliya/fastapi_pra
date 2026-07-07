from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address: Address

def patient_detail(patient: Patient):
    print(patient.name)
    print(patient.gender)
    print(patient.age)
    print(patient.address.street)
    print(patient.address.city)
    print(patient.address.state)
    print(patient.address.zip_code)

address_info = {"street": "123 Main St", "city": "New York", "state": "NY", "zip_code": "10001"}    
address1 = Address(**address_info)

patient_info = {"name": "John Doe", "gender": "Male", "age": 30, "address": address1}
patient = Patient(**patient_info)
# patient_detail(patient)
print(patient_info)
print(patient.name)
print(patient.address.street)
print(patient.address.city)


