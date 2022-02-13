# Messenger Shitpost Bot

This bot reuses old conversations I had with my friends group. It matches random questions with random answers to create fun interactions in the style of Cards against humanity. It works via a Python Flask application that utilizes the Messenger Webhook for Facebook Applications. The Flask applicaiton runs on a Heroku server (https://dashboard.heroku.com/apps). The app itself uses AWS S3 bucket to store and load the created final picture that will be sent in the messenger chat.

### Screenshot of the messenger output

<img width="678" alt="image" src="https://user-images.githubusercontent.com/79012119/153772041-74582f16-2979-4b71-83d0-63ec4f800b23.png">

## How to run

1. Create you Facebook app on https://developers.facebook.com/ and connect it to your Facebook account. Find/create the config variables featured in **config.py** following the instructions here: https://developers.facebook.com/docs/pages/access-tokens/.
2. Download your Messenger conversations from https://www.facebook.com/dyi/?referrer=yfi_settings in a JSON format. Choose one group chat and place the jsons containing the chat to the "convo" folder.
3. Run the **create_db.py** file to load the conversations into a sqlite database.
4. Push the Flask Application to Heroku. I followed a guide here: https://www.youtube.com/watch?v=Li0Abz-KT78.
5. Create an AWS S3 bucket and add it to the heroku app using https://devcenter.heroku.com/articles/s3 (This is not necessary if you do not plan to send pictures).
6. Add your webhook url to the Facebook app here: https://developers.facebook.com/apps/{YOUR-APP-ID}/messenger/settings/
7. Optionally, you can run the app locally using a Ngrok forwarding. Install Ngrok, run the app localy and forward the port using Ngrok http *port* command.
8. Write any message to the application messenger chat on Facebook and see the generated pictures.
