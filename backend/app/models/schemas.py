from pydantic import BaseModel, Field

class CarMetadata(BaseModel):
    user_id: str = Field(..., description="Dealer's user ID")
    platform: str = Field(..., description="Target platform: OLX/Cars24/etc")
    mileage: int | None = None
    ownership: int | None = Field(None, ge=1, le=5, description="Number of previous owners")
    year: int | None = Field(None, ge=1950, le=2024)