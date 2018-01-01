from helpers import aeshelper
from objects import glob

def bake(submit, score):
    #glob.db.execute("") #Get process list and post it into cakes table ;3
    detection = []

    if "osuver" in submit.request.arguments:
        aeskey = "osu!-scoreburgr---------{}".format(submit.get_argument("osuver"))
    else:
        aeskey = "h89f2-890h2h89b34g-h80g134n90133"
    iv = submit.get_argument("iv")
    try:
        pl = aeshelper.decryptRinjdael(aeskey, iv, submit.get_argument("pl"), True).split("\n")

        

    except:
        detection.append("Unable to decrypt process list (Hacked)")
