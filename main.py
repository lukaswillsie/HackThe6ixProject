from flask import Flask, render_template, url_for, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/background_process')
def background_process():
    try:
        location = request.args.get('location', 0, type=str)
        print("got here")
        print(location)
        # Backend process go here
        
        return jsonify(result=[])
    except Exception as e:
        print(str(e))
        return str(e)

if __name__ == "__main__":
    app.run()