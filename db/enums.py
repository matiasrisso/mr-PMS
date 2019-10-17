from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum


class RoomType(Enum):
    STANDARD_ROOM = 1
    DELUXE_ROOM = 2
    HONEYMOON_SUITE = 3
    DELUXE_PRIVATE_POOL = 4
    PRESIDENTIAL_SUITE = 5


room_type_enum = ENUM(RoomType, name="room type")


class ReservationStatus(Enum):
    ACTIVE = 1
    CANCELLED = 2


reservation_status_enum = ENUM(ReservationStatus, name="status")
