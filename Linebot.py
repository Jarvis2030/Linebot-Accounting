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
def Join_auto_message(event):
   #無法自動取得群組成員(初次加入時手動輸入群組成員)

@handler.add(MessageEvent, message = TextMessage) #The text Message you got from Linbot
def handle_msg(event):
    #Line_bot_api.push_message('Testing: Peronsal ID or Group ID', TextSendMessage(text=''))
    if(event.message.text=="start"):
        message=TextSendMessage(event.source.group_id)
        Line_bot_api.reply_message(event.reply_token, message) #get the group ID
    
    







if __name__ == '__main__':
    app.run() 