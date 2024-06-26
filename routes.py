from app import app
import climbs, crags, users, comments, ticklist, favourites, sends
from flask import redirect, render_template, abort, flash, request, session, url_for


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
    latest_sends = sends.get_latest_sends()
    return render_template("home.html", username=username, admin=is_admin, latest_sends=latest_sends)


@app.route("/favourites")
def favourites_page():
    if not users.user_id():
        return redirect("/")
    
    user_id = users.user_id()
    favourite_crags = favourites.get_favourites(user_id)
    is_admin = users.is_admin()
    return render_template("favourites.html", favourite_crags=favourite_crags, admin=is_admin)


@app.route("/ticklist")
def ticklist_page():
    if not users.user_id():
        return redirect("/")
    
    user_id = users.user_id()
    tick_list = ticklist.get_ticklist(user_id)
    is_admin = users.is_admin()
    return render_template("ticklist.html", tick_list=tick_list, admin=is_admin)


@app.route("/logged-sends")
def logged_sends_page():
    if not users.user_id():
        return redirect("/")
    
    user_id = users.user_id()
    logged_sends = sends.get_sends_for_user(user_id)
    is_admin = users.is_admin()

    return render_template("logged_sends.html", sends=logged_sends, admin=is_admin)


@app.route("/search", methods=["GET"])
def search_page():
    if not users.user_id():
        return redirect("/")
    
    query = request.args["query"]
    find_crags = crags.search_crags(query)
    find_climbs = climbs.search_climbs(query)
    is_admin = users.is_admin()
    return render_template("search.html", search_terms=query, crags_list=find_crags, climbs_list=find_climbs, admin=is_admin)


@app.route("/crags", methods=["GET", "POST"])
def crags_page():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
        all_crags = crags.get_all_crags()
        is_admin = users.is_admin()
        return render_template("crags.html", crags_list=all_crags, admin=is_admin)
    

@app.route("/crags/<int:id>")
def crag_detail(id):
    if not users.user_id():
        return redirect("/")

    user_id = users.user_id()
    crag_details = crags.get_crag(id)
    climbs_at_crag = climbs.get_climbs_by_crag_id(id) # all climbs at that crag
    climb_count = len(climbs_at_crag) # number of climbs at crag
    fav_count = favourites.times_favourited(id)
    is_favourite = favourites.is_in_favourites(user_id, id)
    is_admin = users.is_admin()
    return render_template("crag_detail.html", id=id, crag_details=crag_details, climbs_at_crag=climbs_at_crag, climb_count=climb_count, fav_count=fav_count, is_favourite=is_favourite, admin=is_admin)


@app.route("/add-crag", methods=["GET", "POST"])
def add_crag():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        if not users.is_admin():
            return render_template("error.html", message="Only admins can add crags. Get in touch with us if this is something that interests you.")

        is_admin = users.is_admin()
        return render_template("add_crag.html", admin=is_admin)
    
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
        is_admin = users.is_admin()
        return render_template("climbs.html", climbs_list=all_climbs, admin=is_admin)


@app.route("/climbs/<int:id>", methods=["GET", "POST"]) 
def climb_detail(id):
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
        user_id = users.user_id()
        is_admin = users.is_admin()
        climb_details = climbs.get_climb(id)
        all_comments = comments.get_comments_for_climb_id(id) # all comments of that climb
        logged_sends = sends.get_sends_for_climb_id(id) # all sends by users of that climb
        send_count = len(logged_sends) # total number of sends for the climb
        tick_count = ticklist.times_on_ticklist(id)
        tick_date = ticklist.date_ticked(user_id, id)
        send_date = sends.date_sent(user_id, id)
        avg_rating = sends.average_rating(id)
        on_ticklist = ticklist.is_on_ticklist(user_id, id)
        is_climbed = sends.is_sent(user_id, id)
        return render_template("climb_detail.html", current_user=user_id, admin=is_admin, climb_details=climb_details, comments=all_comments, sends=logged_sends, send_count=send_count, tick_count=tick_count, tick_date=tick_date, send_date=send_date, avg_rating=avg_rating, on_ticklist=on_ticklist, is_climbed=is_climbed)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        user_id = users.user_id()

        content = request.form["content"]
        if comments.add_comment(user_id=user_id, climb_id=id, content=content):
            return redirect(request.url)
        return render_template("error.html", message="Something went wrong with adding the comment :( Please try a again.")


