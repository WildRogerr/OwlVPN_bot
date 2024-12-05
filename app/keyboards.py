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
    [InlineKeyboardButton(text='✔️ Выбрать тариф', callback_data='choosetariff'),InlineKeyboardButton(text='➕ Ввести промокод', callback_data='promocode')]
])

backbtn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙', callback_data='startvpn')]
])

tariffkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1 аккаунт', callback_data='tariff1'),InlineKeyboardButton(text='2 аккаунта', callback_data='tariff2'),InlineKeyboardButton(text='3 аккаунта', callback_data='tariff3')],
    [InlineKeyboardButton(text='🔙', callback_data='startvpn')]
])

changetariffkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1 аккаунт', callback_data='chtariff1'),InlineKeyboardButton(text='2 аккаунта', callback_data='chtariff2'),InlineKeyboardButton(text='3 аккаунта', callback_data='chtariff3')],
    [InlineKeyboardButton(text='🔙', callback_data='startvpn')]
]) 

promotariffkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1 аккаунт', callback_data='tariff4'),InlineKeyboardButton(text='2 аккаунта', callback_data='tariff5')],
    [InlineKeyboardButton(text='🔙', callback_data='startvpn')]
])

chpromotariffkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1 аккаунт', callback_data='chtariff4'),InlineKeyboardButton(text='2 аккаунта', callback_data='chtariff5')],
    [InlineKeyboardButton(text='🔙', callback_data='startvpn')]
])

paykeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💳 Оплатить', callback_data='pay')],
    [InlineKeyboardButton(text='🔙', callback_data='choosetariff')]
])

resumekey = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='▶️ Продолжить', callback_data='keyboard')]
])

paykey = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💳 Оплатить', callback_data='keyboard')],
    [InlineKeyboardButton(text='🔙', callback_data='mainchat')]
])

chosepromotariffkey = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✔️ Выбрать тариф', callback_data='choosepromotariff')]
])

chosetariffkeys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✔️ Выбрать тариф', callback_data='changetariff')],
    [InlineKeyboardButton(text='🔙', callback_data='mainchat')]
])