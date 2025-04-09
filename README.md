# stytch-python-magic-links

##### Prerequisites

Ensure you have pip, python and virtualenv installed

##### 1. Clone the repository.

Close this repository and navigate to the folder with the source code on your machine in a terminal window.

##### 2. Setup a virtualenv

We suggest creating a [virtualenv](https://docs.python.org/3/library/venv.html) and activating it to avoid installing dependencies globally

- `python3 -m venv venv`
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
If you're interested in running async instead, run `python3 main_async.py`

##### 7. Login

Visit `http://localhost:3000` and login with your email.
Then check for the Stytch email and click the sign in button.
You should be signed in!

## Next steps

This example app showcases a small portion of what you can accomplish with Stytch. Here are a few ideas to explore:

1. Add additional login methods like [OAuth](https://stytch.com/docs/api/oauth-google-start) or [Passwords](https://stytch.com/docs/api/password-create).
2. Secure your app further by building MFA authentication using methods like [OTP](https://stytch.com/docs/api/send-otp-by-sms).

## Get help and join the community

#### :speech_balloon: Stytch community Slack

Join the discussion, ask questions, and suggest new features in our ​[Slack community](https://stytch.com/docs/resources/support/overview)!

#### :question: Need support?

Check out the [Stytch Forum](https://forum.stytch.com/) or email us at [support@stytch.com](mailto:support@stytch.com).
