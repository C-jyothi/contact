
from pydantic import BaseModel, EmailStr, ConfigDict, Field


# Information received when adding a contact.
class ContactCreate(BaseModel):

    name: str = Field(min_length=1)
    email: EmailStr
    phone: str = Field(min_length=1)


# Information returned to the frontend.
class ContactResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    phone: str

    model_config = ConfigDict(from_attributes=True)
