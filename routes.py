import copy
from datetime import datetime, timedelta
from sqlalchemy import exc
from flask import Blueprint, request, jsonify
from db.models import *
from db.enums import ReservationStatus


routes_blueprint = Blueprint('routes', __name__, )


@routes_blueprint.route('/')
def home():
    return "Best-PMS-ever"


@routes_blueprint.route('/add_reservation', methods=['POST'])
def add_reservation():
    # Prepare data
    new_reservation = Reservation(request.args['hotel_id'],
                                  request.args['room_type'],
                                  datetime.strptime(request.args['arrival_date'], '%d-%m-%Y').date(),
                                  datetime.strptime(request.args['departure_date'], '%d-%m-%Y').date(),
                                  ReservationStatus.ACTIVE)
    # Reservation made only in the future
    # Considering that today can be reserved instantly
    if new_reservation.arrival_date < datetime.today().date():
        return "Reservation can not be made in the past", 400
    # Departure date always after arrival date
    if new_reservation.departure_date < new_reservation.arrival_date:
        return "Departure date must always be set to after arrival date", 400

    db.session.add(new_reservation)
    try:
        db.session.commit()
        return "Reservation made", 201
    except exc.IntegrityError as e:
        return "No such hotel exists", 404
    except exc.SQLAlchemyError as e:
        return jsonify(e.args), 400


@routes_blueprint.route('/cancel_reservation', methods=['PUT'])
def cancel_reservation():
    res = Reservation.query.filter_by(id=request.args['reservation_id']).first()

    if res is None:
        return "No such reservation exists", 404

    try:
        res.status = ReservationStatus.CANCELLED
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return jsonify(e.args), 400
    return "Reservation {} canceled".format(request.args['reservation_id']), 200


@routes_blueprint.route('/delete_reservation', methods=['DELETE'])
def delete_reservation():
    res = Reservation.query.filter_by(id=request.args['reservation_id']).first()
    if res is None:
        return "No such reservation exists", 404

    Reservation.query.filter_by(id=request.args['reservation_id']).delete()
    db.session.commit()
    return "Reservation {} deleted".format(request.args['reservation_id']), 200


@routes_blueprint.route('/get_reservation', methods=['GET'])
def get_reservation():
    res = Reservation.query.filter_by(id=request.args['reservation_id']).first()

    if res is None:
        return "No such reservation exists", 400
    return jsonify(res.serialize()), 200


@routes_blueprint.route('/get_inventory_list', methods=['GET'])
def get_inventory_list():
    # Prepare data
    hotel_id = request.args['hotel_id']
    start_date = datetime.strptime(request.args['start_date'], '%d-%m-%Y').date()
    end_date = datetime.strptime(request.args['end_date'], '%d-%m-%Y').date()

    # Gets available and occupied rooms by given hotel per day (by given range) per room type
    result = db.session.execute("""
        SELECT d.date, t.available_quantity, t.occupied_quantity, t.quantity, t.room_type
          FROM (SELECT to_char(date_trunc('day', ((:start_date - INTERVAL '1 day')::date + offs + 1)), 'YYYY-MM-DD') AS date 
                  FROM generate_series(0, (:end_date-:start_date), 1) AS offs
               ) d 
          LEFT OUTER JOIN ( SELECT DISTINCT res.as_of_date,
                                            (r_hotel_rooms.quantity - res.occupied) AS available_quantity,
                                            res.occupied AS occupied_quantity,
                                            r_hotel_rooms.quantity,
                                            r_hotel_rooms.room_type
		                      FROM r_hotel_rooms
		                      LEFT OUTER JOIN ( SELECT room_type, as_of_date, COUNT(t_reservation.id) occupied
							                      FROM (SELECT d::date AS as_of_date
									                      FROM generate_series(:start_date, :end_date, '1 day'
									                   ) AS d
									          ) dates
                                                  LEFT JOIN t_reservation
                                                    ON dates.as_of_date BETWEEN arrival_date AND departure_date
							                     WHERE t_reservation.hotel_id = :hotel_id
							                       AND t_reservation.status = 'ACTIVE'
							                     GROUP BY as_of_date, room_type ORDER BY as_of_date,room_type) AS res
			                    ON r_hotel_rooms.room_type = res.room_type
		                     WHERE r_hotel_rooms.hotel_id = :hotel_id
		                     ORDER BY res.as_of_date
	                      ) as t
            ON d.date = to_char(date_trunc('day', t.as_of_date), 'YYYY-MM-DD') 
         GROUP BY d.date,
                  t.available_quantity,
                  t.occupied_quantity,
                  t.quantity,
                  t.room_type,
                  t.as_of_date
    """, {"hotel_id": hotel_id, "start_date": start_date, "end_date": end_date})

    # Default hotel's room layout for un-reserved days
    hotels_result = db.session.execute("""
        SELECT * from r_hotel_rooms 
        WHERE r_hotel_rooms.hotel_id = :hotel_id
    """, {"hotel_id": hotel_id})

    if hotels_result.rowcount == 0:
        return "No such hotel exists", 404

    hotel_default = {}
    for h in hotels_result:
        hotel_default[h['room_type']] = {
            'available_rooms': h['quantity'],
            'occupied_rooms': 0
        }

    # Going over given dates and setting and replacing default hotel's layout
    # with the counted occupied and available rooms per room type
    dates_dict = {}
    for r in result:
        key = r['date']
        room_type = r['room_type']
        try:
            dates_dict[key] is None
        except:
            dates_dict[key] = copy.deepcopy(hotel_default)

        if room_type is not None:
            dates_dict[key][room_type]['available_rooms'] = r['available_quantity']
            dates_dict[key][room_type]['occupied_rooms'] = r['occupied_quantity']

    return jsonify(dates_dict), 200
