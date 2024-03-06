from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS  # Add this import
from flasgger import Swagger


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SWAGGER"] = {
    "title": "Schedule microservice API",
    "version": 1.0,
    "openapi": "3.0.2",
    "description": "Allows create, retrieve, update, and delete schedule \n Gets schedule for specific auction, user \n Gets all schedules in specific time range,"
}
swagger = Swagger(app)

"""
-- API Endpoints
1. GET /schedule - Get all schedules
2. POST /schedule/create/<int:auction_id> - Create a new schedule (planning to create once the auction has been created)
3. PUT /schedule/edit/<int:auction_id> - Edit schedule (edit after payment to fill in details)
4. DELETE /schedule/delete/<int:auction_id> - Delete schedule by auction ID
5. GET /schedule/<int:auction_id> - Get schedule for a specific auction ID
6. GET /schedule/user/<int:user_id> - Get all schedules for a specific user ID
7. GET /schedule/time - Get all schedules in a time range, use query params of (start_time=YYYY-MM-DD%20HH:MM:SS&end_time=YYYY-MM-DD%20HH:MM:SS)

-- SQL Database creation code for Schedule

CREATE TABLE Schedule (
    auction_id INT PRIMARY KEY,
    user_id INT,
    collection_time TIMESTAMP
);
"""

db = SQLAlchemy(app)

class Schedule(db.Model):
    __tablename__ = 'Schedule'

    auction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    collection_time = db.Column(db.TIMESTAMP)

    def __init__(self, auction_id, user_id, collection_time=None):
        self.auction_id = auction_id
        self.user_id = user_id
        self.collection_time = collection_time

    def json(self):
        return {
            'auction_id': self.auction_id,
            'user_id': self.user_id,
            'collection_time': self.collection_time.strftime('%Y-%m-%d %H:%M:%S') if self.collection_time else None
        }

# Create tables
# with app.app_context():
#     db.create_all()

# Get all schedules
@app.route('/schedule', methods=['GET'])
def get_schedule():

    """Get all schedules
        ---
        tags:
          - Schedule
        responses:
          200:
            description: Returns a list of all schedules

    """

    schedules = db.session.query(Schedule).all()
    schedule_list = [schedule.json() for schedule in schedules]
    return jsonify(schedule_list)

# Create a new schedule
@app.route('/schedule/create/<int:auction_id>', methods=['POST'])
def create_schedule(auction_id):
    """Create a new schedule
        ---
        tags:
          - Schedule
        parameters:
          - name: auction_id
            in: path
            type: integer
            required: true
            description: The ID of the auction for which to create a schedule
        responses:
          201:
            description: Schedule created successfully

          400:
            description: Schedule with the given auction ID already exists
        """

    existing_schedule = Schedule.query.filter_by(auction_id=auction_id).first()

    if existing_schedule:
        return jsonify({
            "code": 400,
            "message": f"Schedule with auction ID {auction_id} already exists."
        }), 400

    new_schedule = Schedule(
        auction_id=auction_id,
        user_id=None,
        collection_time=None
    )

    db.session.add(new_schedule)

    try:
        db.session.commit()
        return jsonify({
            "code": 201,
            "data": new_schedule.json(),
            "message": "Schedule created successfully"
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "data": {
                "auction_id": auction_id
            },
            "message": "An error occurred creating the schedule.",
            "error": str(e),
        }), 500


# Edit schedule based on auction ID
@app.route('/schedule/edit/<int:auction_id>', methods=['PUT'])
def edit_schedule(auction_id):
    """Edit schedule based on auction ID
    ---
    tags:
      - Schedule
    parameters:
      - name: auction_id
        in: path
        type: integer
        required: true
        description: The ID of the auction for which to edit the schedule
    requestBody: 
        required: true
        content:
            application/json:
                schma:
                    type: object
                    description: updated schedule data
    responses:
      200:
        description: Schedule updated successfully
      400:
        description: No data provided for update
      404:
        description: No schedule found with the given auction ID
      500:
        description: An error occurred while updating the schedule
    """
    schedule = db.session.query(Schedule).filter_by(auction_id=auction_id).first()

    if not schedule:
        return jsonify({
            "code": 404,
            "message": f"No schedule found with auction ID {auction_id}",
        }), 404

    data = request.get_json()

    if data:
        for key, value in data.items():
            setattr(schedule, key, value)

        try:
            db.session.commit()
            return jsonify({
                "code": 200,
                "data": schedule.json(),
                "message": "Schedule updated successfully",
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "code": 500,
                "data": {"auction_id": auction_id},
                "message": "An error occurred while updating the schedule",
                "error": str(e),
            }), 500
    else:
        return jsonify({
            "code": 400,
            "message": "No data provided for update",
        }), 400

