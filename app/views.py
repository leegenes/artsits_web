from flask import Flask, request, redirect, render_template, url_for, session, flash
from rauth.service import OAuth2Service
from app import app, spotify_handler
# from . import spotify_handler
import json

spotify = OAuth2Service(name='spotify',
                     authorize_url='https://accounts.spotify.com/authorize',
                     access_token_url='https://accounts.spotify.com/api/token',
                     client_id='5cbabc9978fc41b8b05ed9dd4c03ed2c', # os.getenv('SPOTIFY_CLIENT_ID'),
                     client_secret='22c3ee302938487ca2bd2132c9dba461', #os.getenv('SPOTIFY_CLIENT_SECRET'),
                     base_url='https://api.spotify.com/')

d = {}

@app.route('/')
def welcome():
    return render_template('home.html',
                            title='home')

@app.route('/authorize')
def authorize():
    redirect_uri = url_for('authorized', _external=True)
    params = {  'response_type': 'code',
                'redirect_uri': redirect_uri,
                'scope': 'user-top-read'
                }

    return redirect(spotify.get_authorize_url(**params))

@app.route('/authorized')
def authorized():
    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('welcome'))

    redirect_uri = url_for('authorized', _external=True)
    data = {'grant_type': 'authorization_code',
            'code': request.args['code'],
            'redirect_uri': redirect_uri}

    def byte_decoder(byte_load):
        return json.loads(byte_load.decode())

    oauth_session = spotify.get_auth_session(data=data, decoder=byte_decoder)

    data = spotify_handler.SpotifyData(oauth_session)
    d['top'] = data.get_top_artists()
    d['relations'] = data.get_relations()

    return redirect(url_for('web'))

@app.route('/artist_web')
def web():
    return render_template('web.html',
                            top_artists=d['top'],
                            relations=d['relations'])
