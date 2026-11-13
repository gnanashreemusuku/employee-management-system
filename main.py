from fastapi import FastAPI
from pydantic import BaseModel

from database import SessionLocal, engine, Base
from models import Employee

Base.metadata.create_all(bind=engine)

app = FastAPI()


class EmployeeCreate(BaseModel):
    emp_id: int
    name: str
    salary: float


class EmployeeUpdate(BaseModel):
    name: str
    salary: float


# CREATE
@app.post("/employee")
def create_employee(employee: EmployeeCreate):

    db = SessionLocal()

    db_employee = Employee(
        emp_id=employee.emp_id,
        name=employee.name,
        salary=employee.salary
    )

    db.add(db_employee)
    db.commit()
    db.close()

    return {"message": "Employee created successfully"}


# GET ALL
@app.get("/employees")
def get_employees():

    db = SessionLocal()

    employees = db.query(Employee).all()

    db.close()

    return employees


# GET BY ID
@app.get("/employee/{emp_id}")
def get_employee(emp_id: int):

    db = SessionLocal()

    employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()

    db.close()

    return employee


# UPDATE
@app.put("/employee/{emp_id}")
def update_employee(emp_id: int, employee: EmployeeUpdate):

    db = SessionLocal()

    db_employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()

    if db_employee is None:
        db.close()
        return {"message": "Employee not found"}

    db_employee.name = employee.name
    db_employee.salary = employee.salary

    db.commit()
    db.close()

    return {"message": "Employee updated successfully"}


# DELETE
@app.delete("/employee/{emp_id}")
def delete_employee(emp_id: int):

    db = SessionLocal()

    db_employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()

    if db_employee is None:
        db.close()
        return {"message": "Employee not found"}

    db.delete(db_employee)
    db.commit()
    db.close()

    return {"message": "Employee deleted successfully"}