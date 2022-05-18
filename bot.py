import telebot
from telebot import types
######Текстовые переменные
hi="""Вас приветствует BOT. Я помогу Вам:
-Передать показания
-Сделать заявку (опломбировка, проверка счетчика, пр.)
-Оплатить за газ


ИНСТРУКЦИЯ:
-Для продолжения выберите пункт меню
-Для перезапуска бота в любом месте напишите старт"""


keyboard_main=types.InlineKeyboardMarkup()
keyboard_main.add(types.InlineKeyboardButton("Показания", callback_data="111"),types.InlineKeyboardButton("Оплата",callback_data="payment"),
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

######

######
bot=telebot.TeleBot('1956570124:AAG3m3p3eTmpS7qTqdGrkdGI4eGXdRX_6Ug')
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,hi, parse_mode='html', reply_markup=keyboard_main)


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