from flask import Flask, request, abort #create a light website for Linbot connection
import json #read the data from line
import requests #reach the data from internet immediately
import time # get the current time
from linebot import LineBotApi, WebhookHandler,MessageEvent,TextMessage, TextSendMessage, InvalidSignatureError

Line_bot_api = LineBotApi() # Linebot customize Api
handler = WebhookHandler() # channel secret
app = Flask(__name__)

@app.route("/callback",method = ['POST'])
def callback(): #checking if the input message is right
    signature = request.header['X-Line-Signature']
    body = request.get_data(as_text = True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    Line_bot_api.reply_message(event.reply_token, TextSendMessage(text = event.message.text))

if __name__ == '__main__':
    app.run() 