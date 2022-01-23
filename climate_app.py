## SQLAlchemy - Step 2 - Climate App
# import dependencies

import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc
from flask import Flask, jsonify, render_template, request

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
        
        f"Welcome to the Hawaii Weather API!<br/><br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"Precipitation<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Stations<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature measurements most active station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"For minimum, maximum and averages from a starting date add the start date as yyyy-mm-dd to the following app<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"Add start and end date to the following app to find the minimum, average and maximum temperatures for a period.<br/>"
        f"Search example /api/v1.0/2016-08-23/2017-08-23<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

## Precipitation route
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():


    # version of code for one year results
    # results = session.query(Measurement.date, Measurement.prcp).\
    #filter(Measurement.date >= '2016-08-23').all()
    #results_d = {date: prcp for date, prcp in results}
    #return jsonify(results_d)

   # create session
    session = Session(engine) 

    # query measurement data
    results_all = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    
    # close session
    session.close()

    # get data in a dictionary
    results_all_d = {date: prcp for date, prcp in results_all}

    # jsonify the results
    return jsonify(results_all_d)

# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
   # create session and query the stations table
    session = Session(engine)  
    results_s = session.query(Station.station, Station.name).all()
    session.close()

    results__s_d = {station: name for station, name in results_s}

    return jsonify(results__s_d)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)  
    results_t = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date>='2016-08-23').all()
    session.close()    
    results__t_d = {date: tobs for date, tobs in results_t}
    return jsonify(results__t_d)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
       
    start_measurement = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()  
    temp_start = list(np.ravel(start_measurement))
    return jsonify(temp_start)

  
@app.route("/api/v1.0/<start>/<end>")


def start_end(start,end):
    session = Session(engine)  
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    start_end_measurement = session.query\
        (func.min(Measurement.tobs),\
        func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        all()

    session.close() 

    temp_start_end = list(np.ravel(start_end_measurement))

    return jsonify(temp_start_end)

if __name__ == '__main__':
    app.run(debug=True)