# Get schedule for a specific auction ID
@app.route('/schedule/<int:auction_id>', methods=['GET'])
def get_schedule_for_auction(auction_id):
    """Get schedule for a specific auction ID
    ---
    tags:
      - Schedule
    parameters:
      - name: auction_id
        in: path
        type: integer
        required: true
        description: The ID of the auction for which to get the schedule
    responses:
      200:
        description: Returns the schedule for the given auction ID
      404:
        description: No schedule found for the given auction ID
    """
    schedules = db.session.query(Schedule).filter_by(auction_id=auction_id).all()

    if not schedules:
        return jsonify({
            "code": 404,
            "message": f"No schedule found for auction ID {auction_id}",
        }), 404

    schedule_list = [schedule.json() for schedule in schedules]
    return jsonify(schedule_list)

# Delete schedule by auction ID
@app.route('/schedule/delete/<int:auction_id>', methods=['DELETE'])
def delete_schedule(auction_id):
    """Delete schedule by auction ID
    ---
    tags:
      - Schedule
    parameters:
      - name: auction_id
        in: path
        type: integer
        required: true
        description: The ID of the auction for which to delete the schedule
    responses:
      200:
        description: Schedule deleted successfully
      404:
        description: No schedule found with the given auction ID to delete
      500:
        description: An error occurred while deleting the schedule
    """
    schedule = db.session.query(Schedule).filter_by(auction_id=auction_id).first()

    if not schedule:
        return jsonify({
            "code": 404,
            "message": f"No schedule found with auction ID {auction_id} to delete",
        }), 404

    db.session.delete(schedule)

    try:
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": f"Schedule with auction ID {auction_id} deleted successfully",
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "data": {"auction_id": auction_id},
            "message": "An error occurred while deleting the schedule",
            "error": str(e),
        }), 500

# Get all schedules for a specific user ID
@app.route('/schedule/user/<int:user_id>', methods=['GET'])
def get_schedules_for_user(user_id):
    """Get all schedules for a specific user ID
    ---
    tags:
      - Schedule
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user for which to get the schedules
    responses:
      200:
        description: Returns a list of schedules for the given user ID
      404:
        description: No schedules found for the given user ID
    """
    schedules = db.session.query(Schedule).filter_by(user_id=user_id).all()

    if not schedules:
        return jsonify({
            "code": 404,
            "message": f"No schedules found for user ID {user_id}",
        }), 404

    schedule_list = [schedule.json() for schedule in schedules]
    return jsonify(schedule_list)

# Get all schedules in specific time range
@app.route('/schedule/time', methods=['GET'])
def get_schedules_within_time_range():
    """Get all schedules in a specific time range
    ---
    tags:
      - Schedule
    parameters:
      - name: start_time
        in: query
        type: string
        required: true
        description: The start time of the time range (format: '%Y-%m-%d %H:%M:%S')
      - name: end_time
        in: query
        type: string
        required: true
        description: The end time of the time range (format: '%Y-%m-%d %H:%M:%S')
    responses:
      200:
        description: Returns a list of schedules within the specified time range
      400:
        description: Invalid date format. Please use the format '%Y-%m-%d %H:%M:%S'
    """
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')

    try:
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({
            "code": 400,
            "message": "Invalid date format. Please use the format '%Y-%m-%d %H:%M:%S'",
        }), 400

    schedules = db.session.query(Schedule).filter(
        Schedule.collection_time.between(start_time, end_time)
    ).all()

    schedule_list = [schedule.json() for schedule in schedules]
    return jsonify(schedule_list)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
