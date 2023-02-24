import spotipy
import pandas as pd
import requests
import os
from dotenv import load_dotenv


load_dotenv()

username = 	"Srivatsan Thiruvengadam"
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-recently-played'

token = spotipy.util.prompt_for_user_token(username=username, 
                                   scope=scope, 
                                   client_id=client_id,   
                                   client_secret=client_secret,     
                                   redirect_uri=redirect_uri)

sp = spotipy.Spotify(token)
ani = sp.artist('4zCH9qm4R2DADamUHMCa6O')
print(ani)
