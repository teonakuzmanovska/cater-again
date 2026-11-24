from app.models import Supplier
from app.schemas import SupplierCreate, SupplierUpdate
from sqlalchemy.orm import Session


def add_supplier(db: Session, supplier: SupplierCreate):
    db_supplier = Supplier(**supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def get_suppliers(db: Session, offset: int = 0, limit: int = 100):
    return (
        db.query(Supplier)
        .order_by(Supplier.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

def get_supplier_by_id(db: Session, supplier_id: int):
    return db.get(Supplier, supplier_id)

def search_supplier_by_name(db: Session, name: str):
    return (
        db.query(Supplier)
        .filter(Supplier.name.icontains(name, autoescape=True))
        .all())

def update_supplier_by_id(db: Session, supplier_id: int, supplier: SupplierUpdate):
    db_supplier = get_supplier_by_id(db, supplier_id)
    if db_supplier is None:
        return None

    for field, value in supplier.model_dump(exclude_unset=True).items():
        setattr(db_supplier, field, value)

    db.commit()
    db.refresh(db_supplier)
    return db_supplier