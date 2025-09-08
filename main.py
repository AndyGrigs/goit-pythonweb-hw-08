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
    search: Optional[str] = Query(None, description="Search with a name or email")
    db: Session = Depends(get_db)
):