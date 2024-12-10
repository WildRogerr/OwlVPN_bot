from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile
import asyncio
import time
import logging
from config import TOKEN
from config import ADMIN
from config import LINKSUPPORT
from config import TARIFF
from config import PROMOCODE
from config import PROMOTARIFF
from asyncio import sleep
import app.keyboards as kb
from app.owlvpnbackend import database
from app.owlvpnbackend import managebot

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

class data:
    databasemanager = database()
    servermanager = managebot()
    userdata = []
    messages_to_delete = {}
    sent_messages = []

    def update_user_ids(self):
        user_ids = []
        while True:
            user_ids = self.databasemanager.getusers()
            time.sleep(2)
            return user_ids



class sheduler():
    def sent_pay_message(self):
        while True:
            users = data()
            user_ids = users.update_user_ids()
            for user_id in user_ids:
                active_status = data.databasemanager.get_active_status(user_id)
                pay_day = data.databasemanager.get_pay_day(user_id)
                day_of_mounth = data.databasemanager.get_day_of_mount()
                hour = data.databasemanager.get_hour()
                if active_status == 1 and pay_day == day_of_mounth and hour == 12:
                    data.databasemanager.set_left_days(user_id,code=1)
                    end_day = data.databasemanager.three_days_counter()
                    data.databasemanager.set_end_day(user_id,end_day)
                    bot.send_message(user_id, 'Добрый день, сегодня день оплаты по вашему тарифу, пожалуйста оплатите следующий месяц с помощью кнопки "Произвести оплату".')
            time.sleep(600)

    def countdown_shutdown():
        while True:    
            users = data()
            user_ids = users.update_user_ids()
            for user_id in user_ids:
                left_days = data.databasemanager.get_left_days(user_id)
                if left_days == 1:
                    while True:
                        end_day = data.databasemanager.get_end_day()
                        day_of_mounth = data.databasemanager.get_day_of_mount()
                        hour = data.databasemanager.get_hour()
                        remaining_time = end_day - day_of_mounth
                        if remaining_time <= 1 and remaining_time > 0 and hour >= 12:
                            bot.send_message(user_id, 'Добрый день, у вас остался 1 день, чтоб осуществить оплату за следующий месяц, иначе ваш аккаунт будет деактивирован до осуществления оплаты. Пожалуйста оплатите следующий месяц с помощью кнопки "Произвести оплату".')
                        elif remaining_time <= 0 and hour >= 12:
                            bot.send_message(user_id, 'Добрый день, Ваш аккаунт деактивирован до поступления средств. Оплатите следующий месяц с помощью кнопки "Произвести оплату" и аккаунт будет активирован вновь.')   
                            data.databasemanager.set_left_days(user_id,code=0)
                            data.databasemanager.set_end_day(user_id,end_day=0)
                            data.databasemanager.active_status(user_id,code=False)
                            client_name = data.databasemanager.get_client_name(user_id)
                            data.servermanager.active_server_switch(user_id,client_name)
                        break
            time.sleep(600)



@dp.message(Command('start'))
async def start(message: Message):
    if message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
        except Exception as e:
            print(f"Ошибка удаления: {e}")
    with open('./txt/welcome.txt','r',encoding="utf-8") as file:
        welcome = file.read()
    new_message = await message.answer(welcome, parse_mode='html', reply_markup=kb.connectkeys)
    data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(Command('help'))#do_later
async def help(message: Message): 
    with open('./txt/help.txt','r',encoding="utf-8") as file:
        help = file.read()
        await message.answer(help, parse_mode='html')
    
@dp.message(Command('support'))#do_later
async def support(message: Message): 
    await message.answer(f'Напишите ваш вопрос или опишите проблему по слудующей ссылке: {LINKSUPPORT}. Прежде чем написать в поддержку посмотрите пожалуйста раздел "F.A.Q.", возможно там уже есть решение вашего вопроса.',parse_mode='html')

@dp.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN:
        await message.answer('Добро пожаловать в режим администратора!', reply_markup=kb.adminkeyboard)
    else:
        message.answer("У вас нет прав на выполнение этой команды.")

