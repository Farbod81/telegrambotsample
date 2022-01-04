
# you should see this text in new commit and push.



# PART 1
import requests
import json
url = "https://api.telegram.org/bot5047047049:AAEgMGxGztL43G7P01_fZ73zMdb29d_ibdE/"
from flask import Flask
from flask import Request
from flask import Response
import os           # for using server.


app = Flask(__name__)

# ALL THE BASIC FUNCTIONS WE NEED:
def get_allupdates():
    result = requests.get(url + "getUpdates")
    return result.json()

def get_last_update(allupdate):
    return allupdate["result"][-1]


def get_last_message(allupdate):
    return allupdate["result"][-1]["message"]["text"]




def get_chat_id(update):
    return update["message"]["chat"]["id"]


def send_message(chat_id, text, notif = False):

    send_data = {
        "chat_id" : chat_id,
        "text" : text,
        "disable_notification" : notif
    }

    result = requests.post(url + "sendMessage", send_data)
    return result





@app.route("/", method = ["POST", "GET"])
def index():
    if Request.method == "POST":
        msg =  Request.get_json()
        chat_id = get_chat_id(msg)
        text = msg["message"].get("text", "")



        if text == "/start":
            send_message(chat_id, "Welcome:)")
            return Response("ok", status=200)   # in the github main file this line has been removed. So... you may have to remove it as well.




# new "username"
        elif "new" in text:
            contacts = read_json()
            username = msg["message"]["from"]["username"]
            if username not in contacts.keys():
                contacts[username] = []
            contact = text.split(maxsplit=1)[1]
            contacts[username].append(contact)
            write_json(contacts)
            send_message(chat_id, f"{contact} has been added to your contactlist.")



        elif text == "list":
            contacts = read_json()
            username = msg["message"]["from"]["username"]
            if username not in contacts.keys():
                send_message(chat_id, "No contact exist!")
            else:
                for contact in contacts:
                    send_message(chat_id, contact)

    else:
        return "<h1> Hi welcome to our webpage :) </h1>"



def write_json(data, filename = "contactlist.json"):
    with open(filename, "w") as target:
        json.dump(data, target, indent=4, ensure_ascii=False)         # indent is for those spaces before for example "if" in line 44.

def read_json(filename = "contactlist.json"):           # write_json and read_json are use for save our dictionary on the server and read it from that.
    with open(filename, "r") as target:
        ourdict = json.load(target)
        return ourdict






write_json({}) # delete all the previous data. it's optional.
# app.run(debug=True) # we can use debuge if we want to run it on system and not on the server.
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))







# data = get_allupdates()
# print(get_last_message(data))
# if get_last_message(data) == "hi":
#     send_message(get_chat_id(get_last_update(data)), "hello")
# # else:
# #     send_message(get_chat_id(get_last_update(data)), "say hi first!")
















