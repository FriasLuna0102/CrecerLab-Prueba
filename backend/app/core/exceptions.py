from fastapi import HTTPException, status

class DatabaseError(HTTPException):
    def __init__(self, detail: str = "Error de base de datos"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class DuplicatedError(HTTPException):
    def __init__(self, detail: str = "Recurso duplicado"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class ValidationError(HTTPException):
    def __init__(self, detail: str = "Error de validación"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)