from flask import Blueprint
from flask import request
from flask import jsonify
from db.models import *
from datetime import datetime

routes_blueprint = Blueprint('routes', __name__,)


@routes_blueprint.route('/')
def home():
    return "Best-PMS-ever"


@routes_blueprint.route('/add_reservation', methods=['POST'])
def add_reservation():
    # Prepare data
    new_reservation = Reservation(request.args['hotel_id'],
                                  request.args['room_type'],
                                  datetime.strptime(request.args['arrival_date'], '%m-%d-%Y').date(),
                                  datetime.strptime(request.args['departure_date'], '%m-%d-%Y').date(),
                                  request.args['status'])
    db.session.add(new_reservation)
    db.session.commit()
    return "Reservation made"


@routes_blueprint.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    Reservation.query.filter_by(id=request.args['reservation_id']).delete()
    db.session.commit()
    return "Reservation canceled"


@routes_blueprint.route('/get_reservation', methods=['GET'])
def get_reservation():
    return jsonify(Reservation.query.filter_by(id=request.args['reservation_id'])
                   .first().serialize())


@routes_blueprint.route('/get_inventory_list', methods=['GET'])
def get_inventory_list():
    hotel_id = request.args['hotel_id']
    start_date = datetime.strptime(request.args['start_date']).date()
    end_date = datetime.strptime(request.args['end_date']).date()
    db.session.execute("""
        SELECT COUNT(), 
    """)
    # reservations_per_room_type = db.session.query.filter(Reservation.arrival_date > start_date,
    #                                                      Reservation.end_date < start_date,
    #                                                      Reservation.arrival_date > end_date,
    #                                                      Reservation.end_date < end_date)
    # .join()
    return jsonify(HotelRooms.query.all())
