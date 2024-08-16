import time
import gc
import ujson
import urequests
import machine
from machine import Timer

class ubot:
    def __init__(self, token, offset=0):
        self.url = 'https://api.telegram.org/bot' + token
        self.commands = {}
        self.default_handler = None
        self.message_offset = offset
        self.sleep_btw_updates = 0.1

        messages = self.read_first()
        if messages:
             if self.message_offset==0:
                 self.message_offset = messages[-1]['update_id']
             else:
                 for message in messages:
                     if message['update_id'] >= self.message_offset:
                         self.message_offset = message['update_id']
                         break
    
    def send(self, chat_id, text):
       
        text=text.replace('ä','ae')
        text=text.replace('ö','oe')
        text=text.replace('ü','ue')
        data = {'chat_id': chat_id, 'text': text}
        try:
            headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
            response = urequests.post(self.url + '/sendMessage', json=data, headers=headers, timeout=10)
            response.close()
            return True
        except:
            return False
        
    def send_keyboard(self, chat_id, keyboard, text):
        text=text.replace('ä','ae')
        text=text.replace('ö','oe')
        text=text.replace('ü','ue')
       # text=self.replace_utf_unicode(text)
        data = {'chat_id': chat_id, 'text': text, 'reply_markup': keyboard}
        print(data)
        try:
            headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
            response = urequests.post(self.url + '/sendMessage', json=data, headers=headers, timeout=10)
            print(response.text)
            response.close()
            return True
        except:
            return False

    def read_messages(self):
        result = []
        self.query_updates = {
            'offset': self.message_offset + 1,
            'limit': 1,
            'timeout': 30,
            'allowed_updates': ['message']}

        try:
            print("post")
            update_messages = urequests.post(self.url + '/getUpdates', json=self.query_updates, timeout=31).json()
            print("posted")
            if 'result' in update_messages:
                for item in update_messages['result']:
                    result.append(item)
            return result
        except (ValueError):
            print("error")
            return None
        except:
            print("Error")
            return None
        
        
    def read_first(self):
        result = []
        self.query_updates = {
            'offset': self.message_offset + 1,
            'limit': 1,
            'timeout': 1,
            'allowed_updates': ['message']}

        try:
            print("post")
            update_messages = urequests.post(self.url + '/getUpdates', json=self.query_updates, timeout=10).json()
            print("posted")
            if 'result' in update_messages:
                for item in update_messages['result']:
                    result.append(item)
            return result
        except (ValueError):
            print("error")
            return None
        except:
            print("Error")
            return None
        
    def timeout(self,t):
        print("timeout")
        time.sleep(1)
        machine.reset()
        

    def listen(self):
        while True:
            print("read once")
            self.read_once()
            time.sleep(self.sleep_btw_updates)
            gc.collect()

    def read_once(self):
        
        messages = self.read_messages()
        if messages:
            if self.message_offset==0:
                self.message_offset = messages[-1]['update_id']
                self.message_handler(messages[-1])
            else:
                for message in messages:
                    if message['update_id'] >= self.message_offset:
                        self.message_offset = message['update_id']
                        self.message_handler(message)
                        break
    
    def register(self, command, handler):
        self.commands[command] = handler

    def set_default_handler(self, handler):
        self.default_handler = handler

    def set_sleep_btw_updates(self, sleep_time):
        self.sleep_btw_updates = sleep_time

    def message_handler(self, message):
        if 'text' in message['message']:
            parts = message['message']['text'].split(' ')
            if parts[0] in self.commands:
                self.commands[parts[0]](message)
            else:
                if self.default_handler:
                    self.default_handler(message)
                    
    
        
