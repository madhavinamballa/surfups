from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy import create_engine,func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import numpy as np
import datetime as dt
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#setting up Flask
app = Flask(__name__)
#Flask Routes
@app.route("/")
def welcome():
    return(
     f"Availabile Routes: <br/>"
     f"/api/v1.0/precipitation <br/>"
     f"/api/v1.0/stations <br/>"
     f"/api/v1.0/tobs <br/>"
     f"/api/v1.0/start<br/>"
     f"/api/v1.0/start/end<br/>"
     
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    #querying the precipitation data
    latest_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_twelve_months = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
    result=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=last_twelve_months).all()
    prcp_results=dict(result)
    return jsonify(prcp_results)
@app.route("/api/v1.0/stations")    
def station():
    #Return a JSON list of stations from the dataset
    results=session.query(Measurement.station).group_by(Measurement.station).all()
    station_results=list(np.ravel(results))
    return jsonify(station_results)
@app.route("/api/v1.0/tobs")    
def tobs():
    #query for the dates and temperature observations from a year from the last data point.
  # Return a JSON list of Temperature Observations (tobs) for the previous year.
    
    latest_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_twelve_months = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
    result=session.query(Measurement.tobs).filter(Measurement.date>=last_twelve_months).all()
    tobs_results=list(np.ravel(result))
    return jsonify(tobs_results)
    
@app.route("/api/v1.0")
@app.route("/api/v1.0/<start>")   
def start_date_tobs(start):
    start_date=dt.datetime.strptime(start, '%Y-%m-%d')
    result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    tobs_results=list(np.ravel(result))
    return jsonify(tobs_results)
   
@app.route("/api/v1.0")
@app.route("/api/v1.0/<start>/<end>")
def start_end_tobs(start,end):
    start_date=dt.datetime.strptime(start, '%Y-%m-%d')
    end_date=dt.datetime.strptime(end, '%Y-%m-%d')
    result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    tobs_results=list(np.ravel(result))
    return jsonify(tobs_results)
    
if __name__ == '__main__':
    app.run(debug=True)