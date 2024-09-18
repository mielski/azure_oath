import os
import secrets
from urllib import parse
from dotenv import load_dotenv
import pkce
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, session)

from url_request_meta import UrlRequestMeta

load_dotenv()

AUTHORIZE_URL = "https://dev-a5q1ydqw73oghxli.us.auth0.com/authorize"
TOKEN_URL = "https://dev-a5q1ydqw73oghxli.us.auth0.com/oauth/token"
CLIENT_ID = "c4sFmk9OlnitsgqXaryE180II1i02B15"
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

app.jinja_options = {"trim_blocks": True,
                     "lstrip_blocks": True}


@app.before_request
def pre_fill_session_keys():
    for key in ("code_verifier", "code_challenge"):
        if key not in session:
            session[key] = ""

@app.route('/')
def index():
    authorize_params = {"response_type": "code",
                       "client_id": CLIENT_ID,
                       "state": '1234567890abcd',
                       "redirect_uri": "https://example-app.com/redirect",
                       "code_challenge": session["code_challenge"],
                       "code_challenge_method": "S256"}

    # TODO update input variables to pass urls and their arguments
    url_authorize = UrlRequestMeta(AUTHORIZE_URL, "GET",
                                   params=authorize_params)

    return render_template('authentication_code_flow.html', url_authorize=url_authorize)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/output', methods=['GET'])
def output():

    return render_template('output.html')

@app.route('/pkce', methods=['GET', 'POST'])
def pkce_gen():
    """create pcke code on post request, show pkce variables on get."""
    if request.method == "POST":
        # create a new pkce pair
        code_verifier, code_challenge = pkce.generate_pkce_pair(60)
        session["code_verifier"] = code_verifier
        session["code_challenge"] = code_challenge

    return render_template('create_pkce.html')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
