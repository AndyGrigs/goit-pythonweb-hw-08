from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from db_utils import crud
from db_utils.database import get_db, engine
from db_utils.models import Base
from db_utils.schemas import ContactCreate, ContactResponce, ContactUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contact Manager API",
    description="REST API for contacts",
    version="1.0.0"
)


@app.post("/contacts", responce_model=ContactResponce, status_code=201)
def create_contact(contact: ContactCreate, db: Session=Depends(get_db)):
    try:
        return crud.create_contact(db=db, contact=contact)
    except Exception as e:
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=400, detail="Email is already in the system")
        raise HTTPException(status_code=400, detail="Error creating conract")
        
@app.get("/contacts", responce_model=List[ContactResponce])
def read_contacts(
    skip: int = Query(0, ge=0, description="Amout of queries for skipping"),
    limit: int = Query(100, ge=1, le=500, description="Max amount of records"),
    search: Optional[str] = Query(None, description="Search with a name or email"),
    db: Session = Depends(get_db)
):
    contacts = crud.get_contacts(db, skip=skip, limit=limit, search=search)
    return contacts

@app.get("/contacts/birthdays", responce_model=List[ContactResponce])
def read_upcomming_birthdays(db:Session = Depends(get_db)):
    contacts = crud.contacts_with_comming(db)
    return contacts

@app.get("/contacts/{contact_id}", responce_model=ContactResponce)
def read_contact(contact_id: int, db:Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(statuse_code=404, detail="Not found!")
    return db_contact

@app.put("/contacts/{contact_id}", responce_model=ContactResponce)
def update_contact(contact_id: int, contact_update:ContactUpdate, db:Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id=contact_id, update_contact=update_contact)
    if db_contact is None:
        raise HTTPException(statuse_code=404, detail="Not found!")
    return db_contact

@app.delete("/contacts/{contact_id}", responce_model=ContactResponce)
def delete_contact(contact_id: int, db:Session = Depends(get_db)):
    seccess = crud.delete_contact(db, contact_id=contact_id)
    if not seccess:
        raise HTTPException(statuse_code=404, detail="Not found!")
    return {"message": "Contact deleted!"}

@app.get("/")
def root():
    """Головна сторінка API"""
    return {
        "message": "Contact Management API", 
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
