import dao.reservation_dao as reservation_dao

# reservation process
def create_reservation(reservation: dict):
    return reservation_dao.create(reservation)

def update_reservation(reservation: dict):
    return reservation_dao.update(reservation)

def delete_reservation(reservation_id:str):
    return reservation_dao.delete(reservation_id)

def find_reservation(reservation_id:str):
    return reservation_dao.find(reservation_id)