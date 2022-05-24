import telebot,subprocess, os, sys
from telebot import types

bot=telebot.TeleBot('1956570124:AAG3m3p3eTmpS7qTqdGrkdGI4eGXdRX_6Ug')
if len(sys.argv)>1:
    bot.send_message(sys.argv[1],"Введите номер телефона")
    @bot.message_handler(func=lambda message: message.chat.id==sys.argv[1])
    def phone_request(message):
        msg=bot.send_message(message.chat.id,"Введите номер телефона")
        bot.register_next_step_handler(msg,personal_account_request)

    def personal_account_request(message):
        phone=message.text
        if phone.isdigit():
            msg=bot.reply_to(message, "Введите номер лицевого счета")
            bot.register_next_step_handler(msg, statements_request)

    def statements_request(message):
        account=message.text
        if account.isdigit():
            msg=bot.reply_to(message,"Внесите показания счетчика")
            bot.register_next_step_handler(msg, statements_handler)

    def statements_handler(message):
        statements=message.text
        if statements.isdigit():
            msg=bot.reply_to(message,f"Ваш номер {phone} Ваш лицевой счет {account} Ваши показания {statements}")

else:
    print("Error")

bot.infinity_polling()