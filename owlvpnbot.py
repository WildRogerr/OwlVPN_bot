import telebot
from telebot import types
import owlvpnbackend
from owlvpnbackend import managebot

bot = telebot.TeleBot('')

messages_to_delete = {}

admin_ids = [1894714376]

user_ids = [1894714376]

def admin_only(func):
    def wrapper(message):
        if message.chat.id in admin_ids:
            return func(message)
        else:
            bot.reply_to(message.chat.id, "У вас нет доступа к этой команде.")
    return wrapper

@bot.message_handler(commands=['start'])
def main(message):
    with open('./txt/welcome.txt','r',encoding="utf-8") as file:
        welcome = file.read()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('✅ Подключить VPN', callback_data='startvpn'))
    bot.send_message(message.chat.id, welcome, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message): 
    with open('./txt/help.txt','r',encoding="utf-8") as file:
        help = file.read()
        bot.send_message(message.chat.id, help, parse_mode='html')
    
@bot.message_handler(commands=['support'])
def support(message): 
    1

@bot.message_handler(commands=['admin'])
@admin_only
def admin_panel(message):
    bot.reply_to(message, "Добро пожаловать в админ-панель!")
    markup = types.ReplyKeyboardMarkup()
    btncreate = types.KeyboardButton('⚙️ Получить мой файл конфигурации')
    markup.row(btncreate)
    btnbroacast = types.KeyboardButton('Выполнить рассылку сообщения всем пользователям ↗️')
    markup.row(btnbroacast)
    btnhelp = types.KeyboardButton('❔ Помощь')
    btnfaq = types.KeyboardButton('💬 F.A.Q.')
    markup.row(btnhelp, btnfaq)
    btnsup = types.KeyboardButton('✉️ Написать обращение')
    markup.row(btnsup)
    bot.send_message(message.chat.id, 'Добро пожаловать в админ-панель!', reply_markup=markup)

@bot.message_handler(commands=['broadcast'])
@admin_only
def broadcast(message):
    # Получаем текст после команды
    text = message.text[len("/broadcast "):]
    
    if not text:
        bot.reply_to(message, "Пожалуйста, введите текст для рассылки после команды.")
        return

    # Рассылка сообщений всем пользователям
    for user_id in user_ids:
        try:
            bot.send_message(user_id, text)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
    
    bot.reply_to(message, "Рассылка завершена.")

@bot.message_handler(content_types=["text"])
def text_handler(message):
    if message.text == '⚙️ Получить мой файл конфигурации':
        bot.send_message(message.from_user.id, 'Ваш конфигурационный файл:')

    elif message.text == '💳 Произвести оплату':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('💳 Оплатить', callback_data='pay2'))
        bot.send_message(message.from_user.id, "Нажмите кнопку оплатить, чтобы произвести оплату:", reply_markup=markup)

    elif message.text == '❔ Помощь':
        with open('./txt/help.txt','r',encoding="utf-8") as file:
            help = file.read()
            bot.send_message(message.from_user.id, help, parse_mode='html')

    elif message.text == '💬 F.A.Q.':
        with open('./txt/faq.txt','r',encoding="utf-8") as file:
            faq = file.read()
            bot.send_message(message.from_user.id, faq, parse_mode='html')
        
    elif message.text == '✉️ Написать обращение':
        bot.send_message(message.from_user.id, 'Напишите в чём ваша проблема, ответ придёт в ближайшее время') 

    elif message.text == 'XARDAS':
        bot.delete_message(message.chat.id, message.message_id)
        if message.chat.id in messages_to_delete:
            msg_id = messages_to_delete[message.chat.id]
            bot.delete_message(message.chat.id, msg_id)
            del messages_to_delete[message.chat.id]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('✔️ Выбрать тариф', callback_data='choosepromotarif'))
        bot.send_message(message.from_user.id, 'Промокод принят! Выберите тариф:',reply_markup=markup)
        
    elif message.text == '✔️ Сменить тариф':
        bot.delete_message(message.chat.id, message.message_id)
        markup = types.InlineKeyboardMarkup()
        btnchoose = types.InlineKeyboardButton('✔️ Выбрать тариф', callback_data='changetarif')
        markup.row(btnchoose)
        backbtn = types.InlineKeyboardButton('🔙', callback_data='mainchat')
        markup.row(backbtn)
        bot.send_message(message.from_user.id, '''Выберете тариф с помощью кнопки "Выбрать тариф" 
Если у вас есть промокод, нажмите кнопку "Ввести промокод"''',reply_markup=markup)
        
    elif message.text == 'Выполнить рассылку сообщения всем пользователям ↗️':
        bot.delete_message(message.chat.id, message.message_id)
        markup = types.InlineKeyboardMarkup()
        backbtn = types.InlineKeyboardButton('🔙', callback_data='mainchat')
        markup.row(backbtn)
        bot.send_message(message.from_user.id, 'Для рассылки сообщения всем пользователям необходимо ввести команду "broadcast" через slash и текст сообщения после неё, после чего произвести отправку', reply_markup=markup)
        
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Неизвестные данные.') 

