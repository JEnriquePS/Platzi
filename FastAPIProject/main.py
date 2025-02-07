import zoneinfo
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from sqlmodel import select

from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep, create_all_tables

app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"message": "Hello Worlds"}

country_timezones = {
    "US": "America/New_York",
    "UK": "Europe/London",
    "DE": "Europe/Berlin",
    "FR": "Europe/Paris",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

db_customers: list[Customer] = []


@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@app.get("/customers", response_model=list[Customer])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Customer not found")
    return customer_db


@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Customer not found")
    session.delete(customer_db)
    session.commit()
    return {"detail": "Customer deleted"}


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoices(invoices_data: Invoice):
    return invoices_data