@app.route("/delete-comment/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        
        comment = comments.get_comment_for_comment_id(comment_id)
        if comment and (comment.user_id == users.user_id() or users.is_admin()): # Checks if the user is the same that wrote the comment or an admin, in which case they can delete the message
            if comments.delete_comment_using_id(comment_id):
                return redirect(url_for("climb_detail", id=comment.climb_id))
            return render_template("error.html", message="Something went wrong with deleting the comment :( Please try a again.")


@app.route("/add-to-favourites/<int:crag_id>", methods=["POST"])
def add_to_favourites(crag_id):
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        
        user_id = users.user_id()
        if favourites.is_in_favourites(user_id, crag_id): # Flash message if the crag is already in favourites
            flash("The crag is already in favourites", "error")
            return redirect(url_for("crag_detail", id=crag_id))
        
        else:
            if favourites.add_crag_to_favourites(user_id, crag_id): # Add crag to favourite crags
                return redirect(url_for("crag_detail", id=crag_id))
            return render_template("error.html", message="Something went wrong with adding the crag to favourites :( Please try a again.")


@app.route("/remove-from-favourites/<int:crag_id>", methods=["POST"]) 
def remove_from_favourites(crag_id):
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        
        user_id = users.user_id()
        is_favourite = favourites.is_in_favourites(user_id, crag_id)

        if is_favourite: 
            if favourites.delete_from_favourites(user_id, crag_id):
                return redirect(url_for("crag_detail", id=crag_id))
            return render_template("error.html", message="Something went wrong with deleting the crag from favourites :( Please try a again.")


@app.route("/add-to-ticklist/<int:climb_id>", methods=["POST"])
def add_to_ticklist(climb_id):
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        
        user_id = users.user_id()

        if sends.is_sent(user_id, climb_id): # Flash message if the user already sent the climb
            flash("You already sent the climb, so you cannot add it to your tick-list", "error")
            return redirect(url_for("climb_detail", id=climb_id))
        if ticklist.is_on_ticklist(user_id, climb_id): # Flash message if the climb is already on tick-list
            flash("The climb is already on your tick-list", "error")
            return redirect(url_for("climb_detail", id=climb_id))
        else:
            if ticklist.add_climb_to_ticklist(user_id, climb_id): # Add crag to favourite crags
                return redirect(url_for("climb_detail", id=climb_id))
            return render_template("error.html", message="Something went wrong with adding the climb to your tick-list :( Please try a again.")


@app.route("/remove-from-ticklist/<int:climb_id>", methods=["POST"]) 
def remove_from_ticklist(climb_id):
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        
        user_id = users.user_id()
        on_ticklist = ticklist.is_on_ticklist(user_id, climb_id)
        is_sent = sends.is_sent(user_id, climb_id)

        if on_ticklist and not is_sent: 
            if ticklist.delete_from_ticklist(user_id, climb_id):
                return redirect(url_for("climb_detail", id=climb_id))
        return render_template("error.html", message="Something went wrong with removing the climb from your tick-list :( Please try a again.")


@app.route("/add-climb", methods=["GET", "POST"]) 
def add_climb():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
        all_crags = crags.get_all_crags()
        is_admin = users.is_admin()

        return render_template("add_climb.html", all_crags=all_crags, admin=is_admin)
    
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


@app.route("/log-send/<int:climb_id>", methods=["GET", "POST"]) 
def log_send(climb_id):
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
        user_id = users.user_id()
        if sends.is_sent(user_id, climb_id):
            flash("You already sent this climb", "error")
            return redirect(url_for("climb_detail", climb_id=climb_id))
        
        climb_details = climbs.get_climb(climb_id)
        is_admin = users.is_admin()
        return render_template("log_send.html", climb_details=climb_details, admin=is_admin)
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        user_id = users.user_id()
        send_date = request.form["send_date"]
        send_type = request.form["send_type"]
        review = request.form["review"]
        rating = request.form["rating"]

        if sends.add_send(user_id, climb_id, send_date, send_type, review, rating):
            if ticklist.is_on_ticklist(user_id, climb_id):
                ticklist.delete_from_ticklist(user_id, climb_id) 
            return redirect(url_for("climb_detail", id=climb_id))
        else:
            return render_template("error.html", message="Something went wrong with logging the send :( Please try a again.")


@app.route("/edit-send/<int:climb_id>", methods=["GET", "POST"]) 
def edit_send(climb_id):
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
        user_id = users.user_id()
        climb_details = climbs.get_climb(climb_id)
        send_details = sends.get_send_details(user_id, climb_id)
        options = ["onsight", "flash", "send"]
        is_admin = users.is_admin()
        return render_template("edit_send.html", user_id=user_id, climb_details=climb_details, send_details=send_details, options=options, admin=is_admin)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        
        user_id = users.user_id()
        send_date = request.form["send_date"]
        send_type = request.form["send_type"]
        review = request.form["review"]
        rating = request.form["rating"]

        if sends.add_send(user_id, climb_id, send_date, send_type, review, rating):
            if ticklist.is_on_ticklist(user_id, climb_id):
                ticklist.delete_from_ticklist(user_id, climb_id) 
            return redirect(url_for("climb_detail", id=climb_id))
        else:
            return render_template("error.html", message="Something went wrong with logging the send :( Please try a again.")


@app.route("/delete-send/<int:climb_id>", methods=["POST"]) 
def delete_from_sends(climb_id):
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        
        user_id = users.user_id()
        is_sent = sends.is_sent(user_id, climb_id)

        if is_sent: 
            if sends.delete_send(user_id, climb_id):
                return redirect(url_for("climb_detail", id=climb_id))
        return render_template("error.html", message="Something went wrong with deleting the send :( Please try a again.")


@app.route("/random")
def random():
    if not users.user_id():
        return redirect("/")

    random_crag_id = crags.get_random_crag()
    random_climb_id = climbs.get_random_climb()
    crag_details = crags.get_crag(random_crag_id)
    climb_details = climbs.get_climb(random_climb_id)
    is_admin = users.is_admin()
    return render_template("random.html", crag_details=crag_details, climb_details=climb_details, admin=is_admin)


@app.route("/thesaurus")
def thesaurus():
    if not users.user_id():
        return redirect("/")

    is_admin = users.is_admin()
    return render_template("thesaurus.html", admin=is_admin)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        
        user_id = users.user_id()
        user_info = users.get_user_info(user_id)
        is_admin = users.is_admin()
        return render_template("profile.html", user_info=user_info, admin=is_admin)
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        
        user_id = users.user_id()
        old_password = request.form["old_password"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if not users.is_valid_password(password1):
            flash("Password must be at least 8 characters long and contain at least one number", "error")
            return redirect(request.url)
        
        if password1 != password2:
            flash("The passwords do not match", "error")
            return redirect(request.url)
        
        if not users.validate_password(user_id, old_password):
            flash("Incorrect password", "error")
            return redirect(request.url)

        if users.change_password(user_id, password1):
            flash("Password successfully changed", "success")
            return redirect(request.url)
        
        return render_template("error.html", message="The operation was unsuccessful. Please try a again.")

