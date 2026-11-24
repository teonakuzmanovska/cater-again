from app.database import get_db
from app.schemas import SupplierCreate, SupplierRead, SupplierUpdate
from app.services import (add_supplier, get_supplier_by_id, get_suppliers,
                          search_supplier_by_name, update_supplier_by_id)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("/create", response_model=SupplierRead, status_code=status.HTTP_201_CREATED)
def create_supplier(
    data: SupplierCreate, 
    db: Session = Depends(get_db)):
    return add_supplier(db, data)

@router.get("/list", response_model=list[SupplierRead])
def list_suppliers(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),):
    return get_suppliers(db, offset=offset, limit=limit)

@router.get("/search", response_model=list[SupplierRead])
def search_suppliers(
    name: str = Query(min_length=1, max_length=200),
    db: Session = Depends(get_db),):
    search_term = name.strip()
    if not search_term:
        raise HTTPException(status_code=422, detail="Search name cannot be blank")
    return search_supplier_by_name(db, search_term)

@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)):
    supplier = get_supplier_by_id(db, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.patch("/{supplier_id}", response_model=SupplierRead)
def update_supplier(
    supplier_id: int,
    data: SupplierUpdate,
    db: Session = Depends(get_db),):
    supplier = update_supplier_by_id(db, supplier_id, data)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier