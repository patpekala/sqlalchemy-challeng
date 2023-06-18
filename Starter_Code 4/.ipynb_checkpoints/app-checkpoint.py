# Import the dependencies.
from flask import Flask

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime
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

########## Home Route that displays all available routes on the landing page 
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        
    )

########## Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns jsonified precipitation data for the last year in the database""" 
    # Find the most recent date in the data set.
    most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Query to retrieve the last 12 months of precipitation data 
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
    
    # Return jsonified data
    return jsonify(results)
    
########## Tobs Route 
@app.route("/api/v1.0/tobs")
def tobs():
    """Returns jsonified data for the most active station in the last year"""
    # Query to find the most active station
    num_stations = session.queryresult = session.query(Measurement.station, func.count()).group_by(Measurement.station).order_by(func.count().desc()).all()
    most_active = num_stations[0][0]
    
    # Query the last 12 months of temperature observation data for this station
    data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station==most_active).filter(Measurement.date>=one_year_ago).all()
   
    # Close session
    session.close()
    
    # Return jsonified data
    return jsonify(data)
    
########## Start Route 
@app.route("/api/v1.0/<start>")

########## Start/End Route 

@app.route("/api/v1.0/<start>/<end>")
