
from sqlalchemy import Column, Integer, String

from database import Base


# Creates the contacts table.
class Contact(Base):

    __tablename__ = "contacts"

    # Unique ID for every contact.
    id = Column(Integer, primary_key=True, index=True)

    # Contact name.
    name = Column(String, nullable=False)

    # Contact email.
    email = Column(String, nullable=False)

    # Contact phone number.
    phone = Column(String, nullable=False)
