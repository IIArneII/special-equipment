class ServiceError(Exception):
    ...

class NotFoundError(ServiceError):
    ...

class BadRequestError(ServiceError):
    ...


NOT_FOUND_ERR = NotFoundError('Not found')
