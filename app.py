from flask import Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
from math import radians, cos, sin, asin, sqrt 

#import sqlite3 as sql

app = Flask(__name__)

import MySQLdb



import json
import requests
import chardet
import geocoder


with open('config.json', 'r') as c:
   params= json.load(c)["params"]

local_server=params['local_server']






if(local_server):
   app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
   app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db=SQLAlchemy(app)

class covidstats(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    city=db.Column(db.String(80), unique=False, nullable=False)
    state=db.Column(db.String(80), unique=False, nullable=False)
    latitude = db.Column(db.Float, unique=False, nullable=False)
    lonngitude = db.Column(db.Float(120), unique=False, nullable=False)
    covidStatus=db.Column(db.String(120), unique=False, nullable=False)


def getlocn():
      res=requests.get('https://ipinfo.io/')
      data=res.json()
      location=data['loc'].split(',')
      latitude=location[0]
      longitude=location[1]


      return (float(latitude),float(longitude))

def cal_distance(lat1,lat2,lon1,lon2):
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return(c * r) 



@app.route('/')
def form():
   return render_template("form.html")

@app.route('/login')
def lo():
   return render_template("login.html")


@app.route('/hello',methods = ['POST', 'GET'])
def logi():
   if request.method == 'POST':
            name = request.form['name']
            city = request.form['city']
            state = request.form['state']
            status=request.form['status']

            latitude , longitude = getlocn()

            entry=covidstats(name=name, city=city, state=state, latitude=latitude, lonngitude=longitude, covidStatus=status)

            count= covidstats.query.filter_by(covidStatus="yes").all()
            total=0
            minn=0

            for case in count:
               reach_area = cal_distance(latitude,case.latitude,longitude,case.lonngitude)
               if  reach_area <= 0.1 :
                     total=total+1
                     minn=min(minn,reach_area)

            

            if(status=="yes"):
               db.session.add(entry)
            db.session.commit()


            return render_template("hello.html",name=name,count=total,closest=(minn*1000))
   

if __name__ == '__main__':
   app.run()