@dp.message(Command('broadcast'))
async def broadcast(message: Message):
    user_request = message.from_user.id
    if user_request != ADMIN:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return

    if len(message.text.split()) < 2:
        await message.answer('Пожалуйста, введите текст для рассылки:\n"/broadcast Текст сообщения"')
        return
    
    text = message.text.split(maxsplit=1)[1]

    successful = 0
    failed = 0

    data.sent_messages.clear()
    users = data()
    user_ids = users.update_user_ids()
    for user_id in user_ids:
        try:
            sent_message = await bot.send_message(user_id, text)
            successful += 1
            data.sent_messages.append({
                'chat_id': user_id,
                'message_id': sent_message.message_id
            })
            await sleep(0.1)  # Задержка для предотвращения лимитов Telegram
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
            failed += 1

    await message.answer(f"Рассылка завершена.\nУспешно: {successful}, Не удалось: {failed}.")

@dp.message(Command('delete_broadcast'))
async def delete_broadcast_command(message: Message):
    user_request = message.from_user.id
    if user_request != ADMIN:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return

    for msg in data.sent_messages:
        try:
            await bot.delete_message(msg['chat_id'], msg['message_id'])
        except Exception as e:
            print(f"Не удалось удалить сообщение {msg['message_id']} у пользователя {msg['chat_id']}: {e}")

    data.sent_messages.clear()
    await message.answer("Все разосланные сообщения удалены.")

@dp.message(F.text == '⚙️ Получить файл конфигурации')
async def text_handler1(message: Message):
    user_id = message.from_user.id
    if data.databasemanager.get_server_account1(user_id):
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        user_id = message.from_user.id
        tariff_number = data.databasemanager.gettariff(user_id)
        client_name = data.databasemanager.get_client_name(user_id)
        if tariff_number == 1:
            tariff = '1 аккаунт'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file)
        elif tariff_number == 2:
            tariff = '2 аккаунта'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
            file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file,caption="Файл 1:")
            await bot.send_document(chat_id=message.chat.id,document=file2,caption="Файл 2:")
        elif tariff_number == 3:
            tariff = '3 аккаунта'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
            file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
            file3 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}3/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file,caption="Файл 1:")
            await bot.send_document(chat_id=message.chat.id,document=file2,caption="Файл 2:")
            await bot.send_document(chat_id=message.chat.id,document=file3,caption="Файл 3:")
        elif tariff_number == 4:
            tariff = '1 аккаунт PROMO'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
            file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file,caption="Для смартфона:")
            await bot.send_document(chat_id=message.chat.id,document=file2,caption="Для PC:")
        elif tariff_number == 5:
            tariff = '2 аккаунта PROMO'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
            file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
            file3 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}3/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file,caption="Для смартфона:")
            await bot.send_document(chat_id=message.chat.id,document=file2,caption="Для PC:")
            await bot.send_document(chat_id=message.chat.id,document=file3,caption="Для смартфона:")
        elif tariff_number == 0:
            tariff = 'Бесплатный'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}1/owlvpn.kz.conf")
            file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file,caption="Для смартфона:")
            await bot.send_document(chat_id=message.chat.id,document=file2,caption="Для PC:")
        else: 
            tariff = 'Не выбран'
            await message.answer(f'Ваш тариф: "{tariff}"')
    else:
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!', reply_markup=kb.paykey)
        data.messages_to_delete[message.chat.id] = new_message.message_id
    
@dp.message(F.text == '✔️ Сменить тариф')
async def text_handler2(message: Message):
    user_id = message.from_user.id
    if data.databasemanager.get_server_account1(user_id):
        await message.delete()
        user_id = message.from_user.id
        tariff_number = data.databasemanager.gettariff(user_id)
        tariff_promo = data.databasemanager.getpromo(user_id)
        if tariff_number == 1:
            tariff = '1 аккаунт'
        elif tariff_number == 2:
            tariff = '2 аккаунта'
        elif tariff_number == 3:
            tariff = '3 аккаунта'
        elif tariff_number == 4:
            tariff = '1 аккаунт PROMO'
        elif tariff_number == 5:
            tariff = '2 аккаунта PROMO'
        elif tariff_number == 0:
            tariff = 'Бесплатный'
        else: 
            tariff = 'Не выбран'

        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        if tariff_promo == 1:
            new_message = await message.answer(f'Ваш тариф: "{tariff}"\n\nВыберите новый тариф с помощью кнопки "Выбрать тариф".',reply_markup=kb.tariffkeys)
        else:
            new_message = await message.answer(f'Ваш тариф: "{tariff}"\n\nВыберите новый тариф с помощью кнопки "Выбрать тариф".',reply_markup=kb.changetariffkeys)
        data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!', reply_markup=kb.paykey)
        data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '💳 Произвести оплату')
