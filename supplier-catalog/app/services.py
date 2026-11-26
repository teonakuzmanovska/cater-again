from app.models import Supplier
from app.schemas import SupplierCreate, SupplierUpdate
from sqlalchemy.orm import Session


def add_supplier(
    db: Session,
    supplier: SupplierCreate,
    company_id: str
):
    db_supplier = Supplier(company_id=company_id, **supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def get_suppliers(
    db: Session,
    company_id: str,
    offset: int = 0,
    limit: int = 100
):
    return (
        db.query(Supplier)
        .filter(Supplier.company_id == company_id)
        .order_by(Supplier.id)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_supplier_by_id(
    db: Session,
    supplier_id: int,
    company_id: str
):
    return (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id, Supplier.company_id == company_id)
        .one_or_none()
    )


def search_supplier_by_name(
    db: Session,
    name: str,
    company_id: str
):
    return (
        db.query(Supplier)
        .filter(
            Supplier.company_id == company_id,
            Supplier.name.icontains(name, autoescape=True),
        )
        .all()
    )


def update_supplier_by_id(
    db: Session,
    supplier_id: int,
    supplier: SupplierUpdate,
    company_id: str
):
    db_supplier = get_supplier_by_id(db, supplier_id, company_id)
    if db_supplier is None:
        return None

    for field, value in supplier.model_dump(exclude_unset=True).items():
        setattr(db_supplier, field, value)

    db.commit()
    db.refresh(db_supplier)
    return db_supplier