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
Gspreadsheet = 'CashFlow' # google sheet name
Line_bot_api = LineBotApi('mGZ+2slcF0VcNjs1YvreNpOm3h4STfJqPUzTonl64akZ79ieFSZjgvHU/PFx44dNBbzfcL5odxlvtcMcDaPeriu2A7LD43fPhkrOHzcS4Y5MSBg6gmto7Jqv15fOuODPKc2NdPWWiR108i0ti4u1VwdB04t89/1O/w1cDnyilFU=') # Linebot customize Api
handler = WebhookHandler('008021c29864de0a406566a9ad5e01de') # channel secret

app = Flask(__name__)

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
def google_sheet_message(event):
   #無法自動取得群組成員(初次加入時手動輸入群組成員)
    Line_bot_api.reply_message(event.reply_token,TextSendMessage(text="紀錄成功"))
    pass
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
        textt+= event.message.text
        if textt!="":
                sheet.append_row((json.dumps(datetime.datetime.now(), cls = DateTimeEncoder), textt))
                print('新增一列資料到試算表' ,Gspreadsheet)
                return textt


'''@handler.add(MessageEvent, message = TextMessage) #The text Message you got from Linbot
def handle_msg(event):
    #Line_bot_api.push_message('Testing: Peronsal ID or Group ID', TextSendMessage(text=''))
    if(event.message.text=="start"):
        message=TextSendMessage(event.source.group_id)
        Line_bot_api.reply_message(event.reply_token, message) #get the group ID '''
    
    







if __name__ == '__main__':
    app.run() 