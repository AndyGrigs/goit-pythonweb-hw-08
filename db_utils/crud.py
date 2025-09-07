from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_ , and_ ,extract
from db_utils.models import Contact
from db_utils.schemas import ContactCreate, ContactUpdate
from datetime import date, timedelta

def get_contact(db: Session, contact_id:int) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> Optional[Contact]:
    query = db.query(Contact)
    if search:
        search_filter = or_(
            Contact.first_name.ilike(f"%{search}%"),
            Contact.last_name.ilike(f"%{search}%"),
            Contact.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    return query.offset(skip).limit(limit).all()
    

def create_contact(db:Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db:Session, contact_id:int, contact_update: ContactUpdate) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return None
    update_data = contact_update.model_dump(exclude_unset=True)
    for field, value in update_contact.items():
        setattr(db_contact, field, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db:Session, contact_id:int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return False
    
    db.delete(db_contact)
    db.commit()
    return True
