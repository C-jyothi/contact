
import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import Base, engine, get_db
from models import Contact
from schemas import ContactCreate, ContactResponse


# Create database tables if they do not exist.
Base.metadata.create_all(bind=engine)


# Create FastAPI application.
app = FastAPI()


# Allow React frontend to communicate with FastAPI.
frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

allowed_origins = [
    "http://localhost:5173",
    frontend_url
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


# --------------------------------
# API 1: ADD A CONTACT
# --------------------------------

@app.post("/contacts", response_model=ContactResponse)
def add_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):

    try:

        # Create a new contact object.
        new_contact = Contact(
            name=contact.name,
            email=str(contact.email),
            phone=contact.phone
        )

        # Save the contact.
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        return new_contact

    except SQLAlchemyError:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to save contact"
        )


# --------------------------------
# API 2: VIEW ALL CONTACTS
# --------------------------------

@app.get("/contacts", response_model=list[ContactResponse])
def get_contacts(db: Session = Depends(get_db)):

    try:

        contacts = db.query(Contact).all()

        return contacts

    except SQLAlchemyError:

        raise HTTPException(
            status_code=500,
            detail="Unable to get contacts"
        )


# --------------------------------
# API 3: DELETE A CONTACT
# --------------------------------

@app.delete("/contacts/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):

    try:

        # Find the contact using its ID.
        contact = db.query(Contact).filter(
            Contact.id == contact_id
        ).first()

        # Check whether the contact exists.
        if contact is None:

            raise HTTPException(
                status_code=404,
                detail="Contact not found"
            )

        # Delete the contact.
        db.delete(contact)
        db.commit()

        return {
            "message": "Contact deleted successfully"
        }

    except HTTPException:

        raise

    except SQLAlchemyError:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to delete contact"
        )
