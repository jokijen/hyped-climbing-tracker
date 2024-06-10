from app import app
import climbs, crags, users
from flask import redirect, render_template, request, session


@app.route("/index", methods=["GET", "POST"]) # landing/login page
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


@app.route("/logout")
def logout():
    users.logout() # clears the session
    return render_template("logout.html")
    

@app.route("/home")
def home():
    if not users.user_id(): # if user is not logged in, take to login page
        return redirect("/")
    
    return render_template("home.html")


@app.route("/search", methods=["GET"])
def search_page():
    query = request.args["query"]
    find_crags = crags.search_crags(query)
    find_climbs = climbs.search_climbs(query)
    return render_template("search.html", search_terms=query, crags_list=find_crags, climbs_list=find_climbs)


@app.route("/crags", methods=["GET", "POST"])
def crags_page():
    if not users.user_id():
        return redirect("/")

    if request.method == "GET":
        all_crags = crags.get_all_crags()
        return render_template("crags.html", crags_list=all_crags)
    

@app.route("/crags/<int:id>")
def crag_detail(id):
    if not users.user_id():
        return redirect("/")

    crag_details = crags.get_crag(id)
    climbs_at_crag = climbs.get_climbs_by_crag_id(id) # all climbs at that crag
    climb_count = len(climbs_at_crag) # number of climbs at crag
    return render_template("crag_detail.html", id=id, crag_details=crag_details, climbs_at_crag=climbs_at_crag, climb_count=climb_count)


@app.route("/climbs", methods=["GET", "POST"])
def climbs_page():
    if not users.user_id():
        return redirect("/")

    if request.method == "GET":
        all_climbs = climbs.get_all_climbs()
        return render_template("climbs.html", climbs_list=all_climbs)


@app.route("/climbs/<int:id>")
def climb_detail(id):
    if not users.user_id():
        return redirect("/")

    climb_details = climbs.get_climb(id)
    comments = climbs.get_comments_for_climb_id(id) # all comments of that climb
    sends = climbs.get_sends_for_climb_id(id) # all sends by users of that climb
    send_count = len(sends) # total number of sends for the climb
    return render_template("climb_detail.html", id=id, climb_details=climb_details, comments=comments, sends=sends, send_count=send_count)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    pass
