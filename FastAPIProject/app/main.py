import zoneinfo
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from sqlmodel import select

from models import Customer, Transaction, Invoice
from db import SessionDep, create_all_tables
from .routers import customers


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)

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



@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoices(invoices_data: Invoice):
    return invoices_data