import json 
import requests
import time

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
            # TODO: Dipanshu Verma
            # Exception handling for non-text
            text="INVALID"
            # TODO: Add voice message handling
        chat = update["message"]["chat"]["id"]
        if text.startswith("/"):
            # Command
            response = "Command not supported"
        else:
            # TODO: Ayushman Dixit
            response = "Hi, you sent \"{}\"".format(text)
            # TODO: get response
        send_message(response, chat)
