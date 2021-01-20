import json
import requests
import time
from API import VoiceHandler, WeatherHandler
from googlesearch import search

from model import chatbot_response
import random
import subprocess


# TODO: Hide token
BOT_NAME = "Il_servitore"
BOT_CREATOR = "IIT Mandi"
TOKEN = "1568387409:AAHzWMtLieiNtzbQcCRyqXI9zsL3oV5BjiQ"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
AUDIO_OUTPUT = []


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def coin_toss():
    if random.randint(0, 1) == 0:
        return "HEADS"
    return "TAILS"


def roll_a_dice():
    return str(random.randint(0, 5) + 1)


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def getaudiomode(chat):
    global AUDIO_OUTPUT
    if chat in AUDIO_OUTPUT:
        return True
    return False


def setaudiomode(chat, state):
    global AUDIO_OUTPUT
    if state == False and chat in AUDIO_OUTPUT:
        AUDIO_OUTPUT.remove(chat)
    if state == True and chat not in AUDIO_OUTPUT:
        AUDIO_OUTPUT.append(chat)


def get_voice_input(file_id):
    url = URL + "getFile?file_id=" + file_id
    js = get_json_from_url(url)
    file_path = js["result"]["file_path"]
    url = "https://api.telegram.org/file/bot" + TOKEN + "/" + file_path
    r = requests.get(url)
    with open("dummy.oga", "wb") as f:
        f.write(r.content)
    f.close()
    return VoiceHandler.ExtractText("dummy.oga")


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def google_search(query, max_results=1):
    result = ""

    for j in search(query, tld="co.in", num=max_results, stop=max_results, pause=2):
        result += j + "\n"

    return result


def send_message(text, chat_id, reply_id):
    url = f"{URL}sendMessage?text={text}&chat_id={chat_id}&reply_to_message_id={reply_id}&disable_web_page_preview=True"
    get_url(url)


def sendvoice(chat_id, reply_id):
    with open("file.mp3", "rb") as audio:
        payload = {
            "chat_id": chat_id,
            "title": "file.mp3",
            "parse_mode": "HTML",
            "reply_to_message_id": reply_id,
        }
        files = {
            "audio": audio.read(),
        }
        resp = requests.post(
            "https://api.telegram.org/bot{token}/sendAudio".format(token=TOKEN),
            data=payload,
            files=files,
        ).json()
    subprocess.run(["rm", "file.mp3"])


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
        reply_id = message["message_id"]
        # print(message)
        # print(reply_id)
        try:
            text = message["text"]
        except:
            try:
                voice = message["voice"]
                text = get_voice_input(voice["file_id"])
            except Exception as e:
                send_message("Sorry, I didn't get you.", chat, reply_id)
                continue

        if text.startswith("/"):
            # Command
            if text == "/start":
                try:
                    name = (
                        f' {message["from"]["first_name"]} {message["from"]["last_name"]}'
                    )
                except:
                    name=""
                response = f'Hello{name}! I am {BOT_NAME}. To know the usage send "/usage" or "/help"'
            elif text == "/help" or text == "/usage":
                response = f"""I am {BOT_NAME}. I can help you with your queries. Send me a message or a command.
Message that begins with / is a command.   \n
Some of the supported commands are         \n
- /start to start the bot                  \n
- /help to get help                        \n
- /audio to toggle audio mode(default off) \n
- /coin_toss to toss a coin                \n
- /roll_a_dice to roll a dice              \n
- /weather to know the weather             \n"""
            elif text == "/audio":
                if getaudiomode(chat) == False:
                    setaudiomode(chat, True)
                    response = "Audio turned ON"
                else:
                    setaudiomode(chat, False)
                    response = "Audio turned OFF"
            elif text == "/coin_toss":
                response = coin_toss()
            elif text == "/roll_a_dice":
                response = roll_a_dice()
            elif text == "/weather":
                response = WeatherHandler.WeatherHandler()
            else:
                response = 'Command not supported. Please check "usage".'
            send_message(response, chat, reply_id)
            if AUDIO_OUTPUT and response != "":
                VoiceHandler.get_audio_file(response)
                sendvoice(chat, reply_id)
        else:
            resp = ""
            g=""
            que,resp,cat = chatbot_response(text)
            try:
                cat=cat["context"][0]
                if cat == "iitmandi":
                    g = google_search(f"iit mandi {text}")
                elif cat == "programming":
                    g = google_search(text)
            except:
                g=""
            if g != "":
                response = f"{resp}\n\nHere is the link to the most similar page:\n{g}"
            else:
                response = resp
            send_message(response, chat, reply_id)
            if AUDIO_OUTPUT and resp != "":
                VoiceHandler.get_audio_file(resp)
                sendvoice(chat, reply_id)


start_bot()
