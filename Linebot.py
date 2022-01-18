from flask import Flask, request, abort #create a light website for Linbot connection
import json #read the data from line
import requests #reach the data from internet immediately
import time # get the current time
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, JoinEvent, TextMessage, TextSendMessage)
import gspread
import sys
import datetime
from oauth2client.service_account import ServiceAccountCredentials as SAC

GDriveJSON = 'Accountingkey.json' #json file that contain Google API private key
Gspreadsheet = 'Personal Accounting' # google sheet name
Line_bot_api = LineBotApi('mGZ+2slcF0VcNjs1YvreNpOm3h4STfJqPUzTonl64akZ79ieFSZjgvHU/PFx44dNBbzfcL5odxlvtcMcDaPeriu2A7LD43fPhkrOHzcS4Y5MSBg6gmto7Jqv15fOuODPKc2NdPWWiR108i0ti4u1VwdB04t89/1O/w1cDnyilFU=') # Linebot customize Api
handler = WebhookHandler('008021c29864de0a406566a9ad5e01de') # channel secret

app = Flask(__name__)

def gsheetedit(event,content1):
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            client = gspread.authorize(key)
            sheet = client.open(Gspreadsheet).sheet1
        except Exception:
            Line_bot_api.reply_message(event.reply_token,TextSendMessage(text="無法連到google sheet"))
            sys.exit(1)

        textt=""
        textt+= content1
        content1 = json.dumps(datetime.datetime.now(), cls = DateTimeEncoder) + '\0' + content1
        content = content1.split('\0')
        if textt!="":
                sheet.append_row(content)
                Line_bot_api.reply_message(event.reply_token,TextSendMessage(text="紀錄成功"))
                print('新增一列資料到試算表' ,Gspreadsheet)
                return textt

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z) # for the error: 'TypeError: Object of type datetime is not JSON serializable'
                                      # redefined json type

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
@handler.add(MessageEvent, message = TextMessage)
def reply_message(event):
   #個人記帳功能
    text = event.message.text
    content = text.split()
    for i in range(5-len(content)+1):
        content.append('NA')
        #確保全部index都有內容
    if content[0] == '記帳':
        lists = content[1] + '\0' + content[2] + '\0' + content[3] + '\0' + content[4] 
        gsheetedit(event, lists)
        

'''@handler.add(MessageEvent, message = TextMessage) #The text Message you got from Linbot
def handle_msg(event):
    #Line_bot_api.push_message('Testing: Peronsal ID or Group ID', TextSendMessage(text=''))
    if(event.message.text=="start"):
        message=TextSendMessage(event.source.group_id)
        Line_bot_api.reply_message(event.reply_token, message) #get the group ID '''
    
    

if __name__ == '__main__':
    app.run() 