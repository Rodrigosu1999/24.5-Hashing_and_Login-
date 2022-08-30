from logging import getLoggerClass
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from models import connect_db, db, User, Feedback
from forms import AddUserForm, LoginUserForm, AddFeedbackForm, UpdateFeedbackForm
# from sqlalchemy.exc import IntegrityError

bcrypt = Bcrypt()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_exc"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "Secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return redirect("/register")

# User routes


@app.route('/register', methods=["GET", "POST"])
def register_page():
    """Show register form
    When form is submitted a new user will be created"""
    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username
        flash(f"You have successfully registered {new_user.username}")
        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    """Show  login form
    If authentication is successfull the user will be logged in"""
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session["username"] = user.username
            flash(f"Welcome back {username}!")
            return redirect(f"/users/{user.username}")
        else:
            flash(
                "Authentication failed, Either the user doesn't exist or the password was typed incorrectly")
            return redirect("/login")

    else:
        return render_template("login.html", form=form)


@app.route('/secret')
def secret_page():
    if "username" not in session:
        flash("You must be logged in to access")
        return redirect("/")
    return render_template("secret.html")


@app.route("/logout", methods=["POST"])
def logout():
    """Logout the user from the session"""
    session.pop("username")

    return redirect("/")


@app.route('/users/<username>')
def user_detail(username):
    """Display teh current users information"""
    if "username" not in session:
        flash("You must be logged in to access")
        return redirect("/")
    elif session["username"] != username:
        flash("You can only look at the logged in user details")
        return redirect("/")
    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.filter_by(username=user.username).all()
    return render_template("details.html", user=user, feedback=feedback)

# Feedback routes


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def feedback_form_page(username):
    """Show feedback form"""
    if "username" not in session:
        flash("You must be logged in to access")
        return redirect("/")
    elif session["username"] != username:
        flash("Only the owner can access this feedback form")
        return redirect("/")

    form = AddFeedbackForm()
    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content,
                            username=session["username"])
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{session['username']}")

    else:
        return render_template("new_feedback.html", form=form)


@app.route('/feedback/<fb_id>/update', methods=["GET", "POST"])
def feedback_update_page(fb_id):
    """Show update feedback form"""
    feedback = Feedback.query.get_or_404(fb_id)

    if "username" not in session:
        flash("You must be logged in to access")
        return redirect("/")
    elif session["username"] != feedback.user.username:
        flash("Only the owner can access this feedback form")
        return redirect("/")

    form = UpdateFeedbackForm()
    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data

        feedback.title = title
        feedback.content = content

        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{session['username']}")

    else:
        return render_template("update_feedback.html", form=form, feedback=feedback)


# Delete routes

@app.route('/feedback/<fb_id>/delete', methods=["POST"])
def delete_feedback(fb_id):
    """Delete feedback from database"""
    feedback = Feedback.query.get_or_404(fb_id)

    if "username" not in session:
        flash("You must be logged in to access")
        return redirect("/")
    elif session["username"] != feedback.user.username:
        flash("Only the owner can delete this feedback")
        return redirect("/")

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{session['username']}")


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete user from database"""
    user = User.query.filter_by(username=username).first()

    if "username" not in session:
        flash("You must be logged in to access")
        return redirect("/")
    elif session["username"] != user.username:
        flash("Only the authorized user can acces this page")
        return redirect("/")

    db.session.delete(user)
    db.session.commit()

    return redirect("/")
