import requests
import pokebase as pb
from datetime import datetime

#TODO this is, at the moment, just a collection of experiments.

def create_request(url, params=[], headers=[]):
    try:
        return requests.get(url, params=params, headers=headers)
    except BaseException:
        print(BaseException)
    return None

def write_debug_log(debug_text, filepath = ''):
    timestamp = datetime.now()
    if filepath == '':
        filepath = timestamp.strftime('%Y%m%d%H%M%S_Debug.txt')
    with open(filepath, 'w+', 'utf-8') as debugFile:
        debugFile.write(f'{timestamp.strftime("%Y.%m.%d")}\n{timestamp.strftime("%H:%M:%S")}\n\n{debug_text}')
    return

def dbygo_card():
    apireturn = create_request(r"https://db.ygorganization.com/data/card/15110")

    print(apireturn.json()["cardData"]["en"]["name"])
    # scribe.writeDebugLog(apireturn.text)
    return


def dbpoke():
    apireturn1 = pb.pokemon("gardevoir")
    print(apireturn1.__dir__())
    #apireturn=pb.SpriteResource('pokemon', apireturn1.height)
    #print(apireturn)
