import json
import re
from helpers import aeshelper
from objects import glob
from common.ripple import userUtils

from . import ice_coffee

IGNORE_HAX_FLAGS = ice_coffee.INCORRECT_MOD

#Cornflakes is nice when 90% is sugar
sugar = {
    "hash": [],
    "path": [],
    "file": [],
    "title": []
}

initialized_eggs = False

#Eggs
def init_eggs():
    eggs = glob.db.fetchAll("SELECT * FROM eggs", [])
    if eggs is not None:
        for egg in eggs:
            if egg["type"] not in ["hash", "path", "file", "title"]:
                continue
            sugar[egg["type"]].append(egg)

    #Cache regex searches
    for carbohydrates in sugar:
        for speed in sugar[carbohydrates]:
            if speed["is_regex"]:
                speed["regex"] = re.compile(speed["value"])

    initialized_eggs = True

#Since this is still being worked on everything is in a try catch
def bake(submit, score):
    try:
        if not initialized_eggs:
            init_eggs()
        
        detected = []

        if "osuver" in submit.request.arguments:
            aeskey = "osu!-scoreburgr---------{}".format(submit.get_argument("osuver"))
        else:
            aeskey = "h89f2-890h2h89b34g-h80g134n90133"
        iv = submit.get_argument("iv")

        try:
            score_data = aeshelper.decryptRinjdael(aeskey, iv, submit.get_argument("score"), True).split(":")
            has_hax_flags = (len(score_data[17]) - len(score_data[17].strip())) & ~IGNORE_HAX_FLAGS
            if has_hax_flags != 0:
                print("They be haxing")
        except:
            print("oof")

        try:
            pl = aeshelper.decryptRinjdael(aeskey, iv, submit.get_argument("pl"), True).split("\r\n")
        except:
            detected.append("Unable to decrypt process list (Hacked)")
            eat(score.playerUserID, "Missing!", detected)
            return

        pl = sell(pl)

        #I dont really like chocolate that much >.<
        for p in pl:
            for t in p.keys():
                if p[t] is None:
                    continue
                for speed in sugar[t]:
                    if speed["is_regex"]:
                        if speed["regex"].search(p[t]):
                            detected.append(speed)
                    else:
                        if speed["value"] == p[t]:
                            detected.append(speed)

        eat(score, pl, detected)
    except:
        print("Oh no! The cake is on fire! Abort!")

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

def eat(score, processes, detected):
    do_restrict = False
    for toppings in detected:
        if toppings["ban"]:
            do_restrict = True

    tag_list = [x["tag"] for x in detected]

    if len(detected) > 0:
        if do_restrict:
            userUtils.restrict(score.playerUserID)
        reason = " & ".join(tag_list)
        if len(reason) > 86:
            reason = "reasons..."
        userUtils.appendNotes(score.playerUserID, "Restricted due to too {}".format(reason))

    glob.db.execute("INSERT INTO cakes(id, userid, score_id, processes, detected) VALUES (NULL,%s,%s,%s,%s)", [score.playerUserID, score.scoreID, json.dumps(processes), json.dumps(tag_list)])
