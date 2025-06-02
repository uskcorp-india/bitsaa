from enum import Enum

class Model(Enum):
    book = "BOOKING"
    registration = "REGISTRATION"
    room = "ROOM"

class Operation(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"