# 載入需要的模組
from __future__ import unicode_literals
import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

with open("token.json") as jFile:
    data = json.load(jFile)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(data["lineToken"])
handler = WebhookHandler(data["lineChannelSecret"])

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

if __name__ == "__main__":
    app.run()