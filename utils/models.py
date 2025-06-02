from enum import Enum

class Model(Enum):
    reservation = "RESERVATION"
    registration = "REGISTRATION"
    resort = "RESORT"

class Operation(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"