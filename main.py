from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import db_utils.crud
from db_utils.database import get_db, engine
from db_utils.models import Base
from db_utils.schemas import ContactCreate, ContactResponce, ContactUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contact Manager API",
    description="REST API for contacts",
    version="1.0.0"
)


