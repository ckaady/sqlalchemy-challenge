# import dependencies

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
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

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>Temperature Observation Data</a><br/>"
        f"Use yyyy-mm-dd format when entering date in URLs below:<br/>"
        f"<a href='/api/v1.0/temp/<start>'>Start Date</a><br/>"
        f"<a href='/api/v1.0/temp/<start>/<end>'>Start Date / End Date</a><br/>"

    )



########### PRECIPITATION ###########
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the precipitation data of the last twelve months including date and prcp values """
   # Query measurements for the past 12 months
    date = dt.datetime(2016, 8, 22)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date).order_by(Measurement.date).all()


    session.close()

    # Create dictionary from row data and append to list (year_prcp) 
    year_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        year_prcp.append(prcp_dict)

    return jsonify(year_prcp)



########### STATIONS ###########
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list(good practice to close session/housekeeping) 
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



############ TOBS ############
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs from the most active station for the previous year"""
    # Query all stations
    date = dt.datetime(2016, 8, 23)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station =='USC00519281').filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').order_by(Measurement.date).all()

    session.close()
   
    # Convert list of tuples into normal list(good practice to close session/housekeeping) 
    tobs = list(np.ravel(results))
  
    return jsonify(tobs)



############ START AND START DATE/END DATE############
# @app.route("/api/v1.0/<start>")
# @app.route("/api/v1.0/<start>/<end>")



if __name__ == '__main__':
    app.run(debug=True)

