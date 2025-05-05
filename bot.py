import telebot
import random
from secret import tok

bot = telebot.TeleBot(tok)


name = ''
surname = ''
age = 0
greets = ['Hello!', 'Bonjour!', 'Привет!']

@bot.message_handler(content_types=['text'])
def start(message):

    if message.text == "Привет":
        bot.send_message(message.from_user.id, f"Привет {message.from_user.first_name}!!!")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text == "/hello":
        bot.send_message(message.from_user.id, text=random.choice(greets))
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, 'Сейчас я попрошу тебя ответить на некоторые вопросы')
        # get_name(message)
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Выбери команду\n/help -- помощь\n/reg -- принять данные от пользователя\n/hello -- поздороваться")

def get_name(message): #получаем фамилию
    global name
    # bot.send_message(message.from_user.id, "Как тебя зовут?")

    name = message.text
    # get_surname(message)
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    # bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    surname = message.text
    # get_age(message)
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    while age == 0: #проверяем что возраст изменился
        try:
            age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')

        age = message.text

    keyboard = telebot.types.InlineKeyboardMarkup() #наша клавиатура
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
    key_no= telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    keyboard.add(key_no)

    question = f"Тебе {str(age)} лет, тебя зовут {name} {surname}?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call:True)
def callback_worker(call):
    if call.message:
        if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        
            bot.send_message(call.message.from_user.id, 'Запомню : )')
        elif call.data == "no":
            # bot.send_message(call.message.from_user.id, text="Введите /reg")
            bot.send_message(call.from_user.id, "Как тебя зовут?")
            print("+++++++++++++++++++++++")
            bot.register_next_step_handler(call, get_name)
            print("+++++++++++++++++++++++")
        # get_name(call)
        # bot.register_next_step_handler(call.message, get_name)




bot.polling(non_stop=True)
