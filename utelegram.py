import time
import gc
import ujson
import requests


class ubot:
    def __init__(self, token, offset=0):
        self.url = 'https://api.telegram.org/bot' + token
        self.commands = {}
        self.default_handler = None
        self.message_offset = offset
        self.sleep_btw_updates = 3

        messages = self.read_messages()
        if messages:
            if self.message_offset==0:
                self.message_offset = messages[-1]['update_id']
            else:
                for message in messages:
                    if message['update_id'] >= self.message_offset:
                        self.message_offset = message['update_id']
                        break

   # def replace_utf_unicode(self, text):
    #    print(text)
     #   text_str=text.replace("ä","/u00e4")
      #  text_str=text_str.replace("ö","/u00f6")
       # text_str=text_str.replace("ü","/u00fc")
        #text_b = bytearray(text_str,'utf')
   #     for x in range(len(text_b)):
    #        if text_b[x]==47:
     #           #text_b[x]=195
      #          text_b[x]=92
       # text_str2=text_b.decode()
        #print(text_str2)
        #return text_str2
    
    def send(self, chat_id, text):
       
        text=text.replace('ä','ae')
        text=text.replace('ö','oe')
        text=text.replace('ü','ue')
        data = {'chat_id': chat_id, 'text': text}
        try:
            headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
            response = requests.post(self.url + '/sendMessage', json=data, headers=headers, timeout=10)
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
            response = requests.post(self.url + '/sendMessage', json=data, headers=headers, timeout=10)
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
            update_messages = requests.post(self.url + '/getUpdates', json=self.query_updates, timeout=31).json() 
            if 'result' in update_messages:
                for item in update_messages['result']:
                    result.append(item)
            return result
        except (ValueError):
            return None
        except (OSError):
            print("OSError: request timed out")
            return None

    def listen(self):
        while True:
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
                    
    
        
