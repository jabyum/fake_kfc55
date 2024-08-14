import telebot
import buttons as bt
from geopy.geocoders import Photon
import database as db

bot = telebot.TeleBot(token="TOKEN")
geolocator = Photon(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Главное меню")
    elif checker == False:
        bot.send_message(user_id, "Добро пожаловать в наш бот доставки!\n"
                                  "Напишите своё имя")
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, "Поделитесь своими контактами",
                     reply_markup=bt.phone_number_bt())
    bot.register_next_step_handler(message, get_number, name)

def get_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(user_id, f"{name}, вы успешно зарегистрированы!\n"
                                  "Выберите действие из меню")
        db.add_user(name, phone_number, user_id)
    else:
        bot.send_message(user_id, "Отправьте свой номер через кнопку в меню",
                         reply_markup=bt.phone_number_bt())
        bot.register_next_step_handler(message, get_number, name)
def get_location(message):
    user_id = message.from_user.id
    if message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        address = geolocator.reverse((latitude, longitude)).address
        print(address)

bot.infinity_polling()
