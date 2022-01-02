import os
from flask import app

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, MessageTemplateAction, ImageSendMessage, StickerSendMessage
from linebot.models.messages import StickerMessage
from linebot.models.template import ButtonsTemplate

import pyimgur

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

def imgur_URL(path):
    # normal_samples = np.random.normal(size = 100000)
    # uniform_samples = np.random.uniform(size = 100000)
    # plt.hist(normal_samples)
    # plt.savefig('send.png')
    CLIENT_ID = "fd09955e4ff9447"
    PATH = path#"./img/account.png"
   # CLIENT_SECRETE = "3ade55fbdb044063c963eb1fb03a161589a8a52d"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    return uploaded_image.link

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_sticker_message(reply_token, packageId = 1, stickerId = 1):
    line_bot_api = LineBotApi(channel_access_token)
    message = StickerSendMessage(
        package_id = str(packageId),
        sticker_id = str(stickerId)
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"


def send_image_message(reply_token,url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)

    return

def send_button_message(reply_token,title,text, buttons):#id, text, buttons):
    line_bot_api = LineBotApi(channel_access_token)
    message = []
    for i in range(len(buttons)):
        message.append(MessageTemplateAction(label=buttons[i],text = buttons[i]))
    line_bot_api.reply_message(reply_token, TemplateSendMessage(alt_text="template",
    
    template=ButtonsTemplate(title=title,text = text,actions=message)))
    return "OK"


