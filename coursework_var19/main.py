from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient  
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import nest_asyncio
import uvicorn

nest_asyncio.apply()

# ����������� ����������� � MongoDB
client = AsyncIOMotorClient("mongodb://192.168.226.132:27017/")
db = client["MAI_database"]
students_collection = db["students"]

# ������ Pydantic
class Students(BaseModel):
    surname: str
    group: str
    list_number: int
    password: str

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ����������� ����� ��� ��������� ����� ���������
@app.get("/students/form", response_class=HTMLResponse)
async def get_students_form(request: Request, error_message: str = ""):
    students = await students_collection.find({}, {"_id": 0}).to_list(None)  # ���������� �������� ���������
    return templates.TemplateResponse(
        "students_form.html",
        {
            "request": request,
            "students": students,
            "error_message": error_message,
        },
    )

# ����������� ����� ��� ���������� ��������
@app.post("/students/add")
async def add_students(
    request: Request,
    surname: str = Form(...),
    group: str = Form(...),
    list_number: int = Form(...),
    password: str = Form(...),
):
    try:
        # ���������, ���������� �� ������� � ������ �������
        existing_student = await students_collection.find_one({
            "surname": surname,
            "group": group,
            "list_number": list_number
        })
        
        if existing_student:
            raise ValueError("A student with such data already exists")

        existing_student_2 = await students_collection.find_one({
            "group": group,
            "list_number": list_number
        })
        
        if existing_student_2:
            raise ValueError("This list number already exists in the group")
        
        # ��������� ��������
        await students_collection.insert_one({
            "surname": surname,
            "group": group,
            "list_number": list_number,
            "password": password,
        })

        # ���� ������ �� API-�������, ���������� JSON-�����
        if request.headers.get("accept") == "application/json":
            return JSONResponse(content={"message": "Student added successfully"}, status_code=200)

        # ��� HTML-������� ���������� ������ ����� ��� ������
        return templates.TemplateResponse(
            "students_form.html",
            {
                "request": request,
                "students": await students_collection.find({}, {"_id": 0}).to_list(None),
                "error_message": None,
            },
            status_code=200,  # �������� ���
        )

    except ValueError as ve:
        error_message = str(ve)
        status_code = 400  # ��� ������ �������
    except Exception as e:
        error_message = f"Error: {str(e)}"
        status_code = 500  # ��� ���������� ������ �������

    # ���� ������ �� API-�������, ���������� JSON � �������
    if request.headers.get("accept") == "application/json":
        return JSONResponse(content={"error": error_message}, status_code=status_code)

    # ��� HTML-������� ���������� ������ � ������� � ������-�����
    return templates.TemplateResponse(
        "students_form.html",
        {
            "request": request,
            "students": await students_collection.find({}, {"_id": 0}).to_list(None),
            "error_message": error_message,
        },
        status_code=status_code,  # ������������� ��������������� ������-���
    )

@app.post("/students/delete_all")
async def delete_all_students(request: Request):
    try:
        # ������� ��� ��������� �� ��������� ���������
        result = await students_collection.delete_many({})

        if result.deleted_count == 0:
            raise ValueError("No students found to delete")

        # ���� ������ �� API-�������, ���������� JSON-�����
        if request.headers.get("accept") == "application/json":
            return JSONResponse(content={"message": "All students deleted successfully"}, status_code=200)

        # ��� HTML-������� ���������� ����������� �����
        return templates.TemplateResponse(
            "students_form.html",
            {
                "request": request,
                "students": [],
                "error_message": None,
            },
            status_code=200,  # �������� ���
        )

    except ValueError as ve:
        error_message = str(ve)
        status_code = 400  # ��� ������ �������
    except Exception as e:
        error_message = f"Error: {str(e)}"
        status_code = 500  # ��� ���������� ������ �������

    # ���� ������ �� API-�������, ���������� JSON � �������
    if request.headers.get("accept") == "application/json":
        return JSONResponse(content={"error": error_message}, status_code=status_code)

    # ��� HTML-������� ���������� ������ � �������
    return templates.TemplateResponse(
        "students_form.html",
        {
            "request": request,
            "students": await students_collection.find({}, {"_id": 0}).to_list(None),
            "error_message": error_message,
        },
        status_code=status_code,  # ������������� ��������������� ������-���
    )

