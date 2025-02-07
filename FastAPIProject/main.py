import zoneinfo
from datetime import datetime

from fastapi import FastAPI

from models import Customer, Transaction, Invoice


app = FastAPI()


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


@app.post("/customers")
async def create_customer(customer_data: Customer):
    return customer_data

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoices(invoices_data: Invoice):
    return invoices_data