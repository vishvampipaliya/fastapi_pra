# FastAPI Patient API

Simple FastAPI tutorial project for managing patient records.

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn

## Project Files

- main.py: FastAPI app and routes
- patients.json: local data store for patient records

## Setup

1. Create or use the virtual environment in this project.
2. Activate environment on Windows PowerShell:

```powershell
.\myenv\Scripts\Activate.ps1
```

3. Install dependencies if needed:

```powershell
pip install fastapi uvicorn
```

## Run Server

```powershell
uvicorn main:app --reload
```

Server will run at:

- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## API Endpoints

- GET / : health/root response
- GET /patients : list all patients
- GET /patients/{patient_id} : get one patient by id
- GET /sorted_patients?sort_by=age&sort_order=asc : sorted patient list
- POST /create_patient : create a new patient

## Example Create Request

```json
{
  "id": "p011",
  "name": "Test User",
  "age": 33,
  "gender": "Male",
  "condition": "Flu",
  "weight": 72,
  "height": 178
}
```

## Troubleshooting

### 1) Internal Server Error on /openapi.json or /docs

- Check Pydantic field definitions in main.py.
- In Pydantic v2, examples must be lists, not single values.

  Correct:

  ```python
  examples=["p001"]
  ```

  Wrong:

  ```python
  examples="p001"
  ```

- For string fields, use min_length and max_length instead of numeric constraints like lt or gt.

### 2) Error while starting Uvicorn (could not import module)

- Use the correct app path from this project root:

  ```powershell
  uvicorn main:app --reload
  ```

- If you run uvicorn app:main --reload by mistake, startup can fail depending on file names.

### 3) Port already in use

- Run on another port:

  ```powershell
  uvicorn main:app --reload --port 8001
  ```

### 4) 422 Unprocessable Entity on POST /create_patient

- Ensure request body is valid JSON and all required fields exist:
  - id
  - name
  - age
  - gender
  - condition
  - weight
  - height
- Ensure gender value is exactly Male or Female.
- Ensure age, weight, and height are positive values.

### 5) Data not saved or patient not found

- Confirm patients.json exists in the project root.
- Confirm server is started from the same folder where main.py and patients.json are located.
- If JSON file is malformed, fix it to valid JSON format and restart server.

### 6) Virtual environment activation issues (PowerShell)

- Activate environment:

  ```powershell
  .\myenv\Scripts\Activate.ps1
  ```

- If script execution is blocked, run PowerShell as administrator once and allow local scripts:

  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