@app.post("/students/delete")
async def delete_students(
    request: Request,
    surname: str = Form(...),
    group: str = Form(...),
    list_number: int = Form(...),
    search_value: str = Form(None),  # �������� ��������� ������
    search_field: str = Form(None)   # �������� ��������� ������
):
    try:
        # �������� ������� ��������
        result = await students_collection.delete_one({
            "surname": surname,
            "group": group,
            "list_number": list_number
        })
        
        if result.deleted_count == 0:
            raise ValueError("Student not found")

        # ���� ������ �� API-�������, ���������� JSON-�����
        if request.headers.get("accept") == "application/json":
            return JSONResponse(content={"message": "Student deleted successfully"}, status_code=200)

        # ����� �������� ��������� ����� � ���� �� �����������
        query = {
            search_field: {"$regex": search_value, "$options": "i"}
        } if search_value else {}
        
        students = await students_collection.find(query, {"_id": 0}).to_list(None)

        # ���������� ������ � ������������ ������ ����� ��������
        return templates.TemplateResponse(
            "students_form.html",
            {
                "request": request,
                "students": students,
                "error_message": None,
                "search_value": search_value,  # �������� ��������� ������ �������
                "search_field": search_field,  # �������� ��������� ������ �������
            },
            status_code=200,  # �������� ���
        )

    except ValueError as ve:
        error_message = str(ve)
        status_code = 400  # ��� ������ �������
    except Exception as e:
        error_message = f"Error: {str(e)}"
        status_code = 500  # ��� ���������� ������ �������

    # ���� ������ �� API-�������, ���������� JSON � �������
    if request.headers.get("accept") == "application/json":
        return JSONResponse(content={"error": error_message}, status_code=status_code)

    # ��� HTML-������� ���������� ������ � �������
    return templates.TemplateResponse(
        "students_form.html",
        {
            "request": request,
            "students": await students_collection.find({}, {"_id": 0}).to_list(None),
            "error_message": error_message,
        },
        status_code=status_code,  # ������������� ��������������� ������-���
    )

    # ����������� ����� ��� ������ ���������
@app.get("/students/search")
async def search_students(request: Request, search_value: str = "", search_field: str = "surname"):
    try:
        # ������ ��� ������ �� ��������� (�������������������)
        query = {
            search_field: {"$regex": search_value, "$options": "i"} 
        } if search_value else {}
        # ��������� ������ ���������, ��������������� �������
        students = await students_collection.find(query, {"_id": 0}).to_list(None)
         # ���� ��������� �� �������
        if not students:
            raise ValueError("No students found matching your search criteria")
        # ���� ������ �� API-�������, ���������� JSON-����� � ������������ ������
        if request.headers.get("accept") == "application/json":
            return JSONResponse(content={"students": students}, status_code=200)

        # ��� HTML-������� ���������� ������ � ������������ ������
        return templates.TemplateResponse(
            "students_form.html",
            {
                "request": request,
                "students": students,
                "error_message": None,
                "search_value": search_value,
                "search_field": search_field,
            },
            status_code=200,  # �������� ���
        )
    
    except Exception as e:
        error_message = f"Error: {str(e)}"
        status_code = 404 # ��� ���������� ������ �������

        # ���� ������ �� API-�������, ���������� JSON � �������
        if request.headers.get("accept") == "application/json":
            return JSONResponse(content={"error": error_message}, status_code=status_code)

        # ��� HTML-������� ���������� ������ � �������
        return templates.TemplateResponse(
            "students_form.html",
            {
                "request": request,
                "students": students,
                "error_message": error_message,
            },
            status_code=status_code,  # ������������� ��������������� ������-���
        )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)