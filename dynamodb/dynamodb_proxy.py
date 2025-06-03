import dao.reservation_dao as reservation_dao
import dao.registration_dao as registration_dao
import dao.resort_dao as resort_dao

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

#resort

def create_resort(resort:dict):
    return resort_dao.create(resort)

def update_resort(resort:dict):
    return resort_dao.update(resort)

def delete_resort(resort_id:str):
    return resort_dao.delete(resort_id)

def find_resort(resort_id:str):
    return  resort_dao.find(resort_id)

def find_all_resorts():
    return resort_dao.find_all()