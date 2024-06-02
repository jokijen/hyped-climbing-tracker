from app import app
import crags
import users
from flask import redirect, render_template, request


@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.login(username, password):
            return redirect("/home")
        else:
            return render_template("error.html", message="Incorrect username or password")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("error.html", message="The passwords do not match")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registration was unsuccessful. Please try a again.")


@app.route("/home")
def home():
    if request.method == "GET":
        return render_template("home.html")

    if request.method == "POST":
        pass



@app.route("/crags")
def crags():
    pass
