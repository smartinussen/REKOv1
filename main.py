import json
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, HttpUrl

app = FastAPI()

def create_farm_table():
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

create_farm_table()

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

class FarmUpdate(BaseModel):
    farm_name: str | None = Field(None, description="Name of the farm")
    farm_manager: str | None = Field(None, description="Owners name")
    address: str | None = Field(None, description="Street address")
    city: str | None = Field(None, description="City or municipality")
    postal_code: str | None = Field(None, description="Postal code")
    latitude: float | None = Field(None, ge=-90.0, le=90.0)
    longitude: float | None = Field(None, ge=-180.0, le=180.0)
    phone_no: str | None = Field(None, description="Primary contact phone number")
    email: EmailStr | None = Field(None, description="Public contact email for the farm")
    website: HttpUrl | None = Field(None, description="Farm's website URL")
    description: str | None = Field(None, description="A short bio or story about the farm")
    certifications: list[str] | None = Field(None, description="List of certifications (e.g., Organic, Demeter)")
    produce_categories: list[str] | None = Field(None, description="Categories of produce sold (e.g., Root vegetables, Berries)")
    reko_markets: list[str] | None = Field(None, description="Which REKO markets does the farm participate in")
    is_active: bool | None = Field(None, description="Whether the farm profile is currently active on the marketplace")



def insert_farm(farm: Farm):
    conn = sqlite3.connect("reko.db")
    cursor = conn.execute(
        "INSERT INTO farms (farm_name, farm_manager, address, city, postal_code, latitude, longitude, phone_no, email, website, description, certifications, produce_categories, reko_markets, is_active) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (farm.farm_name,
         farm.farm_manager,
         farm.address,
         farm.city,
         farm.postal_code,
         farm.latitude,
         farm.longitude,
         farm.phone_no,
         farm.email,
         str(farm.website) if farm.website else None,
         farm.description,
         json.dumps(farm.certifications),
         json.dumps(farm.produce_categories),
         json.dumps(farm.reko_markets),
         int(farm.is_active)
         )
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def clear_farm_data(farm):
    farm["certifications"] = json.loads(farm["certifications"])
    farm["produce_categories"] = json.loads(farm["produce_categories"])
    farm["reko_markets"] = json.loads(farm["reko_markets"])
    farm["is_active"] = bool(farm["is_active"])
    return farm

def get_farms():
    conn = sqlite3.connect("reko.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        "SELECT * FROM farms"
         )
    rows = cursor.fetchall()
    conn.close()
    farms = [dict(row) for row in rows]
    for row in farms:
        clear_farm_data(row)
    return farms

def get_farm_by_id(farm_id: int):
    conn = sqlite3.connect("reko.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        "SELECT * FROM farms WHERE id = ?", (farm_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    farm = dict(row)
    clear_farm_data(farm)
    return farm


def update_farm(farm_id: int, updates: dict):
    conn = sqlite3.connect("reko.db")
    fields = ", ".join(f"{key} = ?" for key in updates)
    sql = f"UPDATE farms SET {fields}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
    converted = {}
    for key, value in updates.items():
        if key in ("certifications", "produce_categories", "reko_markets"):
            value = json.dumps(value)
        elif key == "website":
            value = str(value)
        elif key == "is_active":
            value = int(value)
        converted[key] = value
    values = list(converted.values())
    values.append(farm_id)
    cursor = conn.execute(sql, values)
    conn.commit()
    conn.close()
    return cursor.rowcount != 0

# Routes below
@app.get("/")
async def root():
    return {"message": "It's working"}

@app.post("/farms")
async def create_farm(farm: Farm):
    new_id = insert_farm(farm)
    return {"id": new_id, "farm": farm}

@app.get("/farms")
async def get_all_farms():
    all_farms = get_farms()
    return {"Farms": all_farms}

@app.get("/farms/{farm_id}")
async def get_farm(farm_id: int):
    farm = get_farm_by_id(farm_id)
    if farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    return {"id": farm_id, "farm": farm}

@app.patch("/farms/{farm_id}")
async def patch_farm(farm_id: int, updates: FarmUpdate):
    updates_dict = updates.model_dump(exclude_unset=True)
    success = update_farm(farm_id, updates_dict)
    if not success:
        raise HTTPException(status_code=404, detail="Farm not found")
    updated_farm = get_farm_by_id(farm_id)
    return {"message": "Farm updated.","Farm": updated_farm}