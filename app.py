from flask import Flask, request
import requests
import json
import config
import os
from pic_content import sql_crawler
from create_pic import pic_creator

app = Flask(__name__)
crawler = sql_crawler("msg_db.db")
pic_create = pic_creator(crawler)


# Sends the created picture 
def send_pic(senderPsid):
    print(os.path.basename)
    payload = {
        'recipient': (None, {"id": senderPsid}),
        'message': (None, {"attachment": {"type": "image", "payload": {}}}),
    }
    files = {
        'filedata': ("final", pic_create.s3_load(), 'image/png')
    }
    url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(config.PAGE_ACCESS_TOKEN)
    response = requests.post(url, data=payload, files=files)
    print(response.text.encode('utf8'))

# Sends received message back to see if webhook works
def sendMessage(senderPsid, response, type = "message"):
    if type == "message":
        payload = {
        'recipient': {'id': senderPsid},
        'message': response,
        'messaging_type': 'RESPONSE'
        }
        url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(config.PAGE_ACCESS_TOKEN)
        response = requests.post(url, json=payload)
        print(response.text.encode('utf8'))


def handleMessage(senderPsid, receivedMessage):
    print('We entered the HANDLE MESSAGE FUNCTION')
    if 'text' in receivedMessage:
        toSend = receivedMessage['text']
        chatbotResponse = "Your message was: " + toSend + "."
        response = {"text": chatbotResponse }
        pic = pic_create.create_pic()
        pic_create.s3_put(pic)
        send_pic(senderPsid)
        #sendMessage(senderPsid, response,type= "message")
    else:
        response = {"text": 'Wrong format.'}
        sendMessage(senderPsid, response,type = "message")


@app.route('/webhook', methods=["GET", "POST"])
def webhook():
    if request.method == 'GET':
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == config.VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')
                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403

        return 'SOMETHING', 200


    if request.method == 'POST':
        payload = request.json
        print(payload)
        #do something else
        data = request.data
        body = json.loads(data.decode('utf-8'))

        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                print(webhookEvent)

                senderPsid = webhookEvent['sender']['id']
                print('Sender PSID: {}'.format(senderPsid))
                if 'message' in webhookEvent:
                    handleMessage(senderPsid, webhookEvent['message'])
                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404


if __name__ == '__main__':
    app.run()
