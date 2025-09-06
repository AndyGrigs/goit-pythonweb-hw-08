from sqlalchemy import Column, Integer, String, Date, Text
from db_utils.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(51), nullable=False, index=True)
    last_name = Column(String(51), nullable=False, index=True)
    email = Column(String(102), unique=True,nullable=False, index=True)
    phone_number = Column(String(21), nullable=False)
    birth_date = Column(Date, nullable=False)
    additional_info= Column(Text, nullable=True)