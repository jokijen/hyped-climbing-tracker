from app import app
import climbs, crags, users
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
        email = request.form["email"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("error.html", message="The passwords do not match")
        if users.register(username, email, password1):
            return redirect("/home")
        else:
            return render_template("error.html", message="Registration was unsuccessful. (Possible reasons: username already taken, other error.) Please try a again.")


@app.route("/logout", methods=["GET"])
def logout():
    if request.method == "GET":
        return render_template("logout.html")
    

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")

    if request.method == "POST":
        if users.logout():
            return redirect("/logout")
        pass


@app.route("/search", methods=["GET"])
def search_page():
    search_terms = request.args["query"]
    all_crags = crags.get_all_crags()
    all_climbs = climbs.get_all_climbs()
    return render_template("search.html", search_terms=search_terms, crags_list=all_crags, climbs_list=all_climbs)


@app.route("/crags", methods=["GET", "POST"])
def crags_page():
    if request.method == "GET":
        all_crags = crags.get_all_crags()
        return render_template("crags.html", crags_list=all_crags)
    

@app.route("/climbs", methods=["GET", "POST"])
def climbs_page():
    if request.method == "GET":
        all_climbs = climbs.get_all_climbs()
        return render_template("climbs.html", climbs_list=all_climbs)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    pass
