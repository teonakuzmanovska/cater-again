from pydantic import BaseModel, ConfigDict, Field, field_validator

class SupplierBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=50)
    description: str | None = None
    contact_phone: str | None = Field(default=None, max_length=32)
    contact_email: str | None = Field(default=None, max_length=254)

class SupplierCreate(SupplierBase):
    pass

class SupplierRead(SupplierBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    contact_phone: str | None = Field(default=None, max_length=32)
    contact_email: str | None = Field(default=None, max_length=254)

    @field_validator("name", "category")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Omit this field to leave it unchanged.")
        return value