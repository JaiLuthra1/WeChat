import json 
import requests
import time
from API import VoiceHandler

# TODO: Jai Luthra
TOKEN = "1547146270:AAETQgCJBWkc60fomzJOIgSVgY9GE4YbfYs"
# TODO: Hide token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_voice_input(file_id):
    url = URL + "getFile?file_id=" + file_id
    js = get_json_from_url(url)
    file_path = js["result"]["file_path"]
    url="https://api.telegram.org/file/bot"+TOKEN+"/"+file_path
    r=requests.get(url)
    with open("dummy.oga",'wb') as f: 
        f.write(r.content)
    f.close()
    # ?
    # return VoiceHandler.ExtractText("dummy.oga")
    # TODO: Get text from dummy.oga


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def start_bot():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
        except:
            try:
                voice = update["message"]["voice"]
                text=get_voice_input(voice["file_id"])
            except:
                text="INVALID"
        chat = update["message"]["chat"]["id"]
        if text.startswith("/"):
            # Command
            response = "Command not supported"
        else:
            # TODO: Ayushman Dixit
            response = "Hi, you sent \"{}\"".format(text)
            # TODO: get response
        send_message(response, chat)