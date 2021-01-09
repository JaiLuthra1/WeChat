import json 
import requests
import time
from API import VoiceHandler

# TODO: Hide token
BOT_NAME = "Il_servitore"
BOT_CREATOR = "IIT Mandi"
TOKEN = "1568387409:AAHzWMtLieiNtzbQcCRyqXI9zsL3oV5BjiQ"
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
    return VoiceHandler.ExtractText("dummy.oga")


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
        # print(update)
        try:
            message = update["message"]
        except:
            message = update["edited_message"]    
        chat = message["chat"]["id"]
        try:
            text = message["text"]
        except:
            try:
                voice = message["voice"]
                text=get_voice_input(voice["file_id"])
            except Exception as e:
                send_message("Sorry, I didn't get you.", chat)
                continue

        if text.startswith("/"):
            # Command
            if(text=="/start"):
                response=f"Hello! I am {BOT_NAME}. I can help you with any queries. To know the usage send \"/usage\""
            elif(text=="/usage"):
                response=f"I am {BOT_NAME}.\n\n- I can understand text and voice messages.\n\n - Currently, I know only English. I am learning a few more languages :)"
            else:
                response = "Command not supported. Please check usage."
        else:
            # TODO: Get response
            response = "Hi, you sent \"{}\"".format(text)
        send_message(response, chat)