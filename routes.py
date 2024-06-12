from app import app
import climbs, crags, users
from flask import redirect, render_template, request, session


@app.route("/index", methods=["GET", "POST"]) # landing/login page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if users.user_id(): # user already logged in
            return redirect("/home")
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
        if users.user_id():
            return redirect("/home")
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
    
    username = session.get("username")
    is_admin = users.is_admin()

    return render_template("home.html", username=username, admin=is_admin)


@app.route("/favourites")
def favourites():
    if not users.user_id():
        return redirect("/")
    user_id = users.user_id()
    favourites = crags.get_favourites(user_id)
    return render_template("favourites.html", favourites=favourites)


@app.route("/ticklist")
def ticklist():
    if not users.user_id():
        return redirect("/")
    user_id = users.user_id()
    tick_list = climbs.get_ticklist(user_id)
    return render_template("ticklist.html", tick_list=tick_list)


@app.route("/logged-sends")
def logged_sends():
    if not users.user_id():
        return redirect("/")
    user_id = users.user_id()
    sends = climbs.get_sends(user_id)
    return render_template("logged_sends.html", sends=sends)


@app.route("/search", methods=["GET"])
def search_page():
    if not users.user_id():
        return redirect("/")
    query = request.args["query"]
    find_crags = crags.search_crags(query)
    find_climbs = climbs.search_climbs(query)
    return render_template("search.html", search_terms=query, crags_list=find_crags, climbs_list=find_climbs)


@app.route("/crags", methods=["GET", "POST"])
def crags_page():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
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


@app.route("/add-crag", methods=["GET", "POST"])
def add_crag():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        if not users.is_admin():
            return render_template("error.html", message="Unfortunately only admins can add crags. Get in touch with us if this is something that interests you.")
        return render_template("add_crag.html")
    
    if request.method == "POST":
        crag_name = request.form["crag_name"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        crag_description = request.form["crag_description"]
        created_by = request.form["created_by"]

        if crags.add_new_crag(crag_name, latitude, longitude, crag_description, created_by):
            return redirect("/home")
        else:
            return render_template("error.html", message="Something went wrong with adding the crag :( Please try a again.")


@app.route("/climbs", methods=["GET", "POST"])
def climbs_page():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
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


@app.route("/add-climb", methods=["GET", "POST"]) 
def add_climb():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
        all_crags = crags.get_all_crags()
        return render_template("add_climb.html", all_crags=all_crags)
    
    if request.method == "POST":
        climb_name = request.form["climb_name"]
        difficulty = request.form["difficulty"]
        climb_type = request.form["climb_type"]
        climb_description = request.form["climb_description"]
        crag_id = request.form["crag_id"]
        created_by = request.form["created_by"]

        if climbs.add_new_climb(climb_name, difficulty, climb_type, climb_description, crag_id, created_by):
            return redirect("/home")
        else:
            return render_template("error.html", message="Something went wrong with adding the climb :( Please try a again.")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    pass
