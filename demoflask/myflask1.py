from flask import Flask,render_template,request,redirect,url_for,session,flash,json
from flask_restful import Api,Resource,abort,reqparse
from flask_sqlalchemy import SQLAlchemy,Model
from flask_socketio import SocketIO, send
from datetime import timedelta
import pymssql
app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days = 5)

# databasetype+driver://user:password@host:port/db_name/
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pymssql://client1:admin@127.0.0.1/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
sockketio = SocketIO(app)


class Student(db.Model):
    # __tablename__ = 'test_table'
   _id = db.Column("id",db.Integer() , primary_key = True)
   fname = db.Column("fname",db.String(10))
   lname = db.Column("lname",db.String(10))
   age = db.Column("age",db.Integer())
   def __init__(self,fname,lname,age):
        self.fname = fname
        self.lname = lname
        self.age = age

#    def __repr__(self):
#         return "<User {}>".format(self.fname)

        
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

@app.route("/")
@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        getuser = request.form.get('user_data')
        getpass = request.form.get('pass_data')
        session["getuser"] = getuser
        session["getpass"] = getpass
        print(getuser,getpass)

        founduser =  Student.query.filter_by(fname = getuser).first()
        if founduser:
            session["age"] = founduser.age
            print(founduser.age)

        else:
            student = Student(getuser,"-",0)
            db.session.add(student)
            db.session.commit()

        flash("Login Success !!")
        return render_template("user.html",user = getuser)
        # else:
        #     return render_template("login.html")
    else:
        if "getuser" in session:
            getuser = session["getuser"]
            flash("Login Already !!")
            return render_template("user.html",user = getuser)
        # else:
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
    session.pop("age",None)
    return redirect(url_for("login"))



@app.route("/raw")
def rawdata():
    # data = 5
    # return "hello World"
    db1 = getdb()
    # print(db1[0])
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


@app.route("/chartdata",methods = ["GET"])
def chart():
    legend = 'Monthly Data' 
    # labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    # values = [6, 9, 8, 7, 6, 4, 7, 8]

    # labels = [i["fname"]  for i in getdb() ]
    # values = [i["age"]  for i in getdb() ]
    # print(labels)
    values = json.dumps( [i["age"]  for i in getdb() ] )
    labels = json.dumps( [i["fname"]  for i in getdb() ] )
    return render_template("chart.html",values=values, labels=labels, legend=legend )


@sockketio.on('message')
def handleMessage(msg):
    print('Message :' + msg)
    send(msg,broadcast = True)

if __name__ == "__main__":
    db.create_all()
    # app.run(debug = True)
    sockketio.run(app)