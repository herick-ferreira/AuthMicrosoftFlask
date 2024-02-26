from datetime import datetime
import base64
import requests
import app_config

# Checked login

def check_login(msal_app, session):

    if ("access_token" not in  list(session.keys())) or ("exp" not in list(session.keys())) or ('username' not in list(session.keys())):
       return False

    if str(session['exp']) == "None" or str(session["access_token"])  == "None" or str(session["username"])  == "None":
        return False
    
    if not 'username' in session.keys(): return False

    list_accounts = msal_app.get_accounts()

    if len(list_accounts) > 0: list_accounts = [v['username']  for v in list_accounts if 'username' in v.keys()]
    if str(session['username']) not in list_accounts: return [False, session]


    if datetime.timestamp(datetime.now()) > float(session['exp']):
        token = msal_app.acquire_token_by_refresh_token(
            scopes=app_config.SCOPE_MS,
            refresh_token = str(session["refresh_token"])

        )

        if "error" in token:
            return [False, session]


        session["access_token"] = token.get("access_token")

        try: session['exp'] = token['client_info']['id_token_claims']['exp']
        except (KeyError, TypeError): session['exp'] = None


        try: session['username'] = token['client_info']['id_token_claims']['preferred_username']
        except (KeyError, TypeError): session['username'] = None


        try: session['name'] = token['id_token_claims']['name']
        except (KeyError, TypeError):  session['name'] = ''

    
    return True











# Get Image Profile

def get_picture(token): 

    with open(".//static//profile.png", "rb") as file:

        bytes_photo = file.read()

    encode_photo =  base64.b64encode(bytes_photo).decode('utf-8')

    
    req_photo = requests.get(
            "https://graph.microsoft.com/v1.0/me/photo/$value",
            headers={'Authorization': 'Bearer ' + token},
            timeout=30,
        )

    if req_photo.status_code == 200:

        bytes_photo = req_photo.content

        encode_photo =  base64.b64encode(bytes_photo).decode('utf-8')
        


    return encode_photo






