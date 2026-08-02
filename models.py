from pydantic import BaseModel, EmailStr, Field, HttpUrl


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
    certifications: list[str] = Field(
        default=[], description="List of certifications (e.g., Organic, Demeter)"
    )
    produce_categories: list[str] = Field(
        default=[],
        description="Categories of produce sold (e.g., Root vegetables, Berries)",
    )
    reko_markets: list[str] = Field(
        ..., description="Which REKO markets does the farm participate in"
    )
    is_active: bool = Field(
        True,
        description="Whether the farm profile is currently active on the marketplace",
    )


class FarmUpdate(BaseModel):
    farm_name: str | None = Field(None, description="Name of the farm")
    farm_manager: str | None = Field(None, description="Owners name")
    address: str | None = Field(None, description="Street address")
    city: str | None = Field(None, description="City or municipality")
    postal_code: str | None = Field(None, description="Postal code")
    latitude: float | None = Field(None, ge=-90.0, le=90.0)
    longitude: float | None = Field(None, ge=-180.0, le=180.0)
    phone_no: str | None = Field(None, description="Primary contact phone number")
    email: EmailStr | None = Field(
        None, description="Public contact email for the farm"
    )
    website: HttpUrl | None = Field(None, description="Farm's website URL")
    description: str | None = Field(
        None, description="A short bio or story about the farm"
    )
    certifications: list[str] | None = Field(
        None, description="List of certifications (e.g., Organic, Demeter)"
    )
    produce_categories: list[str] | None = Field(
        None, description="Categories of produce sold (e.g., Root vegetables, Berries)"
    )
    reko_markets: list[str] | None = Field(
        None, description="Which REKO markets does the farm participate in"
    )
    is_active: bool | None = Field(
        None,
        description="Whether the farm profile is currently active on the marketplace",
    )
