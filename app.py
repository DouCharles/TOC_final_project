import os
import re
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from transitions.core import Condition

from fsm import TocMachine
from utils import send_button_message, send_image_message, send_text_message, send_sticker_message,imgur_URL

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

import sql

def pie(data,category,color,seperated):
    myFont = FontProperties(fname = "./font/kaiu.ttf",size  = 14)
    category = category#["測試1","測試2"]
    expend = data #[50,70]
    color = color #['#ff0000', '#d200d2']
    plt.figure(figsize=(12,8))
    separeted = seperated#(0,0.4)
    pictures,category_text,percent_text = plt.pie(
            expend,                           # 數值
            colors = color,                   # 指定圓餅圖的顏色
            labels = category,                # 分類的標記
            autopct = "%0.2f%%",              # 四捨五入至小數點後面位數
            explode = separeted,              # 設定分隔的區塊位置
            pctdistance = 0.65,               # 數值與圓餅圖的圓心距離
            radius = 0.7,                     # 圓餅圖的半徑，預設是1
            center = (-10,0),                 # 圓餅圖的圓心座標
            shadow=False)                     # 是否使用陰影

    for t in category_text:
        t.set_fontproperties(myFont)
    for t in percent_text:
        t.set_fontproperties(myFont)
    plt.title("財務分析表", fontproperties=myFont, x=0.5, y=1.03)

    # 設定legnd的位置
    plt.legend(loc = "center right", prop=myFont)
    #plt.show()
    plt.savefig("./img/account.png")
    #plt.savefig("static/img/account.png")



load_dotenv()


