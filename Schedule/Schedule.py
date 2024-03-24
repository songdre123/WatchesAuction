from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from flasgger import Swagger
from os import environ

# from db_config import set_database_uri

app = Flask(__name__)

CORS(app)

# path = "schedule"
# set_database_uri(app, path)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL") or "mysql+mysqlconnector://root:password@localhost:3306/Schedule"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SWAGGER"] = {
    "title": "Schedule microservice API",
    "version": 1.0,
    "openapi": "3.0.2",
    "description": "Allows create, retrieve, update, and delete schedule \n Gets schedule for specific auction, user \n Gets all schedules in specific time range,",
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
7. GET /schedule/date - Get all schedules in a date range, use query params of (start_date=YYYY-MM-DDT end_date=YYYY-MM-DD)

-- SQL Database creation code for Schedule

CREATE DATABASE IF NOT EXISTS Schedule;
USE Schedule;
CREATE TABLE Schedule (
    auction_id INT PRIMARY KEY,
    user_id INT,
    collection_date DATE
);
"""

db = SQLAlchemy(app)


class Schedule(db.Model):
    __tablename__ = "Schedule"
    __table_args__ = {"schema": "Schedule"}

    auction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    collection_date = db.Column(db.TIMESTAMP)

    def __init__(self, auction_id, user_id, collection_date=None):
        self.auction_id = auction_id
        self.user_id = user_id
        self.collection_date = collection_date

    def json(self):
        return {
            "auction_id": self.auction_id,
            "user_id": self.user_id,
            "collection_date": (
                self.collection_date.strftime("%Y-%m-%d")
                if self.collection_date
                else None
            ),
        }


# Create tables (including the 'Schedule' table in the 'Schedule' schema)
with app.app_context():
    db.create_all()


# Get all schedules
@app.route("/schedule", methods=["GET"])
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
@app.route("/schedule/create/<int:auction_id>", methods=["POST"])
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
        return (
            jsonify(
                {
                    "code": 400,
                    "message": f"Schedule with auction ID {auction_id} already exists.",
                }
            ),
            400,
        )

    new_schedule = Schedule(auction_id=auction_id, user_id=None, collection_date=None)

    db.session.add(new_schedule)

    try:
        db.session.commit()
        return (
            jsonify(
                {
                    "code": 201,
                    "data": new_schedule.json(),
                    "message": "Schedule created successfully",
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "code": 500,
                    "data": {"auction_id": auction_id},
                    "message": "An error occurred creating the schedule.",
                    "error": str(e),
                }
            ),
            500,
        )


# Edit schedule based on auction ID
@app.route("/schedule/edit/<int:auction_id>", methods=["PUT"])
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
                schema:
                    type: object
                    properties:
                        collection_date:
                            type: string
                            format: date
                            description: The scheduled date for collection (YYYY-MM-DD)
                        user_id:
                            type: integer
                            description: The ID of the user
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
        return (
            jsonify(
                {
                    "code": 404,
                    "message": f"No schedule found with auction ID {auction_id}",
                }
            ),
            404,
        )

    data = request.get_json()

    if data:
        collection_date_str = data.get("collection_date")

        if collection_date_str:
            try:
                collection_date = datetime.strptime(
                    collection_date_str, "%Y-%m-%d"
                ).date()
                schedule.collection_date = collection_date
            except ValueError:
                return (
                    jsonify(
                        {
                            "code": 400,
                            "message": "Invalid date format. Please use the format 'YYYY-MM-DD'",
                        }
                    ),
                    400,
                )

        user_id = data.get("user_id")
        if user_id is not None:
            schedule.user_id = user_id

        try:
            db.session.commit()
            return (
                jsonify(
                    {
                        "code": 200,
                        "data": schedule.json(),
                        "message": "Schedule updated successfully",
                    }
                ),
                200,
            )

        except Exception as e:
            db.session.rollback()
            return (
                jsonify(
                    {
                        "code": 500,
                        "data": {"auction_id": auction_id},
                        "message": "An error occurred while updating the schedule",
                        "error": str(e),
                    }
                ),
                500,
            )
    else:
        return (
            jsonify(
                {
                    "code": 400,
                    "message": "No data provided for update",
                }
            ),
            400,
        )


# Get schedule for a specific auction ID
@app.route("/schedule/<int:auction_id>", methods=["GET"])
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
    schedule = db.session.scalars(
        db.select(Schedule).filter_by(auction_id=auction_id).limit(1)
    ).first()

    # print(schedule.json())

    if not schedule:
        return (
            jsonify(
                {
                    "code": 404,
                    "message": f"No schedule found for auction ID {auction_id}",
                }
            ),
            404,
        )

    return jsonify({"code": 200, "data": schedule.json()})


# Delete schedule by auction ID
@app.route("/schedule/delete/<int:auction_id>", methods=["DELETE"])
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
        return (
            jsonify(
                {
                    "code": 404,
                    "message": f"No schedule found with auction ID {auction_id} to delete",
                }
            ),
            404,
        )

    db.session.delete(schedule)

    try:
        db.session.commit()
        return (
            jsonify(
                {
                    "code": 200,
                    "message": f"Schedule with auction ID {auction_id} deleted successfully",
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "code": 500,
                    "data": {"auction_id": auction_id},
                    "message": "An error occurred while deleting the schedule",
                    "error": str(e),
                }
            ),
            500,
        )


# Get all schedules for a specific user ID
@app.route("/schedule/user/<int:user_id>", methods=["GET"])
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
        return (
            jsonify(
                {
                    "code": 404,
                    "message": f"No schedules found for user ID {user_id}",
                }
            ),
            404,
        )

    schedule_list = [schedule.json() for schedule in schedules]
    return jsonify(schedule_list)


# Get all schedules in specific time range
@app.route("/schedule/date", methods=["GET"])
def get_schedules_within_date_range():
    """Get all schedules in a specific date range
    ---
    tags:
      - Schedule
    parameters:
      - name: start_date
        in: query
        type: string
        format: date
        required: true
        description: The start date of the date range YYYY-MM-DD
      - name: end_date
        in: query
        type: string
        format: date
        required: true
        description: The end date of the date range YYYY-MM-DD
    responses:
      200:
        description: Returns a list of schedules within the specified date range
      400:
        description: Invalid date format. Please use the format 'YYYY-MM-DD'
    """
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        return (
            jsonify(
                {
                    "code": 400,
                    "message": "Invalid date format. Please use the format 'YYYY-MM-DD'",
                }
            ),
            400,
        )

    schedules = (
        db.session.query(Schedule)
        .filter(
            Schedule.collection_date >= start_date, Schedule.collection_date <= end_date
        )
        .all()
    )

    schedule_list = [schedule.json() for schedule in schedules]
    return jsonify(schedule_list)


if __name__ == "__main__":
    app.run(port=5003, debug=True, host="0.0.0.0")
