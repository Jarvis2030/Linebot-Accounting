from flask import Flask, request, abort #create a light website for Linbot connection
import json #read the data from line
import requests #reach the data from internet immediately
import time # get the current time
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, JoinEvent, TextMessage, TextSendMessage)

Line_bot_api = LineBotApi('mGZ+2slcF0VcNjs1YvreNpOm3h4STfJqPUzTonl64akZ79ieFSZjgvHU/PFx44dNBbzfcL5odxlvtcMcDaPeriu2A7LD43fPhkrOHzcS4Y5MSBg6gmto7Jqv15fOuODPKc2NdPWWiR108i0ti4u1VwdB04t89/1O/w1cDnyilFU=') # Linebot customize Api
handler = WebhookHandler('008021c29864de0a406566a9ad5e01de') # channel secret
app = Flask(__name__)

@app.route("/callback", methods = ['POST'])
def callback(): #checking if the input message is right
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text = True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

'''@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    Line_bot_api.reply_message(event.reply_token, TextSendMessage(text = event.message.text))'''

@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "正在取得群組資訊...."

    Line_bot_api.reply_message(event.reply_token, TextMessage(text=newcoming_text))
    print("JoinEvent =", JoinEvent)


@handler.add(MessageEvent, message = TextMessage) #The text Message you got from Linbot
def inputdirectly(event):
    mtext = event.message.text #save the message from Linebot into variable 'mtext'






if __name__ == '__main__':
    app.run() 