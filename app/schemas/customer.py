from app.schemas.base import RequestSchema, ResponseSchema


class CustomerFields:
    country: str | None = None
    contactTitle: str | None = None
    address: str | None = None
    city: str | None = None
    phone: str | None = None
    contactName: str | None = None
    companyName: str | None = None
    postalCode: str | None = None
    fax: str | None = None
    region: str | None = None


class CustomerCreate(RequestSchema, CustomerFields):
    customerID: str


class CustomerUpdate(RequestSchema, CustomerFields):
    pass


class CustomerResponse(ResponseSchema, CustomerFields):
    customerID: str
