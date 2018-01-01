import json
import re
from helpers import aeshelper
from objects import glob

#Use this so we dont blow up the machine
regex_cache = {}
sugar = None

#Magic config
with open("secret/sugar.json", "r") as f:
    sugar = json.load(f)

#Cache regex searches
for x in sugar["title"].keys():
    regex_cache[x] = re.compile(x)

def bake(submit, score):
    detected = []

    if "osuver" in submit.request.arguments:
        aeskey = "osu!-scoreburgr---------{}".format(submit.get_argument("osuver"))
    else:
        aeskey = "h89f2-890h2h89b34g-h80g134n90133"
    iv = submit.get_argument("iv")
    try:
        pl = aeshelper.decryptRinjdael(aeskey, iv, submit.get_argument("pl"), True).split("\r\n")
    except:
        detected.append("Unable to decrypt process list (Hacked)")
        eat(score.playerUserID, "Missing!", detected)
        return

    pl = sell(pl)

    #Search thru known hacks list
    for p in pl:
        if p["hash"] is not None:
            for x in sugar["hash"].keys():
                if x == p["hash"]:
                    detected.append(sugar["hash"][x])

        if p["title"] is not None:
            for x in regex_cache.keys():
                if regex_cache[x].search(p["title"]) is not None:
                    detected.append(sugar["title"][x])

    eat(score.playerUserID, pl, detected)

def sell(processes):
    formatted_pl = []
    for p in processes: #Formats the process list
        try:
            t = p.split(" | ", 1)
            try:
                d = t[0].split(" ", 1)
                file_hash = d[0]
                file_path = d[1]
            except:
                file_hash = None
                file_path = None

            h = t[1].split(" (", 1)
            file_name = h[0]

            file_title = None
            if len(h[1]) > 1:
                file_title = h[1][:-1]

            formatted_pl.append({"hash":file_hash, "path":file_path,
                                 "file":file_name, "title":file_title})
        except:
            continue

    return formatted_pl

def eat(user_id, processes, detected):
    glob.db.execute("INSERT INTO cakes(id, userid, processes, detected) VALUES (NULL,%s,%s,%s)", [user_id, json.dumps(processes), json.dumps(detected)])
