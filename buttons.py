from telebot import types

def phone_number_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Поделиться номером", request_contact=True)
    kb.add(button)
    return kb
def location_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Поделиться локацией", request_location=True)
    kb.add(button)
    return kb
def main_menu_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton(text="🍴Меню")
    cart = types.KeyboardButton(text="🛒Корзина")
    feedback = types.KeyboardButton(text="❗️Отзыв")
    kb.add(menu, cart, feedback)
    return kb
def products_in(all_products):
    kb = types.InlineKeyboardMarkup(row_width=2)
    # статичные кнопки
    cart = types.InlineKeyboardButton(text="Корзина", callback_data="cart")
    back = types.InlineKeyboardButton(text="Назад", callback_data="main_menu")
    # динамичные кнопки
    all_buttons = [types.InlineKeyboardButton(text=product[1], callback_data=f"prod_{product[0]}")
                   for product in all_products]
    kb.add(*all_buttons)
    kb.row(cart)
    kb.row(back)
    return kb






