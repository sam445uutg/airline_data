#from flask import Flask
import pandas as pd
import numpy as np
from flask import Flask , jsonify,request
from flask_ngrok import run_with_ngrok
import excel2json
app= Flask(__name__)


dataset = pd.read_excel("./Data_Train.xlsx")

@app.route('/')
def hello():
  res = jsonify(message="helloooo")
  res.headers.add("Access-Control-Allow-Origin", "*")
  return res
@app.route('/find_filght',methods=['GET'])
def find_search():
  source= request.args.get('src')
  destination = request.args.get('den')
  date= request.args.get('dat')  
  data=dataset[dataset['Source']==source]
  data = data[data['Destination']==destination]
  data['joureny_month']= pd.to_datetime(data['Date_of_Journey'], format="%d/%m/%Y").dt.month
  data['joureny_day']= pd.to_datetime(data['Date_of_Journey'], format="%d/%m/%Y").dt.day
  
  date_joureny = date.split('-')
  day_of_joureny = int(date_joureny[2])
  month_of_joureny =int( date_joureny[1])
  data = data[data['joureny_month']>= month_of_joureny]   
  data = data.head(50)
  data_json = data.to_json(orient="records")
  print(data_json)
  resonpse = jsonify(message= data_json)
  resonpse.headers.add("Access-Control-Allow-Origin", "*")
  return resonpse


@app.route('/add_filght')
def airLine_add():
  airline  = request.args.get('airline')
  Date_of_Journey = request.args.get('date-of-journey')
  Source  = request.args.get('src')
  Destination = request.args.get('den')
  Route  = request.args.get('Rout')
  Dep_time  = request.args.get('dep_t')
  Arrival_time = request.args.get('arr_t')
  Duration  = request.args.get('dur')
  Total_stops = request.args.get('tos')
  Additional_info  = request.args.get('addinfo')
  price = request.args.get('price')
  flgnno = request.args.get('flgno')
  print(dataset)
  df = dataset
 
  new=[len(dataset.index),None,None,None,airline, Date_of_Journey,Source, Destination,Route, Dep_time ,Arrival_time, Duration, Total_stops, Additional_info, price,flgnno]
  df = df.append(pd.Series(new, index=df.columns[:len(new)]), ignore_index=True)
  df.to_excel("./Data_Train.xlsx")
  resonpse = jsonify(message='Sccessfully add csv')
  resonpse.headers.add("Access-Control-Allow-Origin", "*")
  return resonpse


if __name__=="__main__":
    app.run()

