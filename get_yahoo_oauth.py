import config  # import yahoo API keys from config.py

import json

yahoo_app_id = config.yahoo_app_id
yahoo_client_id = config.yahoo_client_id
yahoo_client_secret = config.yahoo_client_secret

creds = {'consumer_key': yahoo_client_id, 'consumer_secret': yahoo_client_secret}
with open("oauth2.json", "w") as f:
    f.write(json.dumps(creds))