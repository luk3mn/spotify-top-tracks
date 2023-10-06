from dotenv import dotenv_values
from utils.get_data import GetData
from utils.data_struct import DataStruct
from utils.access_token import AccessToken
from utils.data_validation import DataValidation
from utils.data_load import DataLoad
from flask import Flask, request, redirect, session, url_for
import urllib

### API ACCESS CREDENTIALS
credentials = dotenv_values(".env")
SPOTIFY_CLIENT_ID = credentials['CLIENT_ID']
SPOTIFY_CLIENT_SECRET = credentials['CLIENT_SECRET']

### URL APIs
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'
REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
AUTH_URL = 'https://accounts.spotify.com/authorize'

### ACCESS TOKEN
TOKEN = 'access_token'

app = Flask(__name__)
app.secret_key = '8fy*ḧ#h*%YHD'
app.config['SESSION_COOKIE_NAME'] = 'Spotify Access'

get_data = GetData(api_url=API_BASE_URL)
data = DataStruct()
access_token = AccessToken(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=REDIRECT_URI, token_url=TOKEN_URL)

@app.route('/')
def authorization():
    scope = 'user-read-recently-played user-top-read'

    params = {
        'client_id': SPOTIFY_CLIENT_ID,
        'response_type': 'code', # spotify documentation info to set 'code' here 
        'redirect_uri': REDIRECT_URI, # to redirect if something wrong happen
        'scope': scope # our permissions from the user
    }

    auth_url = f'{AUTH_URL}?{urllib.parse.urlencode(params)}'
    return redirect(auth_url) # return to navigator after authentication

@app.route('/redirect')
def redirect_page():
    try:
        session.clear()
        code = request.args['code']
        new_token = access_token.get_token(code=code).json()['access_token']
        session[TOKEN] = new_token

        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "Authorization" : "Bearer {token}".format(token=new_token)
        }

    except:
        return redirect('/') # if access token doesn't exist, redirect to get a new authentication
    
    get_user_top_items = get_data.get_user_top_items(headers=headers, type='tracks', limit=50)
    df = data.struct_top_items()
    print(df)
    data_validation = DataValidation(df)
    data_validation.isempty()
    data_validation.isnull()
    data_validation.isuinique(column_name='song_id')

    data_load = DataLoad(df=df)
    data_load.sql_store()

    return get_user_top_items

if __name__ == '__main__':
    app.run(debug=True)