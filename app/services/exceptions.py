class ServiceError(Exception):
    status_code: int

    def __init__(self, detail: str):
        self.detail = detail


class ResourceNotFound(ServiceError):
    status_code = 404


class ResourceAlreadyExists(ServiceError):
    status_code = 409


class ResourceLinked(ServiceError):
    status_code = 409


class RelationshipConflict(ServiceError):
    status_code = 409
