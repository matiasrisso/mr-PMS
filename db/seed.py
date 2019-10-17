from db.models import db, Hotel, HotelRooms
from db.enums import *

def seed_all():
    seed_hotels()
    seed_hotels_rooms()

def seed_hotels():
    # 1
    hotel = Hotel("The Tavern Hotel")
    db.session.add(hotel)
    # 2
    hotel = Hotel("The Resort Hotel")
    db.session.add(hotel)
    db.session.commit()

def seed_hotels_rooms():
    hotel_room = HotelRooms(1, RoomType.STANDARD_ROOM, 10)
    db.session.add(hotel_room)
    hotel_room = HotelRooms(1, RoomType.DELUXE_ROOM, 5)
    db.session.add(hotel_room)
    hotel_room = HotelRooms(1, RoomType.HONEYMOON_SUITE, 1)
    db.session.add(hotel_room)

    hotel_room = HotelRooms(2, RoomType.DELUXE_ROOM, 8)
    db.session.add(hotel_room)
    hotel_room = HotelRooms(2, RoomType.DELUXE_PRIVATE_POOL, 4)
    db.session.add(hotel_room)
    hotel_room = HotelRooms(2, RoomType.PRESIDENTIAL_SUITE, 1)
    db.session.add(hotel_room)
    db.session.commit()
