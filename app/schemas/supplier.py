from app.schemas.base import RequestSchema, ResponseSchema


class SupplierFields:
    country: str | None = None
    contactTitle: str | None = None
    address: str | None = None
    city: str | None = None
    phone: str | None = None
    contactName: str | None = None
    companyName: str | None = None
    postalCode: str | None = None
    region: str | None = None
    fax: str | None = None
    homePage: str | None = None


class SupplierCreate(RequestSchema, SupplierFields):
    supplierID: str


class SupplierUpdate(RequestSchema, SupplierFields):
    pass


class SupplierResponse(ResponseSchema, SupplierFields):
    supplierID: str
