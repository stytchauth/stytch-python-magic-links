#!/usr/bin/env python3

import os
import sys

import dotenv
import stytch
from flask import Flask, render_template, request

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


# handles the homepage for Hello Socks
@app.route("/")
async def index() -> str:
    return render_template("loginOrSignUp.html")


# takes the email entered on the homepage and hits the stytch
# loginOrCreateUser endpoint to send the user a magic link
@app.route("/login_or_create_user", methods=["POST"])
async def login_or_create_user() -> str:
    resp = await stytch_client.magic_links.email.login_or_create_async(
        email=request.form["email"],
        login_magic_link_url=MAGIC_LINK_URL,
        signup_magic_link_url=MAGIC_LINK_URL,
    )

    if resp.status_code != 200:
        print(resp)
        return "something went wrong sending magic link"
    return render_template("emailSent.html")


# This is the endpoint the link in the magic link hits.
# It takes the token from the link's query params and hits the
# stytch authenticate endpoint to verify the token is valid
@app.route("/authenticate")
async def authenticate() -> str:
    resp = await stytch_client.magic_links.authenticate_async(request.args["token"])

    if resp.status_code != 200:
        print(resp)
        return "something went wrong authenticating token"
    return render_template("loggedIn.html")


# handles the logout endpoint
@app.route("/logout")
async def logout() -> str:
    return render_template("loggedOut.html")


# run's the app on the provided host & port
if __name__ == "__main__":
    # in production you would want to make sure to disable debugging
    app.run(host=HOST, port=PORT, debug=True)