machine = TocMachine(
    states=["user", 
    "memo", "memoAdd", "memoDelete", "memoList",
    "bookkeeping", "bookkeepingRecord"
    # ,"bookkeeping", "bookkeepingCost", "bookkeepingEarn", "bookkeepingCategory", "bookeepingMoney", "bookeepingContent"
    ],
    transitions=[
        {"trigger": "advance","source": ["user", "bookkeeping"],"dest": "memo","conditions": "is_going_to_memo",},
        {"trigger": "advance","source": ["user", "memo"],"dest": "bookkeeping","conditions": "is_going_to_bookkeeping",},
        {"trigger": "advance","source":  ["memo","bookkeeping"],"dest": "user","conditions": "is_going_to_user",},
        
        {"trigger": "advance","source": "memo", "dest":"memoAdd","conditions":"is_going_to_memoAdd",},
        {"trigger": "advance","source": "memo", "dest":"memoDelete","conditions":"is_going_to_memoDelete",},
        {"trigger": "advance","source": "memo", "dest":"memoList","conditions":"is_going_to_memoList",},
        {"trigger": "go_back_memo","source": ["memoAdd","memoDelete","memoList"], "dest":"memo",},

        {"trigger": "advance","source": "bookkeeping", "dest":"bookkeepingRecord","conditions":"is_going_to_bookkeepingRecord",},
        {"trigger": "advance","source": "bookkeepingRecord","dest": "bookkeeping","conditions": "is_going_back_to_bookkeeping",},
        
        {"trigger": "advance","source":  ["user","memo","bookkeeping","bookkeepingRecord"],"dest": "user","conditions": "is_going_to_reset",},
        #-----------------------------------------------#

    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        
        reply_token = event.reply_token
        if event.message.text == "hi":
            send_sticker_message(reply_token,11538,51626494)
            return "OK"
        if event.message.text == "FSM":
            machine.get_graph().draw("./img/fsm.png", prog="dot", format="png")
            send_image_message(reply_token,imgur_URL("./img/fsm.png"))
            return "OK"
        if machine.mode == "bookkeepingRecord":
            
            message = event.message.text.split('/')
            if message[0]=="返回" or message[0] == "reset":
                response = machine.advance(event)
            # elif len(message) != 3:
            #     send_text_message(reply_token,"錯誤的指令")
            elif message[0] == "help":
                send_text_message(reply_token,
"""進入 記帳->記錄模式
指令：
花費/金額/項目
進帳/金額/項目
刪除/id (需先列表查詢id)
列表

ex
花費/500/書本
進帳/10000/刮刮樂

若要結束記錄模式，可以輸入"返回"
""")
            elif message[0] == "花費" and len(message) == 3:
                # machine.bookkeepingCost.append([int(message[1]),message[2]])
                sql.sql_insert_account(message[2],message[1],message[0])
                send_text_message(reply_token,"記錄成功")
            elif message[0] == "進帳"and len(message) == 3:
                sql.sql_insert_account(message[2],message[1],message[0])
                # machine.bookkeepingEarn.append([int(message[1]),message[2]])
                send_text_message(reply_token,"記錄成功")
            elif message[0] == "刪除"and len(message) == 2:
                sql.sql_delete_account(message[1])
                send_text_message(reply_token,"刪除成功")
            elif message[0] == "列表":
                s = "你的花費內容:\nid:項目->金額\n"
                cost_data = sql.sql_search_account("花費")
                earn_data = sql.sql_search_account("進帳")
                for i in range(len(cost_data)):
                    s = s + "{}:{}->{}\n".format(cost_data[i][0],cost_data[i][2],cost_data[i][1])
                s += "\n你的進帳內容:\nid:項目->金額\n"
                for i in range(len(earn_data)):
                    s = s + "{}:{}->{}\n".format(earn_data[i][0],earn_data[i][2],earn_data[i][1])
                if len(cost_data) == 0 and len(earn_data) == 0:
                    send_text_message(reply_token,"帳本目前為空的")
                else:
                    send_text_message(reply_token,s)
            else:
                send_text_message(reply_token,"錯誤的指令")
            # print("COST = ",machine.bookkeepingCost)
            # print("EARN = ",machine.bookkeepingEarn)
            return "OK"
        elif machine.mode=="bookkeeping" and event.message.text == "列表":
            s = "你的花費內容:\nid:項目->金額\n"
            cost_data = sql.sql_search_account("花費")
            earn_data = sql.sql_search_account("進帳")
            # for i in range(len(machine.bookkeepingCost)):
            #     s = s + "{}->{}\n".format(machine.bookkeepingCost[i][1],machine.bookkeepingCost[i][0])
            # s += "\n你的進帳內容:\n項目->金額\n"
            # for i in range(len(machine.bookkeepingEarn)):
            #     s = s + "{}->{}\n".format(machine.bookkeepingEarn[i][1],machine.bookkeepingEarn[i][0])
            for i in range(len(cost_data)):
                s = s + "{}:{}->{}\n".format(cost_data[i][0],cost_data[i][2],cost_data[i][1])
            s += "\n你的進帳內容:\nid:項目->金額\n"
            for i in range(len(earn_data)):
                s = s + "{}:{}->{}\n".format(earn_data[i][0],earn_data[i][2],earn_data[i][1])
            # if len(machine.bookkeepingCost) == 0 and len(machine.bookkeepingEarn) == 0:
            #     send_text_message(reply_token,"帳本目前為空的")
            # else:
            #     send_text_message(reply_token,s)
            if len(cost_data) == 0 and len(earn_data) == 0:
                send_text_message(reply_token,"帳本目前為空的")
            else:
                send_text_message(reply_token,s)
            return "OK"
        elif machine.mode=="bookkeeping" and event.message.text == "分析":
            # cost = 0
            # for i in range(len(machine.bookkeepingCost)):
            #     cost += machine.bookkeepingCost[i][0]
            # earn = 0
            # for i in range(len(machine.bookkeepingEarn)):
            #     earn += machine.bookkeepingEarn[i][0]
            cost = 0
            earn = 0
            cost_data = sql.sql_search_account("花費")
            earn_data = sql.sql_search_account("進帳")
            for i in range(len(cost_data)):
                cost += int(cost_data[i][1])
            for i in range(len(earn_data)):
                earn += int(earn_data[i][1])
            pie([cost,earn],["花費","進帳"],['#ff0000', '#d200d2'],(0,0.1))
            send_image_message(reply_token,imgur_URL("./img/account.png"))
            # send_image_message(reply_token,"https://toctesting.herokuapp.com/static/img/accorunt.png")
            #send_text_message(reply_token,"開始分析")
            return "OK"
        elif machine.mode=="bookkeeping" and event.message.text == "help":
            send_button_message(reply_token,"記帳模式","歡迎進入記帳模式，請選擇您想要使用的功能",["記錄","列表","分析"])
#             send_text_message(reply_token,
# """進入 記帳->記錄模式
# 指令：
# 花費/金額/項目
# 進帳/金額/項目

# ex
# 花費/500/書本
# 進帳/10000/刮刮樂

# 若要結束記錄模式，可以輸入"返回"
# """)
            return "OK"
        else:
            response = machine.advance(event)
        if response == False:
            #reply_token = event.reply_token
            #machine.go_back_memo()+
            if event.message.text == "help":
                if machine.mode == "memo":
                    send_text_message(reply_token, 
        """歡迎進入 備忘錄模式
指令介紹: 
新增/時間/內容 : 為您新增項目
刪除/id : 為您刪除項目  (請先用列表確定要刪除的事件id)
列表: 列表您的備忘錄

ex:
新增/9:00/開會

若要離開此模式，請輸入"選單"
""")
                elif machine.mode == "user":
                    send_button_message(reply_token,"記錄小幫手","歡迎使用記錄小幫手，請選擇您想要的模式",["記帳","備忘錄"])
                elif machine.mode == "bookkeeping":
                    send_button_message(reply_token,"記帳模式","歡迎進入記帳模式，請選擇您想要使用的功能",["記錄","列表","分析"])
                elif machine.mode == "bookkeepingRecord":
                    send_text_message(reply_token,
"""進入 記帳->記錄模式
指令：
花費/金額/項目
進帳/金額/項目

ex
花費/500/書本
進帳/10000/刮刮樂

若要結束記錄模式，可以輸入"返回"
""")
            else:
                send_text_message(event.reply_token, "查無此指令，若需要幫助請輸入 help")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    #return send_file("fsm22.png", mimetype="image/png")
    return "ok"


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
