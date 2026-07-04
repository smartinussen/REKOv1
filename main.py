
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from fastapi import FastAPI
import sqlite3

def create_table():
    conn = sqlite3.connect("reko.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS farms (
            id INTEGER PRIMARY KEY,
            farm_name TEXT NOT NULL,
            farm_manager TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            phone_no TEXT NOT NULL,
            email TEXT NOT NULL,
            website TEXT,
            description TEXT,
            certifications TEXT,
            produce_categories TEXT,
            reko_markets TEXT,
            is_active INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

app = FastAPI()
create_table()

class Farm(BaseModel):
    farm_name: str = Field(..., description="Name of the farm")
    farm_manager: str = Field(..., description="Owners name")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City or municipality")
    postal_code: str = Field(..., description="Postal code")
    latitude: float | None = Field(None, ge=-90.0, le=90.0)
    longitude: float | None = Field(None, ge=-180.0, le=180.0)
    phone_no: str = Field(..., description="Primary contact phone number")
    email: EmailStr = Field(..., description="Public contact email for the farm")
    website: HttpUrl | None = Field(None, description="Farm's website URL")
    description: str = Field("", description="A short bio or story about the farm")
    certifications: list[str] = Field(default=[], description="List of certifications (e.g., Organic, Demeter)")
    produce_categories: list[str] = Field(default=[], description="Categories of produce sold (e.g., Root vegetables, Berries)")
    reko_markets: list[str] = Field(...,description="Which REKO markets does the farm participate in")
    is_active: bool = Field(True, description="Whether the farm profile is currently active on the marketplace")


@app.get("/")
async def root():
    return {"message": "It's working"}

@app.post("/farms")
async def create_farm(farm: Farm):
    return farm