from flask import Flask, redirect, render_template, session, url_for, request
from datetime import datetime
from pytz import timezone
from werkzeug.middleware.proxy_fix import ProxyFix
import app_config
from warnings import filterwarnings
from functions import get_picture, check_login
from msal import ConfidentialClientApplication




filterwarnings('ignore')

app = Flask(__name__)
app.config.from_object(app_config)

tz = timezone('Brazil/East')
year = f'{datetime.now(tz=tz):%Y}'

app.secret_key =  app.config["SECRET_SESSION"]

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)




# Microsoft
msal_app = ConfidentialClientApplication(
    app.config["CLIENT_ID_MS"],
    authority=app.config["AUTHORITY_MS"],
    client_credential=app.config["CLIENT_SECRET_MS"]
)



# ROUTES

@app.route("/")
def page_home():
    return render_template('index.html', year=year)


@app.route("/login")
def login():

    check_log = check_login(msal_app, session)

    if check_log: 
        return redirect(url_for("page_protect"))

    auth_url = msal_app.get_authorization_request_url(
        scopes=app_config.SCOPE_MS,
        redirect_uri=url_for('callback', _external=True),
        state=session.get("state")
    )

    return redirect(auth_url)



@app.route("/callback")
def callback():
   
    token = msal_app.acquire_token_by_authorization_code(
        request.args["code"],
        scopes=app_config.SCOPE_MS,
        redirect_uri=url_for('callback', _external=True)
    )


    if "error" in token:
        return render_template("index.html")

    session['platform'] = 'microsoft'    

    session["access_token"] = token.get("access_token")

    session["refresh_token"] = token.get("refresh_token")
    
    try:  session['exp'] = token['id_token_claims']['exp']
    except (KeyError, TypeError):  session['exp'] = None

    try:  session['name'] = token['id_token_claims']['name']
    except (KeyError, TypeError):  session['name'] = ''

    try:  session['sub'] = token['id_token_claims']['sub']
    except (KeyError, TypeError):  return redirect(url_for("page_home"))


    try:  session['username'] = token['id_token_claims']['preferred_username']
    except (KeyError, TypeError):  session['username'] = None

    session.permanent = True

    return redirect(url_for("page_protect"))



@app.route('/protect')
def page_protect():
    check_log = check_login(msal_app, session)

    if not check_log: return redirect(url_for("page_home"))


    if not 'picture' in session:

        picture = get_picture(session['access_token'])
        session['picture'] = picture
        

    name = session['name'] if 'name' in session else ''



    return render_template('protect.html',picture=session['picture'], name=name)





@app.route('/logout')
def logout():
    
    # Clear the user's session
    session.clear()
    return redirect(f'{app.config["AUTHORITY_MS"]}/oauth2/v2.0/logout?post_logout_redirect_uri={url_for("page_home", _external=True)}')



if __name__ == '__main__':
     app.run(debug=True)