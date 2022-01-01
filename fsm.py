from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_memo(self, event):
        text = event.message.text
        return text.lower() == "memo"

    def is_going_to_bookkeeping(self, event):
        text = event.message.text
        return text == "記帳"
    
    def is_goint_to_user(self,event):
        text = event.message.text
        return text == "leave"
        

    def on_enter_memo(self, event):
        print("I'm entering memo")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger memo")
        #self.go_back()

    def on_enter_user(self, event):
        print("I'm entering user")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger user")
        

    # def on_exit_user(self):
    #     print("Leaving user")

    def on_exit_memo(self,event):
        print("Leaving memo")

    def on_enter_bookkeeping(self, event):
        print("I'm entering bookkeeping")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger bookkeeping")
        #self.go_back()

    def on_exit_bookkeeping(self,event):
        print("Leaving bookkeeping")