async def text_handler3(message: Message):
    user_id = message.from_user.id
    if data.databasemanager.get_server_account1(user_id):
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Нажмите кнопку "Оплатить", чтобы произвести оплату:', reply_markup=kb.paykey)
        data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!', reply_markup=kb.paykey)
        data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '❔ Помощь')#do_later
async def text_handler4(message: Message):
    user_id = message.from_user.id
    if data.databasemanager.get_server_account1(user_id):
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        with open('./txt/help.txt','r',encoding="utf-8") as file:
            help = file.read()
            new_message = await message.answer(help, parse_mode='html')
        data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!', reply_markup=kb.paykey)
        data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '💬 F.A.Q.')#do_later
async def text_handler5(message: Message):
    user_id = message.from_user.id
    if data.databasemanager.get_server_account1(user_id):
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        with open('./txt/faq.txt','r',encoding="utf-8") as file:
            faq = file.read()
            new_message = await message.answer(faq, parse_mode='html')
        data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!', reply_markup=kb.paykey)
        data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '✉️ Написать обращение')#do_later
async def text_handler6(message: Message):
    user_id = message.from_user.id
    if data.databasemanager.get_server_account1(user_id):
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer(f'Напишите ваш вопрос или опишите проблему по слудующей ссылке: {LINKSUPPORT}. Прежде чем написать в поддержку посмотрите пожалуйста раздел "F.A.Q.", возможно там уже есть решение вашего вопроса.',parse_mode='html')
        data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!', reply_markup=kb.paykey)
        data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == PROMOCODE)
async def text_handler7(message: Message):
    await message.delete()
    user_id = message.from_user.id
    users = data()
    user_ids = users.update_user_ids()
    if user_id in user_ids:  
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Промокод принят! Выберите тариф:',reply_markup=kb.promotariffkey)
        data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Прежде чем ввести промокод нажмите кнопку <b>Подключить VPN</b>', parse_mode='html', reply_markup=kb.connectkeys)
        data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == 'Выполнить рассылку сообщений всем пользователям ↗️')
async def text_handler8(message: Message):
    user_request = message.from_user.id
    if user_request != ADMIN:
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Для рассылки сообщения всем пользователям необходимо ввести команду "/broadcast Текст сообщения", после чего произвести отправку', reply_markup=kb.backbtn)
        data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        message.answer("У вас нет прав на выполнение этой команды.")

@dp.message(F.text != ['⚙️ Получить файл конфигурации',
                       '✔️ Сменить тариф',
                       '💳 Произвести оплату',
                       '❔ Помощь',
                       '💬 F.A.Q.',
                       '✉️ Написать обращение',
                       PROMOCODE,
                       'Выполнить рассылку сообщений всем пользователям ↗️'])
async def text_handler9(message: Message):
    await message.answer('Неизвестные данные.')

@dp.callback_query(F.data == 'startvpn')
async def callback(callback: CallbackQuery): 
    await callback.message.delete()
    if callback.message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=data.messages_to_delete[callback.message.chat.id])
        except Exception as e:
            print(f"Ошибка удаления: {e}")
    data.userdata.clear()
    user_id = callback.from_user.id
    firstname = callback.from_user.first_name
    lastname = callback.from_user.last_name
    username = callback.from_user.username
    data.userdata = [user_id, firstname, lastname, username]
    code = data.databasemanager.adduser(data.userdata)
    if code == 0 or code == 4:
        new_message = await callback.message.answer('Выберите тариф с помощью кнопки "Выбрать тариф"\nЕсли у вас есть промокод, нажмите кнопку "Ввести промокод"', reply_markup=kb.startkeys)
    elif code == 1 or code == 2:
        new_message = await callback.message.answer('Добро пожаловать! Вы уже являетесь пользователем сервиса Owl с активным аккаунтом, нажмите кнопку "Продолжить" для входа в главное меню бота.', reply_markup=kb.resumekey)
    elif code == 3:
        new_message = await callback.message.answer('Добро пожаловать! Вы уже являетесь пользователем сервиса Owl, но к сожалению наш аккаунт сейчас не активен.\n\nДля продолжения использования сервиса нажмите кнопку "Продолжить" чтобы войти в главное меню бота, после чего оплатите подписку через кнопку "Произвести оплату"', reply_markup=kb.resumekey)
    data.messages_to_delete[callback.message.chat.id] = new_message.message_id
    
@dp.callback_query(F.data == 'mainchat')
async def callback(callback: CallbackQuery):
    await callback.message.delete()

