from flask_sqlalchemy import SQLAlchemy
from db.enums import room_type_enum, reservation_status_enum

db = SQLAlchemy()

class Reservation(db.Model):
    __tablename__ = "t_reservation"
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('t_hotel.id'))
    room_type = db.Column(room_type_enum)
    arrival_date = db.Column(db.Date)
    departure_date = db.Column(db.Date)
    status = db.Column(reservation_status_enum)

    def __init__(self, hotel_id, room_type, arrival_date,
                 departure_date, status):
        self.hotel_id = hotel_id
        self.room_type = room_type
        self.arrival_date = arrival_date
        self.departure_date = departure_date
        self.status = status

    def serialize(self):
        return {
            'hotel_id': self.hotel_id,
            'room_type': self.room_type.value,
            'arrival_date': self.arrival_date,
            'departure_date': self.departure_date,
            'status': self.status.value,
        }


class HotelRooms(db.Model):
    __tablename__ = "r_hotel_rooms"
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('t_hotel.id'))
    room_type = db.Column(room_type_enum)
    quantity = db.Column(db.Integer)

    def __init__(self, hotel_id, room_type, quantity):
        self.hotel_id = hotel_id
        self.room_type = room_type
        self.quantity = quantity


class Hotel(db.Model):
    __tablename__ = "t_hotel"
    id = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.String(30))

    def __init__(self, hotel_name):
        self.hotel_name = hotel_name
