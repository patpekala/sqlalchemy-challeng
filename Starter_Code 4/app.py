# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime
import numpy as np
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

########## Home Route 
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f" Enter start_date in YYYY-MM-DD format: /api/v1.0/start_date<br/>"
        f"Enter start_date and end_date in YYYY-MM-DD format: /api/v1.0/start_date/end_date<br/>"
        
    )

########## Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns jsonified precipitation data for the last year in the database""" 
    # Find the most recent date in the data set.
    most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Query to retrieve the last 12 months of precipitation data 
    date_string = most_recent[0]
    date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    one_year_ago = date_object - datetime.timedelta(days=365)
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=one_year_ago).all()
    
    # Close session
    session.close()
    
    # Convert results to dictionary
    results = dict(data)
    
    # Return jsonified data
    return jsonify(results)

########## Stations Route:
@app.route("/api/v1.0/stations")
def stations():
    """Returns jsonified data of all of the stations in the database""" 
    # Query to retrieve all the stations
    results = session.query(Station.station).all()
   
    # Close session
    session.close()

    # Convert list of tuples into a normal list
    all_stations = list(np.ravel(results))
    
    # Return jsonified data
    return jsonify(all_stations)
    
########## Tobs Route 
@app.route("/api/v1.0/tobs")
def tobs():
    """Returns jsonified data for the most active station in the last year"""
    # Query to find the most active station
    num_stations = session.query(Measurement.station, func.count()).group_by(Measurement.station).order_by(func.count().desc()).all()
    most_active = num_stations[0][0]
    
    # Query the last 12 months of temperature observation data for this station
    most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date_string = most_recent[0]
    date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    one_year_ago = date_object - datetime.timedelta(days=365)
    data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station==most_active).filter(Measurement.date>=one_year_ago).all()
   
    # Close session
    session.close()

    # Create a dictionary from the row data and append to a list of all_observations 
    all_observations = []
    for date, tobs in data:
        results_dict = {}
        results_dict["date"] = date
        results_dict["tobs"] = tobs
        all_observations.append(results_dict)

    # Return jsonified data
    return jsonify(all_observations)
    
########## Start Route 
@app.route("/api/v1.0/<start>")
def start(start):
    """Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset"""

    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    # Close session
    session.close()

    # Create a dictionary from the row data and append to a list of all_observations 
    all_observations = []
    for min, max, avg in temps:
        results_dict = {}
        results_dict["min"] = min
        results_dict["max"] = max
        results_dict["average"] = avg
        all_observations.append(results_dict)

    # Return data
    return all_observations
    
########## Start/End Route 
@app.route("/api/v1.0/<start>/<end>")
def start_to_end(start, end):
    """Returns the min, max, and average temperatures calculated from the given start date to the  given end date"""
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),    func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <=    end).all()
    
    # Close session
    session.close()
    
    # Create a dictionary from the row data and append to a list of all_observations 
    all_observations = []
    for min, max, avg in temps:
        results_dict = {}
        results_dict["min"] = min
        results_dict["max"] = max
        results_dict["average"] = avg
        all_observations.append(results_dict)

    # Return data
    return all_observations

if __name__ == '__main__':
    app.run(debug=True)