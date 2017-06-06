from flask import Flask, request, redirect, render_template, url_for
from rauth.service import OAuth2Service
from app import app
import os, json

spotify = OAuth2Service(name='spotify',
                     authorize_url='https://accounts.spotify.com/authorize',
                     access_token_url='https://accounts.spotify.com/api/token',
                     client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                     client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                     base_url='https://api.spotify.com/')

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
        return redirect_uri(url_for('welcome'))

    redirect_uri = url_for('authorized', _external=True)
    data = {'grant_type': 'authorization_code',
            'code': request.args['code'],
            'redirect_uri': redirect_uri}

    return redirect(url_for('web'))

@app.route('/artist_web')
def web():
    return 'Hello!'
