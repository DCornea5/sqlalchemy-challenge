## SQLAlchemy - Step 2 - Climate App
# import dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc
from flask import Flask, jsonify

import numpy as np

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# List all routes that are available.

# main route

@app.route("/")
def home():
    """List all available api routes."""
    return (
        
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"

        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

## Precipitation route
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
   # create session
       
    # code for one year results
    # results = session.query(Measurement.date, Measurement.prcp).\
    #filter(Measurement.date >= '2016-08-23').all()
    #results_d = {date: prcp for date, prcp in results}
    #return jsonify(results_d)

    results_all = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    results_all_d = {date: prcp for date, prcp in results_all}

    return jsonify(results_all_d)

# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
   # create session
       
    results_s = session.query(Station.station, Station.name).all()
    results__s_d = {station: name for station, name in results_s}

    return jsonify(results__s_d)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    results_t = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date>='2016-08-23').all()
    results__t_d = {date: tobs for date, tobs in results_t}
    return jsonify(results__t_d)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def start_only(start):
    results_from_start = session.query(func.min(Measurement.tobs),\
        func.avg(Measurement.tobs),\
        func.max(Measurement.tobs).\
        filter(Measurement.date>=start).all())
    
    return jsonify(results_from_start)




session.close()


    


if __name__ == '__main__':
    app.run(debug=True)