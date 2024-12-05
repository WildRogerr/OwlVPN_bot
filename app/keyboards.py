from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

# ReplyKeyboards
mainkeyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='⚙️ Получить файл конфигурации'),KeyboardButton(text='✔️ Сменить тариф')],
    [KeyboardButton(text='💳 Произвести оплату')],
    [KeyboardButton(text='❔ Помощь'),KeyboardButton(text='💬 F.A.Q.')],
    [KeyboardButton(text='✉️ Написать обращение')],
],
                            resize_keyboard=True,
                            input_field_placeholder='Выберите пункт меню...')

adminkeyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='⚙️ Получить файл конфигурации')],
    [KeyboardButton(text='Выполнить рассылку сообщения всем пользователям ↗️')],
    [KeyboardButton(text='❔ Помощь'),KeyboardButton(text='💬 F.A.Q.')],
    [KeyboardButton(text='✉️ Написать обращение')],
],
                            resize_keyboard=True,
                            input_field_placeholder='Выберите пункт меню...')

# InlineKeyboards
connectkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подключить VPN', callback_data='startvpn')]
])

startkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✔️ Выбрать тариф', callback_data='choosetarif'),InlineKeyboardButton(text='➕ Ввести промокод', callback_data='promocode')]
])

backbtn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙', callback_data='startvpn')]
])

tarifkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1 аккаунт', callback_data='tarif1'),InlineKeyboardButton(text='2 аккаунта', callback_data='tarif2'),InlineKeyboardButton(text='3 аккаунта', callback_data='tarif3')],
    [InlineKeyboardButton(text='🔙', callback_data='startvpn')]
])

changetarifkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1 аккаунт', callback_data='chtarif1'),InlineKeyboardButton(text='2 аккаунта', callback_data='chtarif2'),InlineKeyboardButton(text='3 аккаунта', callback_data='chtarif3')],
    [InlineKeyboardButton(text='🔙', callback_data='startvpn')]
]) 

promotarifkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1 аккаунт', callback_data='tarif4'),InlineKeyboardButton(text='2 аккаунта', callback_data='tarif5')],
    [InlineKeyboardButton(text='🔙', callback_data='startvpn')]
])

chpromotarifkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1 аккаунт', callback_data='chtarif4'),InlineKeyboardButton(text='2 аккаунта', callback_data='chtarif5')],
    [InlineKeyboardButton(text='🔙', callback_data='startvpn')]
])

paykeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💳 Оплатить', callback_data='pay')],
    [InlineKeyboardButton(text='🔙', callback_data='choosetarif')]
])

resumekey = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='▶️ Продолжить', callback_data='keyboard')]
])

paykey = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💳 Оплатить', callback_data='keyboard')],
    [InlineKeyboardButton(text='🔙', callback_data='mainchat')]
])

chosepromotarifkey = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✔️ Выбрать тариф', callback_data='choosepromotarif')]
])

chosetarifkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✔️ Выбрать тариф', callback_data='changetarif')],
    [InlineKeyboardButton(text='🔙', callback_data='mainchat')]
])