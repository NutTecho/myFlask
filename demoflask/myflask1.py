from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_restful import Api,Resource,abort,reqparse
from flask_sqlalchemy import SQLAlchemy,Model
from datetime import timedelta
import pymssql
app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days = 5)

# database
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql://scott:tiger@localhost:'

# dialect+driver://username:password@host:port/database
# engine = db.create_engine('mssql+pymssql://client1:admin@localhost:5000/test')

api = Api(app)


# m = MetaData()
# t = Table('t', m,
#         Column('id', Integer, primary_key=True),
#         Column('x', Integer))

# class CityModel(db.Model):
#     city = db.Column(db.In)

# city_add_args = reqparse.RequestParser()
# city_add_args.add_argument("fname",type=str,help="wrong type. Insert string")
# city_add_args.add_argument("lname",type=str,help="wrong type. Insert string")
# city_add_args.add_argument("age",type=int,help="wrong type. Insert int")

conn = pymssql.connect('127.0.0.1', 'client1', 'admin', "test")
cursor = conn.cursor(as_dict=True)

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

api.add_resource(WeatherCity,"/weather/<string:city>")


def getdb():
    # conn = pymssql.connect('127.0.0.1', 'client1', 'admin', "test")
    # cursor = conn.cursor(as_dict=True)
    # getdata = {}
    cursor.execute('SELECT * FROM dbo.xx ')
    row = cursor.fetchall()
    # for row in cursor:
        # print("ID=%d, Name=%s" % (row['id'], row['fname']))
        # getdata[row['id']] = row['fname']
        # getdata['fname'] = row['fname']
    # conn.close()

    return row

def inserttodb(fname,lname,age):
    sql = "insert into xx(fname,lname,age) values(%s,%s,%s)"
    cursor.execute(sql,(fname,lname,age))
    conn.commit()

def deletetodb(id_data):
    sql = "delete from xx where id = %s"
    cursor.execute(sql,id_data)
    conn.commit()

def updatetodb(id,fname,lname,age):
    sql = "update xx set fname = %s,lname = %s,age = %s where id = %s"
    cursor.execute(sql,(fname,lname,age,id))
    conn.commit()

@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        getuser = request.form.get('user_data')
        getpass = request.form.get('pass_data')
        session["getuser"] = getuser
        session["getpass"] = getpass
        print(getuser,getpass)
        if (getpass == "1234"):
            flash("Login Success !!")
            return render_template("user.html",user = getuser)
        else:
            return render_template("login.html")
    else:
        if "getuser" in session:
            getuser = session["getuser"]
            flash("Login Already !!")
            return render_template("user.html",user = getuser)
        else:
            return render_template("login.html")


@app.route("/user")
def user():
    if "getuser" in session:
        getuser = session["getuser"]
        flash("Login Already !!")
        return render_template("user.html",user = getuser)
    else:
        redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("getuser",None)
    session.pop("getpass",None)
    return redirect(url_for("login"))



@app.route("/raw")
def rawdata():
    # data = 5
    # return "hello World"
    db1 = getdb()
    # print(db1)
    return render_template('rawdata.html',datas = db1)



@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/addform")
def insertform():
    return render_template('addform.html')

@app.route("/insert", methods = ['POST'])
def insert():
    if request.method == "POST":
        fname = request.form['input_fname']
        lname = request.form['input_lname']
        age = request.form['input_age']
        print(fname,lname,age)
        inserttodb(fname,lname,age)
        return redirect(url_for('rawdata'))

@app.route("/update", methods = ['POST'])
def update():
    if request.method == "POST":
        idx = request.form['idx']
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        updatetodb(idx,fname,lname,age)
        return redirect(url_for('rawdata'))


@app.route("/delete/<string:id_data>", methods = ['GET'])
def delete(id_data):
    deletetodb(id_data)
    return redirect(url_for('rawdata'))



if __name__ == "__main__":
    app.run(debug = True)