@dp.callback_query(F.data == 'keyboard')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    startphoto = FSInputFile('./img/startphoto.jpg')
    await bot.send_photo(chat_id=callback.message.chat.id,photo=startphoto)
    with open('./txt/startmessage.txt','r',encoding="utf-8") as file:
            startmessage = file.read()
    await callback.message.answer(startmessage, parse_mode='html', disable_web_page_preview=True, reply_markup=kb.mainkeyboard)
    user_id = callback.message.from_user.id
    tariff_number = data.databasemanager.gettariff(user_id)
    client_name = data.databasemanager.get_client_name(user_id)
    if tariff_number == 1:
        tariff = '1 аккаунт'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file)
    elif tariff_number == 2:
        tariff = '2 аккаунта'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
        file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file,caption="Файл 1:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file2,caption="Файл 2:")
    elif tariff_number == 3:
        tariff = '3 аккаунта'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
        file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
        file3 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}3/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file,caption="Файл 1:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file2,caption="Файл 2:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file3,caption="Файл 3:")
    elif tariff_number == 4:
        tariff = '1 аккаунт PROMO'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
        file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file,caption="Для смартфона:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file2,caption="Для PC:")
    elif tariff_number == 5:
        tariff = '2 аккаунта PROMO'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
        file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
        file3 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}3/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file,caption="Для смартфона:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file2,caption="Для смартфона:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file3,caption="Для PC:")
    elif tariff_number == 0:
        tariff = 'Бесплатный'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}1/owlvpn.kz.conf")
        file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file,caption="Для смартфона:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file2,caption="Для PC:")
    else: 
        tariff = 'Не выбран'
        await callback.message.answer(f'Ваш тариф: "{tariff}"')

@dp.callback_query(F.data == 'promocode')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    new_message = await bot.send_message(callback.message.chat.id, 'Введите промокод и отправьте сообщение:',reply_markup=kb.backbtn)
    data.messages_to_delete[callback.message.chat.id] = new_message.message_id

@dp.callback_query(F.data == 'choosetariff')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    new_message = await callback.message.answer(TARIFF, parse_mode='html', reply_markup=kb.choosetariffkeys)
    data.messages_to_delete[callback.message.chat.id] = new_message.message_id

@dp.callback_query(F.data == 'choosepromotariff')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    new_message = await callback.message.answer(PROMOTARIFF, parse_mode='html', reply_markup=kb.choosepromotariffkeys)
    data.messages_to_delete[callback.message.chat.id] = new_message.message_id

@dp.callback_query(F.data == 'tariff1')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 1
    user_id = callback.from_user.id
    data.databasemanager.addtariff(tariff,user_id)
    data.databasemanager.server_accounts(user_id,code=1)
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff2')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 2
    user_id = callback.from_user.id
    data.databasemanager.addtariff(tariff,user_id)
    data.databasemanager.server_accounts(user_id,code=1)
    data.databasemanager.server_accounts(user_id,code=2)
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff3')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 3
    user_id = callback.from_user.id
    data.databasemanager.addtariff(tariff,user_id)
    data.databasemanager.server_accounts(user_id,code=1)
    data.databasemanager.server_accounts(user_id,code=2)
    data.databasemanager.server_accounts(user_id,code=3)
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff4')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 4
    user_id = callback.from_user.id
    data.databasemanager.server_accounts(user_id,code=1)
    data.databasemanager.server_accounts(user_id,code=2)
    data.databasemanager.addtariff(tariff,user_id)
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff5')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 5
    user_id = callback.from_user.id
    data.databasemanager.addtariff(tariff,user_id)
    data.databasemanager.server_accounts(user_id,code=1)
    data.databasemanager.server_accounts(user_id,code=2)
    data.databasemanager.server_accounts(user_id,code=3)
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'chtariff1')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 1
    user_id = callback.from_user.id
    data.databasemanager.addtariff(tariff,user_id)
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff2')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 2
    user_id = callback.from_user.id
    data.databasemanager.addtariff(tariff,user_id)
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff3')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 3
    user_id = callback.from_user.id
    data.databasemanager.addtariff(tariff,user_id)
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff4')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 4
    user_id = callback.from_user.id
    data.databasemanager.addtariff(tariff,user_id)
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff5')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 5
    user_id = callback.from_user.id
    data.databasemanager.addtariff(tariff,user_id)
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'pay')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Оплата прошла успешно! Нажмите кнопку "Продолжить"',reply_markup=kb.resumekey)

@dp.callback_query(F.data == 'pay2')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Оплата прошла успешно!')

message_sender = sheduler()
message_sender.sent_pay_message()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')