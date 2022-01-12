# stytch-python-magic-links

##### Prerequisites
Ensure you have pip, python and virtualenv installed

##### 1. Clone the repository.
Close this repository and navigate to the folder with the source code on your machine in a terminal window.

##### 2. Setup a virtualenv
We suggest creating a [virtualenv](https://docs.python.org/3/library/venv.html) and activating it to avoid installing dependencies globally

- `virtualenv -p python3 venv`
- `source venv/bin/activate`

##### 3. Install dependencies:
`pip install -r requirements.txt`

##### 4. Set ENV vars
Set your project ID and secret in the `.env` file.

##### 5. Add Magic Link URL
Visit https://stytch.com/dashboard/redirect-urls to add
`http://localhost:3000/authenticate` as a valid sign-up and login URL.

##### 6. Run the Server

Run `python3 main.py`

##### 7. Login

Visit `http://localhost:4567` and login with your email.
Then check for the Stytch email and click the sign in button.
You should be signed in!
