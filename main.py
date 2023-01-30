#!/usr/bin/env python3

import os
import sys

import dotenv
import stytch
from flask import Flask, render_template, request, make_response, redirect, g, url_for
from functools import wraps

# load the .env file
dotenv.load_dotenv()

# By default, run on localhost:4567
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "4567"))
MAGIC_LINK_URL = f"http://{HOST}:{PORT}/authenticate"

# Load the Stytch credentials, but quit if they aren't defined
STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")
STYTCH_SECRET = os.getenv("STYTCH_SECRET")
if STYTCH_PROJECT_ID is None:
    sys.exit("STYTCH_PROJECT_ID env variable must be set before running")
if STYTCH_SECRET is None:
    sys.exit("STYTCH_SECRET env variable must be set before running")

# NOTE: Set environment to "live" if you want to hit the live api
stytch_client = stytch.Client(
    project_id=STYTCH_PROJECT_ID,
    secret=STYTCH_SECRET,
    environment="test",
)

# create a Flask web app
app = Flask(__name__)

# decorator to use for routes that should only be accessed by authenticated users
def auth_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        
        # redirect to home if session is not present in request
        auth_context = get_request_auth_context(request)
        if auth_context is None:
            print("Unauthenticated. Redirecting")
            return redirect(url_for("index"))
        
        g.auth_context = auth_context
        return f(*args, **kwargs)
    return wrap

# decorator for retrieving and passing along context on session user, if exists
def with_auth_context(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        
        g.auth_context = get_request_auth_context(request)
        return f(*args, **kwargs)

    return wrap


# handles the homepage for Hello Socks depending on authentication state
@app.route("/")
@with_auth_context
def index() -> str:
    if g.auth_context:
        email = g.auth_context.get("user").emails[0].email
        resp = make_response(render_template("loggedIn.html", email=email))
        return resp
    
    resp = make_response(render_template("loginOrSignUp.html"))
    resp.delete_cookie("stytch-session")
    return resp


# takes the email entered on the homepage and hits the stytch
# loginOrCreateUser endpoint to send the user a magic link
@app.route("/login_or_create_user", methods=["POST"])
def login_or_create_user() -> str:

    try:
        resp = stytch_client.magic_links.email.login_or_create(
            email=request.form["email"],
            login_magic_link_url=MAGIC_LINK_URL,
            signup_magic_link_url=MAGIC_LINK_URL,
        )
    except:
        return "something went wrong sending magic link"
 
    return render_template("emailSent.html", type="login")


# This is the endpoint the link in the magic link hits.
# It takes the token from the link's query params and hits the
# stytch authenticate endpoint to verify the token is valid
@app.route("/authenticate")
def authenticate():

    try:
        resp = stytch_client.magic_links.authenticate(token=request.args["token"], session_duration_minutes=5)
    except:
        return "something went wrong authenticating token"
    
    stytch_session = resp.session_token

    auth_factor = resp.session.authentication_factors[-1]
    email = auth_factor.get('email_factor').get('email_address')

    session_resp = make_response(render_template("loggedIn.html", email=email))
    session_resp.set_cookie("stytch-session", stytch_session)
    return session_resp


# An example of a protected route, that should only be 
# accessible by an authenticated user
@app.route("/account")
@auth_required
def account():
    emails = []
    user = g.auth_context.get("user")
    for email in user.emails:
        emails.append(email.email)
    
    return render_template("account.html", user_id=user.user_id, emails=", ".join(emails))


# takes the email entered on the logged in account page and hits the Stytch
# magic link send endpoint with the current session, in order to
# associate the email with the authenticated user
@app.route("/add_email", methods=["POST"])
@auth_required
def add_email():

    try:
        resp = stytch_client.magic_links.email.send(
            email=request.form["email"],
            session_token=g.auth_context.get("stytch_session"),
            login_magic_link_url=MAGIC_LINK_URL,
            signup_magic_link_url=MAGIC_LINK_URL,
        )
    except:
        return "something went wrong sending magic link"

    return render_template("emailSent.html", type="authentication")


# handles the logout endpoint
@app.route("/logout")
def logout() -> str:
    resp = make_response(render_template("loggedOut.html"))
    resp.delete_cookie("stytch-session")
    return resp


# authenticates the session token, if present and returns information
# about the logged in user
def get_request_auth_context(request):
    
    stytch_session = request.cookies.get("stytch-session")
    if not stytch_session:
        return None

    # authenticate session, if invalid return empty auth context
    try:
        resp = stytch_client.sessions.authenticate(stytch_session)
    except:
        print("session authentication failed")
        return None
    
    return {"stytch_session": stytch_session, "user": resp.user}

# run's the app on the provided host & port
if __name__ == "__main__":
    # in production you would want to make sure to disable debugging
    app.run(host=HOST, port=PORT, debug=True)
