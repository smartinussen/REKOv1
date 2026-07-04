
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from fastapi import FastAPI

app = FastAPI()

class Farm(BaseModel):
    farm_name: str = Field(..., description="Name of the farm")
    farmer_manager: str = Field(..., description="Owners name")
    street: str = Field(..., description="Street address")
    city: str = Field(..., description="City or municipality")
    state_province: str = Field(..., description="State or province")
    postal_code: str = Field(..., description="Postal code")
    latitude: float | None = Field(None, ge=-90.0, le=90.0)
    longitude: float | None = Field(None, ge=-180.0, le=180.0)
    primary_phone: str = Field(..., description="Primary contact phone number")
    email: EmailStr = Field(..., description="Public contact email for the farm")
    website: HttpUrl | None = Field(None, description="Farm's website URL")
    description: str = Field("", description="A short bio or story about the farm")
    certifications: list[str] = Field(default=[], description="List of certifications (e.g., Organic, Demeter)")
    available_produce_categories: list[str] = Field(default=[], description="Categories of produce sold (e.g., Root vegetables, Berries)")
    reko_markets: list[str] = Field(...,description="Which REKO markets does the farm participate in")
    is_active: bool = Field(True, description="Whether the farm profile is currently active on the marketplace")


@app.get("/")
async def root():
    return {"message": "It's working"}

@app.post("/farms")
async def create_farm(farm: Farm):
    return farm