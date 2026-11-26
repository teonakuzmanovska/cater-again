from app.database import Base
from sqlalchemy import Column, Integer, String, Text

class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = {"schema": "catalog"}

    id = Column(Integer, primary_key=True)
    company_id = Column(String(64), nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(50), nullable=False)
    contact_email = Column(String(254))
    contact_phone = Column(String(32))