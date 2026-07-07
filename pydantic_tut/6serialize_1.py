from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address


def patient_detail(patient: Patient):
    print(patient.name)
    print(patient.gender)
    print(patient.age)
    print(patient.address.street)
    print(patient.address.city)
    print(patient.address.state)
    print(patient.address.zip_code)


# Create Address object
address_info = {"street": "123 Main St", "city": "New York", "state": "NY", "zip_code": "10001"}
address1 = Address(**address_info)

# Create Patient object
patient_info = {"name": "John Doe", "gender": "Male", "age": 30, "address": address1}
patient = Patient(**patient_info)

# Serialize - Different methods
temp_dict = patient.model_dump()
print(temp_dict)

temp1 = patient.model_dump(include={"name", "age"})
temp2 = patient.model_dump(exclude={"address"})
temp3 = patient.model_dump(include={"address"}, exclude={"address": {"zip_code"}})
temp4 = patient.model_dump(exclude_unset=True)  # shows only set fields, excluding defaults

print(temp3)
print(temp2)
print(temp1)

# temp_jason = patient.model_dump_json()
# print(temp_jason)

# patient_detail(patient)
# print(patient_info)
# print(patient.name)
# print(patient.address.street)
# print(patient.address.city)
