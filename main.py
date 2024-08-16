from config import utelegram_config
from config import wifi_config
from messages import texts

import utelegram
import network
import time
import machine

from machine import Pin
from machine import Timer

debug = True



custom_keyboard = {
    'keyboard': [
        ['Einschalten', 'Ausschalten']
    ],
    'resize_keyboard': True,  # Allow the keyboard to resize (optional)
    'one_time_keyboard': False  # Hide the keyboard after use (optional)
}



machine.freq(68000000)


relay= Pin(6,Pin.OUT)
relay.off()
#led = Pin("LED", Pin.OUT)
led = Pin(1, Pin.OUT)
time.sleep(1)



def blink(t):
    led.toggle()


blinktimer = Timer(mode = Timer.PERIODIC, freq=4, callback=blink)


sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(wifi_config['ssid'], wifi_config['password'])

while not sta_if.isconnected() and sta_if.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)
    
print(sta_if.ifconfig())
blinktimer.init(freq=2, callback=blink)

def get_message(message):
    #print(message)
    bot.send(message['message']['chat']['id'], message['message']['text'].upper())
    
def reply_start(message):
    l_message = message
    bot.send_keyboard(message['message']['chat']['id'], custom_keyboard, texts['reply_start1'])
    bot.send(l_message['message']['chat']['id'], texts['reply_start2'])
    
def reply_ping(message):
    #print(message)
    bot.send_keyboard(message['message']['chat']['id'], custom_keyboard, texts['reply_ping'])
    
def reply_on(message):
    #print(message)
    led.on()
    relay.on()
    bot.send(message['message']['chat']['id'], 'Eingeschaltet')

def reply_off(message):
    #print(message)
    led.off()
    relay.off()
    bot.send(message['message']['chat']['id'], 'Ausgeschaltet')

if sta_if.isconnected():
    bot = utelegram.ubot(utelegram_config['token'])
    bot.register('/ping', reply_ping)
    
    bot.register('Einschalten', reply_on)
    bot.register('Ausschalten', reply_off)
    
    bot.register('/Einschalten', reply_on)
    bot.register('/Ausschalten', reply_off)
    
    bot.register('/start', reply_start)
    
    bot.set_default_handler(get_message)

    print('BOT LISTENING')
    blinktimer.deinit()
    led.on()
    bot.listen()
else:
    print('NOT CONNECTED - aborting')
