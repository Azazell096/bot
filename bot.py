import telebot,subprocess,os, sys, requests, selenium, time
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

######Кнопки и текстовые реплики бота
hi="""Вас приветствует BOT. Я помогу Вам:
-Передать показания
-Сделать заявку (опломбировка, проверка счетчика, пр.)
-Оплатить за газ


ИНСТРУКЦИЯ:
-Для продолжения выберите пункт меню
-Для перезапуска бота в любом месте напишите старт"""


keyboard_main=types.InlineKeyboardMarkup()
keyboard_main.add(types.InlineKeyboardButton("Показания", callback_data="statements"),types.InlineKeyboardButton("Оплата",callback_data="payment"),
                    types.InlineKeyboardButton("Личный кабинет", callback_data="None"),types.InlineKeyboardButton("Заявка", callback_data="None"),
                    types.InlineKeyboardButton("Справочная информация", callback_data="callback_info"), row_width=2 )

keyboard_info=types.InlineKeyboardMarkup()
keyboard_info.add(types.InlineKeyboardButton("Цена на газ", url='https://mrgkchr.ru/content/documents/file/ec7a838f6cbdb69ab4ef447ad009b959.pdf'),
                  types.InlineKeyboardButton("Способы оплаты", url='https://mrgkchr.ru/consumers/information-for-the-population/payment-gas/'), row_width=2)
keyboard_info.add(types.InlineKeyboardButton("Наши офисы", url='https://mrgkchr.ru/#map'),
                  types.InlineKeyboardButton("Договор о поставке газа", url='https://mrgkchr.ru/consumers/information-for-the-population/the-agreement-on-gas-supplies/'),
                  types.InlineKeyboardButton("Возврат в основное меню", callback_data="main_menu"), row_width=1)

keyboard_payment=types.InlineKeyboardMarkup()
keyboard_payment.add(types.InlineKeyboardButton("ЛК Газпром межрегионгаз Черкесск", url='https://lk.mrgkchr.ru/unauth/pay.php'),
                    types.InlineKeyboardButton("""ЛК "Смородина" """, url='https://xn--80afnfom.xn--80ahmohdapg.xn--80asehdb/login' ))

keyboard_cancel=types.InlineKeyboardMarkup()
keyboard_cancel.add(types.InlineKeyboardButton("Отмена", callback_data="Cancel"))


######Переменные для отправки показаний

url='https://lk.mrgkchr.ru/unauth/statements.php'
user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')
headers = {
            'referer': f'{url}',
            'User-Agent': user_agent
        }

global driver
driver=dict()

class data_container:
    statements=''
    phone=''
    account=''

state=data_container()


######
bot=telebot.TeleBot('1956570124:AAG3m3p3eTmpS7qTqdGrkdGI4eGXdRX_6Ug')



@bot.message_handler(func=lambda message: message.text in ('start', 'старт', 'Старт', 'Start'))
def second_start(message):
        bot.send_message(message.chat.id,hi, parse_mode='html', reply_markup=keyboard_main)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,hi, parse_mode='html', reply_markup=keyboard_main)

@bot.message_handler(commands=['help'])



@bot.callback_query_handler(func=lambda call: call.data=='statements')
def phone_request(call):
    msg = bot.send_message(call.message.chat.id, "Введите номер телефона",reply_markup=keyboard_cancel)
    bot.register_next_step_handler(msg, personal_account_request)



def personal_account_request(message):
    state.phone = message.text
    if state.phone.isdigit():
        msg = bot.reply_to(message, "Введите номер лицевого счета", reply_markup=keyboard_cancel)
        bot.register_next_step_handler(msg, statements_request)


def statements_request(message):
    state.account = message.text
    if state.account.isdigit():
        msg = bot.reply_to(message, "Внесите показания счетчика",reply_markup=keyboard_cancel)
        bot.register_next_step_handler(msg, statements_handler)


def statements_handler(message):
    state.statements = message.text
    if state.statements.isdigit():
        bot.reply_to(message, f"Ваш номер {state.phone} Ваш лицевой счет {state.account} Ваши показания {state.statements}")
    #Отправка показаний на сайт !!!!!!!!
        driver[message.chat.id] = webdriver.Chrome()
        driver[message.chat.id].get(url=url)
        input_ls = driver[message.chat.id].find_element(By.NAME,'ls')
        input_phone = driver[message.chat.id].find_element(By.NAME,'phone')
        input_statements = driver[message.chat.id].find_element(By.NAME,'statements')
        input_ls.clear()
        input_ls.send_keys(state.account)
        input_statements.clear()
        input_statements.send_keys(state.statements)
        input_phone.clear()
        input_phone.send_keys(state.phone)
        input_phone.send_keys(Keys.ENTER)
        sms=driver[message.chat.id].find_element(By.NAME,'sms_code', )
        print(sms)
        msg=bot.send_message(message.chat.id, "Введите код из смс",reply_markup=keyboard_cancel)
        bot.register_next_step_handler(msg, sms_handler)


def sms_handler(message):
    input_sms=driver[message.chat.id].find_element(By.NAME,'sms_code', )
    input_sms.clear()
    input_sms.send_keys(message.text)
    input_sms.send_keys(Keys.ENTER)
    #!!!!!Реализовать проверу Успешного ввода кода из смс и принятия показаний  сайтом
    bot.send_message(message.chat.id,"Ok",reply_markup=keyboard_main)
    #!!!!!Необходимо закрывать каждый процесс браузера после работы




@bot.callback_query_handler(func=lambda call: call.data=='Cancel')
def Cancel_handler(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    bot.send_message(call.message.chat.id,"!! ", reply_markup=keyboard_main)



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data=='callback_info':
        bot.send_message(call.message.chat.id,"Выберите пункт", reply_markup=keyboard_info)
    elif call.data=='main_menu':
        bot.send_mesage(call.message.chat.id, "Меню:", reply_markup=keyboard_main)
    elif call.data=='payment':
        bot.send_message(call.message.chat.id, "Выберите способ оплаты", reply_markup=keyboard_payment)


bot.infinity_polling()

######