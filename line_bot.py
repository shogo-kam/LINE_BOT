import pya3rt
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

#LINE Developer ID
line_bot_api = LineBotApi('適宜入力')
handler = WebhookHandler('適宜入力')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ai_messege = talk_ai(event.message.text)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ai_messege))

def talk_ai(word):
    apikey = '適宜入力'
    client = pya3rt.TalkClient(apikey) 
    reply_message = client.talk(word) 
    return reply_message['results'][0]['reply'] 

if __name__ == '__main__':
    app.run()