import sqlalchemy
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Create an engine for the sqlite database
engine = create_engine('sqlite:////Users/algend/Homework-10/Resources/hawaii.sqlite', echo=False)

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save a reference
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create a database session object
session=Session(engine)

#Flask setup 
app = Flask(__name__)

#Flask Routes
@app.route("/")
def home():
    """Welcome to the homepage"""
    return(
        f"List of all routes that are available:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
       
        f"/api/v1.0/start.date/end.date</br>")

@app.route("/api/v1.0/precipitation")
def precip():
    #Get last 12 months of precipitation
    date_year_ago=dt.date(2017,8,23)-dt.timedelta(days=365)
    precip_year=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=date_year_ago).all()
    
    #Create a data dictionary and append the list
    precip_data=[]
    for prcp_data in precip_year:
        prcp_dict={}
        prcp_dict["date"]= prcp_data[0]
        prcp_dict["precipitation"]= prcp_data[1]
        precip_data.append(prcp_dict)
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
 #Create a list of stations
def stations():
    stations_data=session.query(Station.name, Station.station, Station.elevation).all()
    station_list=[]
    for s in stations_data:
        stations_dict={}
        stations_dict['name'] = s[0]
        stations_dict['station'] = s[1]
        stations_dict['elevation'] =s[2]
        station_list.append(stations_dict)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    Measurement=Base.classes.measurement
    Station=Base.classes.station
    date_year_ago=dt.date(2017,8,23)-dt.timedelta(days=365)
    tobs_data=session.query(Station.name, Measurement.date, Measurement.tobs).filter(Measurement.date>=date_year_ago).all()
    tobs_list=[]
    for t in tobs_data:
        tobs_dict={}
        
        tobs_dict["Station"] = t[0]
        tobs_dict["Date"] = t[1]
        tobs_dict["Tobs"] = float(t[2])
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)
        
@app.route("/api/v1.0/start.date/end.date")
def start_end_avg():
    
    start_date=dt.date(2017,8,23)-dt.timedelta(days=365)
    end_date=dt.date(2017,8,23)
    #avg_start=session.query(Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date==date).all
    #data_avg=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date_year_ago).filter(Measurement.date <= end_date).all()
    min_temp=session.query(Measurement.tobs, func.min(Measurement.tobs)).filter(Measurement.date>=start_date)
    max_temp=session.query(Measurement.tobs, func.man(Measurement.tobs)).filter(Measurement.date>=start_date)
    avg_temp=session.query(Measurement.tobs, func.avg(Measurement.tobs)).filter(Measurement.date>=start_date)
    
    start_date=dt.date(2017,8,23)-dt.timedelta(days=365)
    end_date=dt.date(2017,8,23)
    
    min_temp=session.query(Measurement.tobs, func.min(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date))
    max_temp=session.query(Measurement.tobs, func.max(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date))
    avg_temp=session.query(Measurement.tobs, func.avg(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date))

    start_end_temp={"Temp Min.":min_temp[0][0], "Temp Max.":max_temp[0][0],"Temp Avg.": avg_temp[0][0]} 
    return jsonify(start_end_temp) 




if __name__=="__main__":
    app.run(debug=True)