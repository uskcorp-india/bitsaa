from enum import Enum

class Model(Enum):
    booking = "BOOKING"
    registration = "REGISTRATION"
    room = "ROOM"

class Operation(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"