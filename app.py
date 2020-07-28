from flask import Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy

#import sqlite3 as sql

app = Flask(__name__)

import MySQLdb



import json

with open('config.json', 'r') as c:
   params= json.load(c)["params"]

local_server=params['local_server']





if(local_server):
   app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
   app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db=SQLAlchemy(app)

class covid(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    location = db.Column(db.String(120), unique=False, nullable=False)
    covidStatus=db.Column(db.String(120), unique=False, nullable=False)



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
            age = request.form['age']
            location = request.form['location']
            status=request.form['status']


            entry=covid(name=name, age=age, location=location, covidStatus=status)

            count= covid.query.filter_by(location=location).filter_by(covidStatus="yes").count()

            

            
            db.session.add(entry)
            db.session.commit()


            return render_template("hello.html",name=name,count=count)
   

if __name__ == '__main__':
   app.run()