@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    if callback.data == 'startvpn':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btnchoose = types.InlineKeyboardButton('✔️ Выбрать тариф', callback_data='choosetarif')
        btnpromo = types.InlineKeyboardButton('➕ Ввести промокод', callback_data='promocode')
        markup.row(btnchoose, btnpromo)
        bot.send_message(callback.message.chat.id, '''Выберете тариф с помощью кнопки "Выбрать тариф" 
Если у вас есть промокод, нажмите кнопку "Ввести промокод"''',reply_markup=markup)
    
    elif callback.data == 'mainchat':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)   
    elif callback.data == 'paymessage':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)   
        bot.send_message(callback.message.chat.id, 'Оплата прошла успешно!')

    elif callback.data == 'keyboard':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.ReplyKeyboardMarkup()
        btncreate = types.KeyboardButton('⚙️ Получить мой файл конфигурации')
        btnchtarif = types.KeyboardButton('✔️ Сменить тариф')
        markup.row(btncreate,btnchtarif)
        btnpay = types.KeyboardButton('💳 Произвести оплату')
        markup.row(btnpay)
        btnhelp = types.KeyboardButton('❔ Помощь')
        btnfaq = types.KeyboardButton('💬 F.A.Q.')
        markup.row(btnhelp, btnfaq)
        btnsup = types.KeyboardButton('✉️ Написать обращение')
        markup.row(btnsup)
        startphoto = open('./img/startphoto.jpg','rb')
        bot.send_photo(callback.message.chat.id, startphoto)
        with open('./txt/startmessage.txt','r',encoding="utf-8") as file:
            startmessage = file.read()
        bot.send_message(callback.message.chat.id, startmessage, parse_mode='html', disable_web_page_preview=True, reply_markup=markup)

    elif callback.data == '4f00f1ca6746ef1367011063d1385ae0304a2a54958c859949a1f38fbeb011a0':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.ReplyKeyboardMarkup()
        btncreate = types.KeyboardButton('⚙️ Получить мой файл конфигурации')
        markup.row(btncreate)
        btnhelp = types.KeyboardButton('❔ Помощь')
        btnfaq = types.KeyboardButton('💬 F.A.Q.')
        markup.row(btnhelp, btnfaq)
        btnsup = types.KeyboardButton('✉️ Написать обращение')
        markup.row(btnsup)
        bot.send_message(callback.message.chat.id, 'Режим администратора.', reply_markup=markup)

    elif callback.data == 'promocode':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        backbtn = types.InlineKeyboardButton('🔙', callback_data='startvpn')
        markup.add(backbtn)
        msg = bot.send_message(callback.message.chat.id, 'Введите промокод и отправьте сообщение:',reply_markup=markup)
        if callback.message.chat.id not in messages_to_delete:
            messages_to_delete[callback.message.chat.id] = []
        messages_to_delete[callback.message.chat.id].extend([msg.message_id])

    elif callback.data == 'choosetarif':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1acc = types.InlineKeyboardButton('1 аккаунт', callback_data='tarif1')
        btn2acc = types.InlineKeyboardButton('2 аккаунта', callback_data='tarif2')
        btn3acc = types.InlineKeyboardButton('3 аккаунта', callback_data='tarif3')
        markup.row(btn1acc, btn2acc, btn3acc)
        backbtn = types.InlineKeyboardButton('🔙', callback_data='startvpn')
        markup.add(backbtn)
        bot.send_message(callback.message.chat.id, '''1 аккаунт - 300 рублей
                         
2 аккаунта - 400 рублей
                         
3 аккаунта - 500 рублей''',reply_markup=markup)

    elif callback.data == 'choosepromotarif':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1pracc = types.InlineKeyboardButton('1 аккаунт', callback_data='tarif4')
        btn2pracc = types.InlineKeyboardButton('2 аккаунта', callback_data='tarif5')
        markup.row(btn1pracc, btn2pracc)
        backbtn = types.InlineKeyboardButton('🔙', callback_data='startvpn')
        markup.add(backbtn)
        bot.send_message(callback.message.chat.id, '''1 аккаунт на 2 устройства (для PC и смартфона) - 150 рублей 
                         
2 аккаунта, 1 на 2 устроства (для PC и смартфона) + 1 аккаунт для смартфона - 250 рублей''',reply_markup=markup)   

    elif callback.data == 'tarif1':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('💳 Оплатить',callback_data='pay'))
        backbtn = types.InlineKeyboardButton('🔙', callback_data='choosetarif')
        markup.add(backbtn)
        bot.send_message(callback.message.chat.id, 'Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=markup)

    elif callback.data == 'tarif2':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('💳 Оплатить',callback_data='pay'))
        backbtn = types.InlineKeyboardButton('🔙', callback_data='choosetarif')
        markup.add(backbtn)
        bot.send_message(callback.message.chat.id, 'Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=markup)

    elif callback.data == 'tarif3':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('💳 Оплатить',callback_data='pay'))
        backbtn = types.InlineKeyboardButton('🔙', callback_data='choosetarif')
        markup.add(backbtn)
        bot.send_message(callback.message.chat.id, 'Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=markup)

    elif callback.data == 'tarif4':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('💳 Оплатить',callback_data='pay'))
        backbtn = types.InlineKeyboardButton('🔙', callback_data='choosepromotarif')
        markup.add(backbtn)
        bot.send_message(callback.message.chat.id, 'Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=markup)

    elif callback.data == 'tarif5':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('💳 Оплатить',callback_data='pay'))
        backbtn = types.InlineKeyboardButton('🔙', callback_data='choosepromotarif')
        markup.add(backbtn)
        bot.send_message(callback.message.chat.id, 'Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=markup)

    elif callback.data == 'changetarif':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1acc = types.InlineKeyboardButton('1 аккаунт', callback_data='chtarif1')
        btn2acc = types.InlineKeyboardButton('2 аккаунта', callback_data='chtarif2')
        btn3acc = types.InlineKeyboardButton('3 аккаунта', callback_data='chtarif3')
        markup.row(btn1acc, btn2acc, btn3acc)
        backbtn = types.InlineKeyboardButton('🔙', callback_data='mainchat')
        markup.add(backbtn)
        bot.send_message(callback.message.chat.id, '''1 аккаунт - 300 рублей
                         
2 аккаунта - 400 рублей
                         
3 аккаунта - 500 рублей''',reply_markup=markup)

    elif callback.data == 'changepromotarif':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1pracc = types.InlineKeyboardButton('1 аккаунт', callback_data='chtarif4')
        btn2pracc = types.InlineKeyboardButton('2 аккаунта', callback_data='chtarif5')
        markup.row(btn1pracc, btn2pracc)
        backbtn = types.InlineKeyboardButton('🔙', callback_data='mainchat')
        markup.add(backbtn)
        bot.send_message(callback.message.chat.id, '''1 аккаунт на 2 устройства (для PC и смартфона) - 150 рублей 
                         
2 аккаунта, 1 на 2 устроства (для PC и смартфона) + 1 аккаунт для смартфона - 250 рублей''',reply_markup=markup)

    elif callback.data == 'chtarif1':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату"')

    elif callback.data == 'chtarif2':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату"')

    elif callback.data == 'chtarif3':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату"')

    elif callback.data == 'chtarif4':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату"')

    elif callback.data == 'chtarif5':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату"')

    elif callback.data == 'pay':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('▶️ Продолжить',callback_data='keyboard'))
        bot.send_message(callback.message.chat.id, 'Оплата прошла успешно! Нажмите кнопку "Продолжить"',reply_markup=markup)
    elif callback.data == 'pay2':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        bot.send_message(callback.message.chat.id, 'Оплата прошла успешно!',reply_markup=markup)

    else:
        bot.send_message(callback.message.chat.id, 'Неизвестная команда')


bot.infinity_polling()