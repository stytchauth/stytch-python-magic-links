import os

from flask import Flask, render_template, request
from dotenv import load_dotenv
from stytch import Client

# load the .env file
load_dotenv()

# pull in configuration from .env file
PORT = os.getenv("PORT")
HOST = os.getenv("HOST")

magic_link_url = "http://{0}:{1}/authenticate".format(HOST, PORT)

# define the stytch client using your stytch project id & secret
# set environment to "live" if you want to hit the live api
stytch_client = Client(
    project_id=os.getenv("STYTCH_PROJECT_ID"),
    secret=os.getenv("STYTCH_SECRET"),
    environment="test",
)

# create a Flask web app
app = Flask(__name__)


# handles the homepage for Hello Socks
@app.route('/')
def index():
    return render_template('loginOrSignUp.html')


# takes the email entered on the homepage and hits the stytch
# loginOrCreateUser endpoint to send the user a magic link
@app.route('/login_or_create_user', methods=['POST'])
def login_or_create_user():
    resp = stytch_client.magic_links.email.login_or_create(
        email=request.form['email'],
        login_magic_link_url=magic_link_url,
        signup_magic_link_url=magic_link_url
    )

    if resp.status_code != 200:
        print(resp)
        return "something went wrong sending magic link"
    return render_template('emailSent.html')


# This is the endpoint the link in the magic link hits. It takes the token from the
# link's query params and hits the stytch authenticate endpoint to verify the token is valid
@app.route('/authenticate')
def authenticate():
    resp = stytch_client.magic_links.authenticate(request.args.get('token'))

    if resp.status_code != 200:
        print(resp)
        return "something went wrong authenticating token"
    return render_template('loggedIn.html')


# handles the logout endpoint
@app.route('/logout')
def logout():
    return render_template('loggedOut.html')


# run's the app on the provided host & port
if __name__ == '__main__':
    # in production you would want to make sure to disable debugging
    app.run(host=HOST, port=PORT, debug=True)
