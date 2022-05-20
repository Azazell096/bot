import telebot,subprocess, os, sys
from telebot import types

bot=telebot.TeleBot('1956570124:AAG3m3p3eTmpS7qTqdGrkdGI4eGXdRX_6Ug')
if len(sys.argv)>1:
    bot.send_message(950181410, "Hi from module")
else:
    print("Error")