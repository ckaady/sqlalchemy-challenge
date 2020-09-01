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
        f"<a href='/api/v1.0/start_date/2017-01-01'>start_date/2017-01-01</a><br/>"
        f"<a href='/api/v1.0/start_and_end_dates/2017-01-01/2017-01-15'>start_and_end_dates/2017-01-01/2017-01-15</a><br/>"    

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



############ START DATE ############
@app.route("/api/v1.0/start_date/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the start date to retrieve TMIN,TAVG,TMAX for all dates greater and equal to start
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)



############ START DATE/END DATE ############
@app.route("/api/v1.0/start_and_end_dates/<start>/<end>")
def start_and_end_dates(start,end):

# Create our session (link) from Python to the DB
    session = Session(engine)

    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    # Query the start and end dates to retrieve TMIN,TAVG,TMAX for dates between and inclusive of those given
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

     # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)


if __name__ == '__main__':
    app.run(debug=True)

