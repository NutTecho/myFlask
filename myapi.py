from flask import Flask,request
from flask_restful import Api,Resource,abort,reqparse

app = Flask(__name__)
api = Api(app)

myCity = {
    "Rayong":{"weather":"hot","population":1500},
    "Chonburi" : {"weather":"rainy","population":1000},
    "Trad" :{"weather":"cool","population":1200}
}

def notfoundcity(city):
    if city not in myCity:
        abort(404,message = "No data weather")

class WeatherCity(Resource):
    def get(self,city):
       notfoundcity(city)
       return myCity[city]
           
    def post(self,city):
        return {"data","Create Resource " + city}

# api.add_resource(WeatherCity,"/weather/<string:city>")

@app.route("/weather",methods = ["GET","POST","PUT","DELETE"])
def weather():
    if request.method == "POST":
        body = request.get_json()
        getk = [i for i in body.keys()][0]
        print(getk)
        myCity[getk] = [i for i in body.values()]
        return {"message" : "data changed", "body" : myCity[getk]},201
    elif request.method == "GET":
        # if getcity == "":
        return myCity,200
        # else:
            # return myCity[getcity],200
    elif request.method == "PUT":
        body = request.get_json()
        myCity[body.key()] = body.values()
        return {"message" : "data changed", "body" : myCity[body.key()]},200
    elif request.method == "DELETE":
        delete = request.args.get()
        # myCity.pop(delete)
        return myCity,200


if __name__ == "__main__":
    app.run(debug = True)