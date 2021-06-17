import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
#################################################

# create the engines
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# bases
Base = automap_base()
#Reflect the tables 
Base.prepare(engine, reflect=True)

# create into a table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
#################################################
app = Flask(__name__)

# Flask Routes
#################################################

@app.route("/")
def ALOHA():
    """List all available api routes."""
    return (
        
        f"<h1>ALOHA!!!</h1></br>"
        f"<h2>This API is for Climate Data in Hawaii</h2></br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"/api/v1.0/start_date</br>"
        f"/api/v1.0/start_date/end_date"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
        session = Session(engine)

        """Return precipitation data"""
        results = session.query(Measurement.date, Measurement.prcp).all()

        session.close()

    # # Convert into Tuple list
        return jsonify(dict(results))

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of stations and station names"""
    results = session.query(Station.station, Station.name).join(Measurement, Station.station == Measurement.station)

    session.close()

    return jsonify(dict(results))

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temperature observations from the most active station for the most recent one-year period"""
    
    # find the most recent date in the data set.
    most_recent_date_set = session.query(func.max(Measurement.date)).first()[0]

    # convert string date to datetime date
    most_recent_date_set = dt.datetime.strptime(most_recent_date_set, "%Y-%m-%d").date()
    
    """Return min, max, and average temperatures after specifified date"""
    # Format start date as datetime date
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    
    # Query data
    results = session.query(func.max(Measurement.tobs).label('temp_max'), func.min(Measurement.tobs).label('temp_min'), func.avg(Measurement.tobs).label('temp_avg')).filter(Measurement.date >= start_date).all()

    session.close()

    

@app.route("/api/v1.0/<start>")
def summarize_temp_after_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # find the most recent date in the data set.
    most_recent_date_set = session.query(func.max(Measurement.date)).first()[0]

    # convert string date to datetime date
    most_recent_date_set = dt.datetime.strptime(most_recent_date_str, "%Y-%m-%d").date()

    """Return min, max, and average temperatures after specifified date (inclusive)"""
    #format start date as datetime date
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    
    # Query data
    results = session.query(func.max(Measurement.tobs).label('temp_max'), func.min(Measurement.tobs).label('temp_min'), func.avg(Measurement.tobs).label('temp_avg')).filter(Measurement.date >= start_date).all()

    session.close()
    
    # Create a dictionary from the data
    temps_list = []
    for temp_max, temp_min, temp_avg in results:
        temps_dict = {}
        temps_dict['start_date'] = str(start_date)
        temps_dict['end_date'] = str(most_recent_date)
        temps_dict["temp_max"] = temp_max
        temps_dict["temp_min"] = temp_min
        temps_dict["temp_avg"] = temp_avg
        temps_list.append(temps_dict)

    return jsonify(temps_list)

@app.route("/api/v1.0/<start>/<end>")
def summarize_temp_between_dates(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return min, max, and average temperatures between specifified dates (inclusive)"""
    #format start date as datetime date
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()
    
    # Query data
    results = session.query(func.max(Measurement.tobs).label('temp_max'), func.min(Measurement.tobs).label('temp_min'), func.avg(Measurement.tobs).label('temp_avg')).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    session.close()
    
    # Create a dictionary from the data
    temps_list = []
    for temp_max, temp_min, temp_avg in results:
        temps_dict = {}
        temps_dict["start_date"] = str(start_date)
        temps_dict["end_date"] = str(end_date)
        temps_dict["temp_max"] = temp_max
        temps_dict["temp_min"] = temp_min
        temps_dict["temp_avg"] = temp_avg
        temps_list.append(temps_dict)

    return jsonify(temps_list)

if __name__ == '__main__':
    app.run(debug=True)
