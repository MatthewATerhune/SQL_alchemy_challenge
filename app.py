import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
    return (
      f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/date/yyyy-mm-dd<br/>"
        f"/api/v1.0/date/yyyy-mm-dd/yyyy-mm-dd"
        )
        
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    year_recent = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   
    results = session.query(measurement.date, measurement.prcp, func.avg(measurement.prcp)).filter(measurement.date >= year_recent).group_by(measurement.date).all()

    session.close
    return jsonify(precipitation=results)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

   
    stations = session.query(station.station).all()

    session.close
    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_recent = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    results = session.query(measurement.date, measurement.tobs).filter(
        measurement.station == 'USC00519281').filter(measurement.date >= year_recent).all()

    session.close
    return jsonify(tobs=results)


@app.route("/api/v1.0/date/<start>")
@app.route("/api/v1.0/date/<start>/<end>")
def sttenddates(start=None, end=None):
    session = Session(engine)

    # SELECT Statement
    sel = [func.min(measurement.tobs), func.avg(
        measurement.tobs), func.max(measurement.tobs)]
    print(*sel)
    if not end:
        # calculate min, max, avg for dates greater than
        results = session.query(*sel).filter(measurement.date >= start).all()
    else:
        # calculate min, max, avg for dates-start and stop
        results = session.query(
            *sel).filter(measurement.date >= start).filter(measurement.date <= end).all()
    #convert to list
    temps = list(np.ravel(results))
    session.close
    return jsonify(temps=temps)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
   