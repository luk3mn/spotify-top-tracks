from dotenv import dotenv_values
from utils.get_data import GetData
from utils.data_struct import DataStruct
from utils.authorization import Authorization
from utils.data_validation import DataValidation
from utils.playlist import Playlist
from utils.data_load import DataLoad
from flask import Flask, request, redirect, session, url_for, render_template
import sqlite3

### API ACCESS CREDENTIALS
credentials = dotenv_values(".env")
SPOTIFY_CLIENT_ID = credentials['CLIENT_ID']
SPOTIFY_CLIENT_SECRET = credentials['CLIENT_SECRET']
SPOTIFY_USER_ID = credentials['USER_ID']

### URL APIs
TOKEN_URL = 'https://accounts.spotify.com/api/token'
ENDPOINT = 'https://api.spotify.com/v1/'
REDIRECT_URI = 'http://127.0.0.1:5000/redirect'

### ACCESS TOKEN
TOKEN = 'token'

app = Flask(__name__)
app.secret_key = '8fy*ḧ#h*%YHD'
app.config['SESSION_COOKIE_NAME'] = 'Spotify Access'

data = DataStruct()
get_authorization = Authorization(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=REDIRECT_URI, token_url=TOKEN_URL)
@app.route('/')
def authorization():
    auth_url = get_authorization.get_auth(scope='user-top-read playlist-modify-public playlist-modify-private')
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    try:
        session.clear()
        code = request.args['code']
        new_token = get_authorization.get_token(code=code).json()['access_token']
        session[TOKEN] = new_token

        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "Authorization" : "Bearer {token}".format(token=new_token)
        }

        get_data = GetData(endpoint=ENDPOINT, headers=headers)
        global playlist
        playlist = Playlist(headers=headers, user_id=SPOTIFY_USER_ID)

    except:
        return redirect('/') # if access token doesn't exist, redirect to get a new authentication
    
    ### Data Extract
    get_users_top_items = get_data.get_users_top_items(limit=50, offset=0)
    
    ### Data Transform
    df = data.struct_top_items()
    data_validation = DataValidation(df)
    data_validation.isempty()
    data_validation.isnull()
    data_validation.isuinique(column_name='song_id')
    print(df)

    ### Data Load
    data_load = DataLoad(df=df)
    data_load.sql_store()

    ### Create Playlist
    # pl = playlist.create_playlist(name='Rock on', description='Testing Spotify Playlist', public=False)
    # uris = data.get_tracks_uris()
    # playlist.populate_playlist(playlist_id=pl['id'], uris=uris)

    # return get_users_top_items
    return redirect('/application')
    # tracks = database()
    # return render_template('index.html', tracks=tracks)

@app.route('/application')
def application():

    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM my_played_tracks')
    tracks = cursor.fetchall()

    return render_template('index.html', tracks=tracks)

@app.route("/create_playlist", methods=['GET', 'POST'])
def create_playlist():

    if request.method == 'POST':
        playlist_name = request.form['name']
        playlist_desc = request.form['description']
        pl = playlist.create_playlist(name=playlist_name, description=playlist_desc, public=False)
        uris = data.get_tracks_uris()
        playlist.populate_playlist(playlist_id=pl['id'], uris=uris)

    return redirect('/application')

if __name__ == '__main__':
    app.run(debug=True)

    # https://kanchanardj.medium.com/redirecting-to-another-page-with-button-click-in-python-flask-c112a2a2304c