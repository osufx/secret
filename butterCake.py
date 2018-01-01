import json
from helpers import aeshelper
from objects import glob

def bake(submit, score):
    #glob.db.execute("") #Get process list and post it into cakes table ;3
    detected = []

    if "osuver" in submit.request.arguments:
        aeskey = "osu!-scoreburgr---------{}".format(submit.get_argument("osuver"))
    else:
        aeskey = "h89f2-890h2h89b34g-h80g134n90133"
    iv = submit.get_argument("iv")
    try:
        pl = aeshelper.decryptRinjdael(aeskey, iv, submit.get_argument("pl"), True).split("\n")
    except:
        detected.append("Unable to decrypt process list (Hacked)")
        eat(score.playerUserID, pl, detected)
        return
    
    
    #eat(score.playerUserID, pl, detected)

def eat(user_id, processes, detected):
    formatted_pl = []
    for p in processes: #Formats the process list
        t = p.split(" | ", 1)
        try:
            d = t[0].split(" ", 1)
            file_hash = '"{}"'.format(d[0])
            file_path = '"{}"'.format(d[1])
        except:
            file_hash = None
            file_path = None

        h = t[1].split(" (", 1)
        file_name = h[0]

        file_title = None
        if len(h[1]) > 1:
            file_title = '"{}"'.format(h[1][:-1])

        formatted_pl.append({"hash":file_hash, "path":file_path,
                             "file":file_name, "title":file_title})

    glob.db.execute("INSERT INTO cakes(id, userid, processes, detected) VALUES (NULL,%s,%s,%s)", [user_id, json.dumps(formatted_pl), json.dumps(detected)])
