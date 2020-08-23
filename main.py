from flask import Flask, render_template, url_for, request, jsonify
import json
import sys
sys.path.append('./backend')
from access_historical import HistoricalDataAccessor
import random


app = Flask(__name__)

obj = HistoricalDataAccessor()
obj.build()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result/')
def result():
	return render_template('result.html')

@app.route('/map_day/')
def map_day():
	return render_template('map_day_cases.html')

@app.route('/map_week/')
def map_week():
	return render_template('map_week_cases.html')


@app.route('/map_month/')
def map_month():
	return render_template('map_month_cases.html')


@app.route('/map_total/')
def map_total():
	return render_template('map_total_cases.html')

def place_value(number): 
    return ("{:,}".format(number)) 

@app.route('/background_process')
def background_process():
    try:
        location = request.args.get('location', 0, type=str).split(",")
        lst = obj.getKeyMetrics(location[0], location[1])
        map_loc = obj.get_graphs(location[0], location[1])
        print(map_loc)
        for i in range(len(lst)):
            if lst[i] < 0:
                lst[i] = 0
            else:
                lst[i] = place_value(lst[i])
        

        f1 = open('data/data5.json', 'r')
        f2 = open('data/data25.json', 'r') 
        f3 = open('data/data50.json', 'r') 
        f4 = open('data/data200.json', 'r')  
        data5 = json.load(f1)
        data25 = json.load(f2) 
        data50 = json.load(f3) 
        data200 = json.load(f4)  


        temp = [data5, data25, data50, data200]

        for data in temp:
            if location[0] in data:
                prob = data[location[0]]
                print(prob)
            else:
                print('County not found')
                prob = random.uniform(0, 0.12)
            if prob > 0.03:
                lst.append('No')
            else:
                lst.append('Yes')
        
        print(lst)
        # Backend process go here
        return jsonify(result=lst)
    except Exception as e:
        print(str(e))
        return str(e)

@app.route('/heat_map_process')
def heat_map_process():
    try:
        location = request.args.get('time_range', 0, type=str)
        print("got here")
        print(location)
        # Backend process go here
        
        return jsonify(result=[])
    except Exception as e:
        print(str(e))
        return str(e)


if __name__ == "__main__":
    app.run(port=8800)