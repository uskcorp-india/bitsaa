import dao.booking_dao as booking_dao

# booking process
def create_booking(booking: dict):
    return booking_dao.create(booking)

def update_booking(booking: dict):
    return booking_dao.update(booking)

def delete_booking(booking_id:str):
    return booking_dao.delete(booking_id)

def find_booking(booking_id:str):
    return booking_dao.find(booking_id)