import telebot
from telebot import types
from currency_converter import CurrencyConverter

bot = telebot.TeleBot("6501555107:AAGPhG8-hCGOqmjRzuVrrCtk2NZJxnAgjRU")
cur = CurrencyConverter()

@bot.message_handler(commands=['start'])
def first(message):
    bot.send_message(message.chat.id, 'Здравствуйте, введите сумму:', parse_mode='html')
    bot.register_next_step_handler(message, summ)

def summ(message):
    global money
    try:
        money = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Ввод не верный, введите сумму:')
        bot.register_next_step_handler(message, summ)
        return
    if money > 0:
        money = message.text.strip()
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot1 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        bot2 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        bot3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        bot4 = types.InlineKeyboardButton('EUR/GBP', callback_data='eur/gbp')
        #конвертация в рубли и обратно не поддерживается в currency converter
        markup.add(bot1, bot2, bot3, bot4)
        bot.send_message(message.chat.id, 'Выберите пару валют:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Сумма должны быть положительной, введите сумму еще раз:')
        bot.register_next_step_handler(message, summ)

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    value = call.data.upper().split('/')
    r = cur.convert(money, value[0], value[1])
    bot.send_message(call.message.chat.id, f'Получается {r}. Можете ввести сумму заново:')
    bot.register_next_step_handler(call.message, summ)


bot.infinity_polling()