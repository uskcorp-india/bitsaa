import dao.reservation_dao as reservation_dao
import dao.registration_dao as registration_dao

# reservation process
def create_reservation(reservation: dict):
    return reservation_dao.create(reservation)

def update_reservation(reservation: dict):
    return reservation_dao.update(reservation)

def delete_reservation(reservation_id:str):
    return reservation_dao.delete(reservation_id)

def find_reservation(reservation_id:str):
    return reservation_dao.find(reservation_id)

#registration
def create_registration(registration:dict):
    return registration_dao.create(registration)

def update_registration(registration:dict):
    return registration_dao.update(registration)

def delete_registration(registration_id:str):
    return registration_dao.delete(registration_id)

def find_registration(registration_id:str):
    return  registration_dao.find(registration_id)