from transitions.extensions import GraphMachine

from utils import send_button_message, send_text_message

import sql

#memo =[]



class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.mode = "user"
        # self.bookkeepingCost = []
        # self.bookkeepingEarn = []
    #memo

    def is_going_to_memo(self, event):
        text = event.message.text
        return text == "備忘錄"

    def is_going_to_memoAdd(self,event):
        text = event.message.text
        return text[0:2] == "新增"
    def is_going_to_memoDelete(self,event):
        text = event.message.text
        print("text = {0}".format(text[0:2]))
        return text[0:2] == "刪除"
    def is_going_to_memoList(self,event):
        text = event.message.text
        return text == "列表"

    def is_going_to_bookkeeping(self, event):
        text = event.message.text
        return text == "記帳"

    def is_going_to_bookkeepingRecord(self, event):
        text = event.message.text
        return text == "記錄"
    
    def is_going_back_to_bookkeeping(self, event):
        text = event.message.text
        return text == "返回"

    def is_going_to_user(self,event):
        text = event.message.text
        return text == "選單"
    
    def is_going_to_reset(self,event):
        text = event.message.text
        if text == "reset":
            sql.sql_reset()
        return text == "reset"

    def on_enter_memoAdd(self,event):
        content = event.message.text.split('/')
        # temp = {}
        # temp[content[2]] = content[1]
        # memo.append(temp)
        reply_token = event.reply_token
        if len(content) == 3:
            sql.sql_insert_memo(content[2],content[1])
        #memo.append(str(event.message.text[3:]))
        # print(memo)
        
            send_text_message(reply_token,"新增成功")
        else:
            send_text_message(reply_token,"新增失敗")
        self.go_back_memo()

    def on_enter_memoDelete(self,event):
        reply_token = event.reply_token
        content = event.message.text.split('/')
        # if (int(content[1]) - 1 < len(memo)):
        #     memo.pop(int(content[1]) - 1 )
        #     send_text_message(reply_token,"刪除成功")
        # else:
        #     send_text_message(reply_token,"查無此事件")
        sql.sql_delete_memo(content[1])
        send_text_message(reply_token,"刪除成功")
        self.go_back_memo()

    def on_enter_memoList(self,event):
        reply_token = event.reply_token
        all_memo = "id/時間/活動內容\n"
        data = sql.sql_search_memo()
        # print("ev = ",ev)
        # print("ev[0] = ",ev[0])
        # print("ev[0][0] = ",ev[0][0] )
        # print("len(ev) = ",len(ev))
        # for i in range(len(memo)):
        #     all_memo = all_memo + str(i+1) + "/" + list(memo[i].values())[0]+"/" + list(memo[i].keys())[0] + "\n"
        for i in range(len(data)):
            all_memo = all_memo + str(data[i][0]) + "/" + data[i][2] +"/" + data[i][1] + "\n"
        if all_memo == "id/時間/活動內容\n":
            all_memo = "備忘錄沒有事情須完成"
        send_text_message(reply_token,all_memo)
        self.go_back_memo()

    def on_enter_memo(self, event = None):
        print("I'm entering memo")
        self.mode = "memo"
        if (event != None):
            reply_token = event.reply_token
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
            
        #self.go_back()

    def on_enter_user(self, event):
        global memo
        print("I'm entering user")
        self.mode = "user"
        reply_token = event.reply_token
        send_button_message(reply_token,"記錄小幫手","歡迎使用記錄小幫手，請選擇您想要的模式",["記帳","備忘錄"])
        text = event.message.text
        print("texttext = {}".format(text))
        # if (event.message.text == "reset"):
        #     memo = []
        #     self.bookkeepingEarn = []
        #     self.bookkeepingCost = []
        

    # def on_exit_user(self):
    #     print("Leaving user")

    def on_exit_memo(self,event):
        print("Leaving memo")
    def on_exit_memoAdd(self):
        print("Leaving memoAdd")
    def on_exit_memoDelte(self):
        print("Leaving memoDelete")
    def on_exit_memoList(self):
        print("Leaving memoList")

    def on_enter_bookkeeping(self, event):
        print("I'm entering bookkeeping")
        self.mode = "bookkeeping"
        reply_token = event.reply_token
        send_button_message(reply_token,"記帳模式","歡迎進入記帳模式，請選擇您想要使用的功能",["記錄","列表","分析"])
        #self.go_back()
    
    def on_enter_bookkeepingRecord(self, event):
        self.mode = "bookkeepingRecord"
        reply_token = event.reply_token
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

    def on_exit_bookkeeping(self,event):
        print("Leaving bookkeeping")
    def on_exit_bookkeepingRecord(self,event):
        print("Leaving bookkeeping")
