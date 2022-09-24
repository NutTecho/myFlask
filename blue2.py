from flask import Blueprint,render_template

second = Blueprint("blue2",__name__,static_folder="static",template_folder="templates")

@second.route("/")
def home():
    return render_template("user.html",user = "admin")