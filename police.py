import os
import json
import requests

from common.ripple import userUtils

#Config cache
config = None

def call(m, *args, user_id = None):
    try:
        if config is None:
            cache_config()

        username = None
        if user_id is not None:
            username = userUtils.getUsername(user_id)
        
        m = m.replace("USERNAME()", username)

        if config["webhook"]["enable"]:
            data = {"text": m}
            response = requests.post(
                config["webhook"]["url"],
                json=data
            )
            if response.status_code != 200:
                raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
    except Exception as e:
        s_print("Unable to call police; {}".format(str(e)))
    
    s_print(m)

def cache_config():
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
        config = json.load(f)
    s_print("Config was loaded. We are ready to go!")

def s_print(m):
    print("[Police] {}".format(m))