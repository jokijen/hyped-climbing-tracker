from app import app
import climbs, crags, users
from flask import redirect, render_template, abort, flash, request, session


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

        if users.is_suspended(username):
            return render_template("error.html", message="Your account has been suspended. Please contact us to sort it out.")
        if users.user_login(username, password):
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

        if not users.is_valid_password(password1):
            flash("Password must be at least 8 characters long and contain at least one number", "error")
            return redirect("/register")
        
        if password1 != password2:
            flash("The passwords do not match.", "error")
            return redirect("/register")
        
        if users.register_user(username, email, password1):
            return redirect("/home")
        
        return render_template("error.html", message="Registration was unsuccessful. (Possible reasons: username already taken, email already has an account, or other error.) Please try a again.")


@app.route("/logout")
def logout():
    users.user_logout() # clears the session
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
    sends = climbs.get_sends_for_user(user_id)
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
            return render_template("error.html", message="Only admins can add crags. Get in touch with us if this is something that interests you.")
        return render_template("add_crag.html")
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]: # invalid or no csrf token
            abort(403)

        crag_name = request.form["crag_name"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        crag_description = request.form["crag_description"]
        manager = request.form["manager"]
        created_by = users.user_id()

        if crags.add_new_crag(crag_name, latitude, longitude, crag_description, manager, created_by):
            return redirect("/crags")
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
    return render_template("climb_detail.html", climb_details=climb_details, comments=comments, sends=sends, send_count=send_count)


@app.route("/add-climb", methods=["GET", "POST"]) 
def add_climb():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
        all_crags = crags.get_all_crags()
        return render_template("add_climb.html", all_crags=all_crags)
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        climb_name = request.form["climb_name"]
        difficulty = request.form["difficulty"]
        climb_type = request.form["climb_type"]
        climb_description = request.form["climb_description"]
        crag_id = request.form["crag_id"]
        first_ascent = request.form["first_ascent"]
        created_by = users.user_id()

        if climbs.add_new_climb(climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by):
            return redirect("/climbs")
        else:
            return render_template("error.html", message="Something went wrong with adding the climb :( Please try a again.")


@app.route("/log-send/<int:id>", methods=["GET", "POST"]) 
def log_send(id):
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
        climb_details = climbs.get_climb(id)
        return render_template("log_send.html", climb_details=climb_details)
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        user_id = users.user_id()
        climb_id = id
        send_date = request.form["send_date"]
        send_type = request.form["send_type"]
        review = request.form["review"]
        rating = request.form["rating"]

        if climbs.add_send(user_id, climb_id, send_date, send_type, review, rating):
            return redirect("/logged-sends")
        
        else:
            return render_template("error.html", message="Something went wrong with logging the send :( Please try a again.")


@app.route("/random")
def random():
    if not users.user_id():
        return redirect("/")

    random_crag_id = crags.get_random_crag()
    random_climb_id = climbs.get_random_climb()
    crag_details = crags.get_crag(random_crag_id)
    climb_details = climbs.get_climb(random_climb_id)

    return render_template("random.html", crag_details=crag_details, climb_details=climb_details)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
        user_id = users.user_id()
        user_info = users.get_user_info(user_id)
        return render_template("profile.html", user_info=user_info)
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        
        user_id = users.user_id()
        old_password = request.form["old_password"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if not users.is_valid_password(password1):
            flash("Password must be at least 8 characters long and contain at least one number", "error")
            return redirect("/profile")
        
        if password1 != password2:
            flash("The passwords do not match", "error")
            return redirect("/profile")
        
        if not users.validate_password(user_id, old_password):
            flash("Incorrect password", "error")
            return redirect("/profile")

        if users.change_password(user_id, password1):
            flash("Password successfully changed", "success")
            return redirect("/profile")
        
        return render_template("error.html", message="The operation was unsuccessful. Please try a again.")
