import telebot
import buttons as bt
from geopy.geocoders import Photon
import database as db
# db.add_product("Бургер", 30000, "лучший бургер", 20, "https://menunedeli.ru/wp-content/uploads/2023/07/4523862E-973D-49D0-BE99-2609DDAA5CF4-933x700.jpeg")
# db.add_product("Чизбургер", 35000, "лучший чизбургер", 20, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7lfdGQENwsxIWcpk80o43dRz2V8jN9pBK_w&s")
# db.add_product("Хот-дог", 15000, "лучший хотдог", 0, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSsfW388zWeoTBoYVtL5yJi85sJmFoVB3isLw&s")

bot = telebot.TeleBot(token="6849219345:AAFcDrJ-NC1FxsfoKqat672eAltYQe9RMpc")
geolocator = Photon(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Главное меню", reply_markup=bt.main_menu_bt())
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
                                  "Выберите действие из меню", reply_markup=bt.main_menu_bt())
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
@bot.callback_query_handler(lambda call: call.data in ["back", "main_menu", "cart"])
def all_calls(call):
    user_id = call.message.chat.id
    if call.data == "main_menu":
        bot.delete_message(user_id, call.message.id)
        bot.send_message(user_id, "Главное меню", reply_markup=bt.main_menu_bt())






@bot.message_handler(content_types=["text"])
def main_menu(message):
    user_id = message.from_user.id
    if message.text == "🍴Меню":
        all_product = db.get_pr_id_name()
        bot.send_message(user_id, "Меню", reply_markup=bt.products_in(all_product))
    elif message.text == "🛒Корзина":
        bot.send_message(user_id, "Ваша корзина:")
    elif message.text == "❗️Отзыв":
        bot.send_message(user_id, "Напишите текст вашего отзыва")


bot.infinity_polling()
