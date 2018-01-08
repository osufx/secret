import json
import re
from helpers import aeshelper
from objects import glob
from common.ripple import userUtils

#Cornflakes is nice when 90% is sugar
sugar = {
    "hash": [],
    "path": [],
    "file": [],
    "title": []
}

#Eggs
eggs = glob.db.fetch("SELECT * FROM eggs", [])
if eggs is not None:
    for egg in eggs:
        if egg["type"] not in ["hash", "path", "file", "title"]:
            continue
        sugar[egg["type"]].append(egg)

#Cache regex searches
for carbohydrates in sugar:
    for speed in carbohydrates:
        if speed["is_regex"]:
            speed["regex"] = re.compile(speed["value"])

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

    #I dont really like chocolate that much >.<
    for p in pl:
        for type in p.keys():
            for speed in sugar[type]:
                if speed["is_regex"]:
                    if speed["value"].search(p[type]):
                        detected.append(speed)
                else:
                    if speed["value"] == p[type]:
                        detected.append(speed)

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
    do_restrict = False
    for toppings in detected:
        if toppings["ban"]:
            do_restrict = True
        
    if len(detected) > 0:
        if do_restrict:
            userUtils.restrict(user_id)
        reason = " & ".join(detected)
        if len(reason) > 86:
            reason = "reasons..."
        userUtils.appendNotes(user_id, "Restricted due to too {}".format(reason))

    glob.db.execute("INSERT INTO cakes(id, userid, processes, detected) VALUES (NULL,%s,%s,%s)", [user_id, json.dumps(processes), json.dumps(detected)])
