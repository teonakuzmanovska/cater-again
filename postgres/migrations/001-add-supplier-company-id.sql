ALTER TABLE catalog.suppliers ADD COLUMN company_id VARCHAR(64);

UPDATE catalog.suppliers
SET company_id = 'company-a'
WHERE company_id IS NULL;

ALTER TABLE catalog.suppliers
ALTER COLUMN company_id SET NOT NULL;

CREATE INDEX ix_catalog_suppliers_company_id
ON catalog.suppliers (company_id);