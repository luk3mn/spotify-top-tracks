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
app.secret_key = credentials['SECRET_KEY']
app.config['SESSION_COOKIE_NAME'] = 'Spotify Access'

data_struct = DataStruct()
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

    ### SHORT TERM TRACKS
    get_data.get_users_top_items(time_range='short_term', filename='short_term.json')
    df_st = data_struct.struct_top_items(filename='short_term.json')

    data_validation = DataValidation(df_st)
    data_validation.isempty()
    data_validation.isnull()
    data_validation.isuinique(column_name='song_id')

    data_load_st = DataLoad(df=df_st, tb_name='short_term_tracks')
    data_load_st.sql_store()

    ### MEDIUM TERM TRACKS
    get_data.get_users_top_items(time_range='medium_term', filename='medium_term.json', limit=50)
    df_mt = data_struct.struct_top_items(filename='medium_term.json')

    data_validation = DataValidation(df_mt)
    data_validation.isempty()
    data_validation.isnull()
    data_validation.isuinique(column_name='song_id')

    data_load_mt = DataLoad(df=df_mt, tb_name='medium_term_tracks')
    data_load_mt.sql_store()

    ### LONG TERM TRACKS
    get_data.get_users_top_items(time_range='long_term', filename='long_term.json', limit=30)
    df_lt = data_struct.struct_top_items(filename='long_term.json')

    data_validation = DataValidation(df_lt)
    data_validation.isempty()
    data_validation.isnull()
    data_validation.isuinique(column_name='song_id')

    data_load_lt = DataLoad(df=df_lt, tb_name='long_term_tracks')
    data_load_lt.sql_store()

    return redirect('/about')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/short-term-tracks')
def short_term_tracks():
    tracks = search_db(table='short_term_tracks')
    global uris
    uris = data_struct.get_tracks_uris(filename='short_term.json')
    return render_template('content.html', tracks=tracks)

@app.route('/medium-term-tracks')
def medium_term_tracks():
    tracks = search_db(table='medium_term_tracks')
    global uris
    uris = data_struct.get_tracks_uris(filename='medium_term.json')
    return render_template('content.html', tracks=tracks)

@app.route('/long-term-tracks')
def long_term_tracks():
    tracks = search_db(table='long_term_tracks')
    global uris
    uris = data_struct.get_tracks_uris(filename='long_term.json')
    return render_template('content.html', tracks=tracks)

def search_db(table):
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {}'.format(table))
    return cursor.fetchall()

""" FIX IT
- Forbid to creating playlist by URL
- Improve application flow to remove error on playlist (maybe improving rotes)
"""
@app.route("/create_playlist", methods=['GET', 'POST'])
def create_playlist():

    if request.method == 'POST':
        playlist_name = request.form['name']
        playlist_desc = request.form['description']
    
    if playlist_name: 
        pl = playlist.create_playlist(name=playlist_name, description=playlist_desc)
        playlist.populate_playlist(playlist_id=pl['id'], uris=uris)
    else:
        return 'Please, enter a value for your playlist name'
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
