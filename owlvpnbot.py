from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery,InputMediaPhoto
from aiogram.types.input_file import FSInputFile
from functools import wraps
import asyncio
import time
import logging
from config import TOKEN,ADMIN,LINKSUPPORT,TARIFF,PROMOCODE,PROMOTARIFF,CARDNUMBER,TARIFF1,TARIFF2,TARIFF3,TARIFF4,TARIFF5
from asyncio import sleep
import app.keyboards as kb
from app.owlvpnbackend import Database
from app.owlvpnbackend import Managebot
from app.owlvpnbackend import Logger

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

class Data:
    logger = Logger()
    databasemanager = Database()
    servermanager = Managebot()
    userdata = []
    messages_to_delete = {}
    sent_messages = []

    def update_user_ids(self):
        user_ids = []
        while True:
            user_ids = self.databasemanager.getusers()
            time.sleep(2)
            return user_ids

def check_ban_user_message(databasemanager):
    def decorator_message(handler):
        @wraps(handler)
        async def wrapper(message: Message, *args, **kwargs):
            user_id = message.from_user.id
            try:
                ban_status = databasemanager.get_ban(user_id)
                if ban_status == 1:
                    await message.delete()
                    if message.chat.id in Data.messages_to_delete:
                        try:
                            await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
                        except Exception as e:
                            print(f"Ошибка удаления: {e}")
                    new_message = await message.answer(
                        "Сожалеем, ваш аккаунт был забанен за нарушения правил сервиса. "
                        "Если вы не нарушали правила, напишите в техподдержку, команда: /support."
                    )
                    Data.messages_to_delete[message.chat.id] = new_message.message_id
                    return
            except:
                pass
            return await handler(message, *args, **kwargs)
        return wrapper
    return decorator_message

def check_ban_user_callback(databasemanager):
    def decorator_callback(handler):
        @wraps(handler)
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            user_id = callback.from_user.id
            try:
                ban_status = databasemanager.get_ban(user_id)
                if ban_status == 1:
                    await callback.message.delete()
                    await callback.message.answer(
                        "Сожалеем, ваш аккаунт был забанен за нарушения правил сервиса. "
                        "Если вы не нарушали правила, напишите в техподдержку, команда: /support."
                    )
                    return
            except:
                pass
            return await handler(callback, *args, **kwargs)
        return wrapper
    return decorator_callback



class sheduler():
    async def sent_pay_message(self):
        while True:
            users = Data()
            user_ids = users.update_user_ids()
            for user_id in user_ids:
                active_status = await Data.databasemanager.get_active_status(user_id)
                pay_day = await Data.databasemanager.get_pay_day(user_id)
                day_of_month = await Data.databasemanager.get_day_of_month()
                hour = await Data.databasemanager.get_hour()
                next_month = await Data.databasemanager.get_next_month(user_id)
                ban = await Data.databasemanager.get_ban(user_id)
                if active_status == 1 and pay_day <= day_of_month and hour == 12 and next_month != 1 and ban == 0:
                    await Data.databasemanager.set_left_days(user_id,code=1)
                    end_day = await Data.databasemanager.three_days_counter()
                    await Data.databasemanager.set_end_day(user_id,end_day)
                    await bot.send_message(user_id, 'Добрый день! Сегодня день оплаты по вашему тарифу, пожалуйста оплатите следующий месяц с помощью кнопки "Произвести оплату".')
                elif active_status == 1 and pay_day <= day_of_month and hour == 12 and next_month != 1 and ban == 1:
                    await Data.databasemanager.set_left_days(user_id,code=1)
                    end_day = await Data.databasemanager.three_days_counter()
                    await Data.databasemanager.set_end_day(user_id,end_day)
                elif active_status == 1 and pay_day <= day_of_month and hour == 12 and next_month == 1 and ban == 0:
                    await Data.databasemanager.set_next_month_0(user_id)
            time.sleep(3600)

    async def countdown_shutdown():
        while True:    
            users = Data()
            user_ids = await users.update_user_ids()
            for user_id in user_ids:
                left_days = await Data.databasemanager.get_left_days(user_id)
                ban = await Data.databasemanager.get_ban(user_id)
                if left_days == 1 and ban == 0:
                    while True:
                        end_day = await Data.databasemanager.get_end_day()
                        day_of_month = await Data.databasemanager.get_day_of_month()
                        hour = await Data.databasemanager.get_hour()
                        remaining_time = end_day - day_of_month
                        if remaining_time <= 1 and remaining_time > 0 and hour == 12:
                            await bot.send_message(user_id, 'Добрый день! У вас остался 1 день, чтоб осуществить оплату за следующий месяц, иначе ваш аккаунт будет деактивирован до осуществления оплаты. Пожалуйста оплатите следующий месяц с помощью кнопки "Произвести оплату".')
                        elif remaining_time <= 0 and hour >= 12:
                            await bot.send_message(user_id, 'Добрый день! Ваш аккаунт деактивирован до поступления средств. Оплатите следующий месяц с помощью кнопки "Произвести оплату" и аккаунт будет активирован вновь.')   
                            active_status = await Data.databasemanager.get_active_status(user_id)
                            client_name = await Data.databasemanager.get_client_name(user_id)
                            await Data.databasemanager.set_left_days(user_id,code=0)
                            await Data.databasemanager.set_end_day(user_id,end_day=0)
                            await Data.databasemanager.active_status(user_id,code=False)
                            await Data.servermanager.active_server_switch(user_id,client_name,active_status)
                        break
                elif left_days == 1 and ban == 1:
                    while True:
                        end_day = await Data.databasemanager.get_end_day()
                        day_of_month = await Data.databasemanager.get_day_of_month()
                        hour = await Data.databasemanager.get_hour()
                        remaining_time = end_day - day_of_month
                        if remaining_time <= 0 and hour == 12:
                            active_status = await Data.databasemanager.get_active_status(user_id)
                            client_name = await Data.databasemanager.get_client_name(user_id)
                            await Data.databasemanager.set_left_days(user_id,code=0)
                            await Data.databasemanager.set_end_day(user_id,end_day=0)
                            await Data.databasemanager.active_status(user_id,code=False)
                            await Data.servermanager.active_server_switch(user_id,client_name,active_status)
                        break
            time.sleep(3600)



@dp.message(Command('start'))
@check_ban_user_message(Data.databasemanager)
async def start(message: Message):
    user_id = message.from_user.id
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    username = message.from_user.username
    if message.chat.id in Data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
        except Exception as e:
            print(f"Ошибка удаления: {e}")
    with open('./txt/welcome.txt','r',encoding="utf-8") as file:
        welcome = file.read()
    new_message = await message.answer(welcome, parse_mode='html', reply_markup=kb.connectkeys)
    Data.messages_to_delete[message.chat.id] = new_message.message_id
    data = f"User {user_id}, {firstname} {lastname}, {username} strated bot."
    Data.logger.log(data)

@dp.message(Command('help'))
async def help(message: Message): 
    with open('./txt/help.txt','r',encoding="utf-8") as file:
        help = file.read()
        image1 = FSInputFile('./img/AmneziaVPN_screen1.jpg')
        image2 = FSInputFile('./img/AmneziaVPN_screen2.jpg')
        image3 = FSInputFile('./img/AmneziaVPN_screen3.jpg')
        image4 = FSInputFile('./img/AmneziaVPN_screen4.jpg')
        image5 = FSInputFile('./img/AmneziaVPN_screen5.jpg')
        image6 = FSInputFile('./img/AmneziaWG_screen1.jpg')
        image7 = FSInputFile('./img/AmneziaWG_screen2.jpg')
        image8 = FSInputFile('./img/AmneziaWG_screen3.jpg')
        image9 = FSInputFile('./img/AmneziaWG_screen4.jpg')
        media_group = [
        InputMediaPhoto(media=image1, caption="Скриншот 1: Нажать кнопку"),
        InputMediaPhoto(media=image2, caption="Скриншот 2: Загрузить скачанный конфигурационный файл"),
        InputMediaPhoto(media=image3, caption="Скриншот 3: Нажать кнопку"),
        InputMediaPhoto(media=image4, caption="Скриншот 4: Подключиться"),
        InputMediaPhoto(media=image5, caption="Скриншот 5: Подключено!"),
        ]
        media_group2 = [
        InputMediaPhoto(media=image6, caption="Скриншот 1: Нажать кнопку +"),
        InputMediaPhoto(media=image7, caption="Скриншот 2: Загрузить скачанный конфигурационный файл"),
        InputMediaPhoto(media=image8, caption="Скриншот 3: Щелкнуть переключатель"),
        InputMediaPhoto(media=image9, caption="Скриншот 4: Подключено!"),
        ]
        await message.answer(help, parse_mode='html')
        await bot.send_media_group(chat_id=message.chat.id, media=media_group)
        await bot.send_media_group(chat_id=message.chat.id, media=media_group2)
        
        
    
@dp.message(Command('support'))
async def support(message: Message): 
    await message.answer(f'Напишите ваш вопрос или опишите проблему по следующей ссылке: {LINKSUPPORT}. Прежде чем написать в поддержку посмотрите пожалуйста раздел "F.A.Q.", возможно там уже есть решение вашего вопроса.',parse_mode='html')

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

    Data.sent_messages.clear()
    users = Data()
    user_ids = users.update_user_ids()
    for user_id in user_ids:
        try:
            sent_message = await bot.send_message(user_id, text)
            successful += 1
            Data.sent_messages.append({
                'chat_id': user_id,
                'message_id': sent_message.message_id
            })
            await sleep(0.1)  # Задержка для предотвращения лимитов Telegram
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
            failed += 1

    await message.answer(f"Рассылка завершена.\nУспешно: {successful}, Не удалось: {failed}.")
    data = f"Broadcast successful. Success: {successful}, Lose: {failed}."
    Data.logger.log(data)

@dp.message(Command('delete_broadcast'))
async def delete_broadcast_command(message: Message):
    user_request = message.from_user.id
    if user_request != ADMIN:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return

    for msg in Data.sent_messages:
        try:
            await bot.delete_message(msg['chat_id'], msg['message_id'])
        except Exception as e:
            print(f"Не удалось удалить сообщение {msg['message_id']} у пользователя {msg['chat_id']}: {e}")

    Data.sent_messages.clear()
    await message.answer("Все разосланные сообщения удалены.")
    data = "Delete broadcast."
    Data.logger.log(data)

@dp.message(Command('ban'))
async def ban(message: Message):
    user_request = message.from_user.id
    if user_request != ADMIN:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return

    if len(message.text.split()) < 2:
        await message.answer('Пожалуйста, введите id пользователя для занесения в бан лист:\n"/ban user_id"')
        return
    
    userid = message.text.split(maxsplit=1)[1]
    try:
        firstlastname = Data.databasemanager.get_first_last_name(userid)
        username = Data.databasemanager.get_username(userid)
        Data.databasemanager.set_ban(userid,code=1)
        await message.answer(f"Пользователь: {userid}, {firstlastname}, @{username} забанен.")
        data = f"User {userid}, {firstlastname}, {username} banned."
        Data.logger.log(data)
    except:
        await message.answer(f"Пользователь {userid} не найден в базе данных.")

@dp.message(Command('unban'))
async def unban(message: Message):
    user_request = message.from_user.id
    if user_request != ADMIN:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return

    if len(message.text.split()) < 2:
        await message.answer('Пожалуйста, введите id пользователя для удаления из бан листа:\n"/unban user_id"')
        return
    
    userid = message.text.split(maxsplit=1)[1]
    try:
        firstlastname = Data.databasemanager.get_first_last_name(userid)
        username = Data.databasemanager.get_username(userid)
        Data.databasemanager.set_ban(userid,code=0)
        await message.answer(f"Пользователь: {userid}, {firstlastname}, @{username} разбанен.")
        data = f"User {userid}, {firstlastname}, {username} unbanned."
        Data.logger.log(data)
    except:
        await message.answer(f"Пользователь {userid} не найден в базе данных.")

@dp.message(F.text == '⚙️ Получить файл конфигурации')
@check_ban_user_message(Data.databasemanager)
async def text_handler1(message: Message):
    user_id = message.from_user.id
    if Data.databasemanager.get_server_account1(user_id):
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        user_id = message.from_user.id
        tariff_number = Data.databasemanager.gettariff(user_id)
        client_name = Data.databasemanager.get_client_name(user_id)
        pay_day = Data.databasemanager.get_pay_day(user_id)
        if tariff_number == 1:
            tariff = '1 аккаунт'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file)
        elif tariff_number == 2:
            tariff = '2 аккаунта'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
            file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file,caption="Файл 1:")
            await bot.send_document(chat_id=message.chat.id,document=file2,caption="Файл 2:")
        elif tariff_number == 3:
            tariff = '3 аккаунта'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
            file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
            file3 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}3/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file,caption="Файл 1:")
            await bot.send_document(chat_id=message.chat.id,document=file2,caption="Файл 2:")
            await bot.send_document(chat_id=message.chat.id,document=file3,caption="Файл 3:")
        elif tariff_number == 4:
            tariff = '1 аккаунт PROMO'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
            file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file,caption="Для смартфона:")
            await bot.send_document(chat_id=message.chat.id,document=file2,caption="Для PC:")
        elif tariff_number == 5:
            tariff = '2 аккаунта PROMO'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
            file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
            file3 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}3/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file,caption="Для смартфона:")
            await bot.send_document(chat_id=message.chat.id,document=file2,caption="Для PC:")
            await bot.send_document(chat_id=message.chat.id,document=file3,caption="Для смартфона:")
        elif tariff_number == 0:
            tariff = 'Бесплатный'
            file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}1/owlvpn.kz.conf")
            file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
            await message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
            await bot.send_document(chat_id=message.chat.id,document=file,caption="Для смартфона:")
            await bot.send_document(chat_id=message.chat.id,document=file2,caption="Для PC:")
        else: 
            tariff = 'Не выбран'
            await message.answer(f'Ваш тариф: "{tariff}"')
    else:
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!')
        Data.messages_to_delete[message.chat.id] = new_message.message_id
    
@dp.message(F.text == '✔️ Сменить тариф')
@check_ban_user_message(Data.databasemanager)
async def text_handler2(message: Message):
    user_id = message.from_user.id
    if Data.databasemanager.get_server_account1(user_id):
        await message.delete()
        user_id = message.from_user.id
        tariff_number = Data.databasemanager.gettariff(user_id)
        tariff_promo = Data.databasemanager.getpromo(user_id)
        pay_day = Data.databasemanager.get_pay_day(user_id)
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

        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        if tariff_promo == 1:
            new_message = await message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВыберите новый тариф с помощью кнопки "Выбрать тариф".',reply_markup=kb.tariffkeys)
        else:
            new_message = await message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВыберите новый тариф с помощью кнопки "Выбрать тариф".',reply_markup=kb.changetariffkeys)
        Data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!')
        Data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '💳 Произвести оплату')
@check_ban_user_message(Data.databasemanager)
async def text_handler3(message: Message):
    user_id = message.from_user.id
    if Data.databasemanager.get_server_account1(user_id):
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        next_month = Data.databasemanager.get_next_month(user_id)
        pay_day = Data.databasemanager.get_pay_day(user_id)
        if next_month == 0:
            new_message = await message.answer('Нажмите кнопку "Оплатить", чтобы произвести оплату:', reply_markup=kb.paykey)
            Data.messages_to_delete[message.chat.id] = new_message.message_id
        else:
            new_message = await message.answer(f'Оплата за следующий месяц уже произведена, оплатите после {pay_day}го числа', reply_markup=kb.backkey)
            Data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!')
        Data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '❔ Помощь')#do_later
@check_ban_user_message(Data.databasemanager)
async def text_handler4(message: Message):
    user_id = message.from_user.id
    if Data.databasemanager.get_server_account1(user_id):
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        with open('./txt/help.txt','r',encoding="utf-8") as file:
            help = file.read()
            image1 = FSInputFile('./img/AmneziaVPN_screen1.jpg')
            image2 = FSInputFile('./img/AmneziaVPN_screen2.jpg')
            image3 = FSInputFile('./img/AmneziaVPN_screen3.jpg')
            image4 = FSInputFile('./img/AmneziaVPN_screen4.jpg')
            image5 = FSInputFile('./img/AmneziaVPN_screen5.jpg')
            image6 = FSInputFile('./img/AmneziaWG_screen1.jpg')
            image7 = FSInputFile('./img/AmneziaWG_screen2.jpg')
            image8 = FSInputFile('./img/AmneziaWG_screen3.jpg')
            image9 = FSInputFile('./img/AmneziaWG_screen4.jpg')
            media_group = [
            InputMediaPhoto(media=image1, caption="Скриншот 1: Нажать кнопку"),
            InputMediaPhoto(media=image2, caption="Скриншот 2: Загрузить скачанный конфигурационный файл"),
            InputMediaPhoto(media=image3, caption="Скриншот 3: Нажать кнопку"),
            InputMediaPhoto(media=image4, caption="Скриншот 4: Подключиться"),
            InputMediaPhoto(media=image5, caption="Скриншот 5: Подключено!"),
            ]
            media_group2 = [
            InputMediaPhoto(media=image6, caption="Скриншот 1: Нажать кнопку +"),
            InputMediaPhoto(media=image7, caption="Скриншот 2: Загрузить скачанный конфигурационный файл"),
            InputMediaPhoto(media=image8, caption="Скриншот 3: Щелкнуть переключатель"),
            InputMediaPhoto(media=image9, caption="Скриншот 4: Подключено!"),
            ]
            new_message = await message.answer(help, parse_mode='html')
            await bot.send_media_group(chat_id=message.chat.id, media=media_group)
            await bot.send_media_group(chat_id=message.chat.id, media=media_group2)
    else:
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!')
        Data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '💬 F.A.Q.')
@check_ban_user_message(Data.databasemanager)
async def text_handler5(message: Message):
    user_id = message.from_user.id
    if Data.databasemanager.get_server_account1(user_id):
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        with open('./txt/faq.txt','r',encoding="utf-8") as file:
            faq = file.read()
            new_message = await message.answer(faq, parse_mode='html')
    else:
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!')
        Data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '✉️ Написать обращение')
@check_ban_user_message(Data.databasemanager)
async def text_handler6(message: Message):
    user_id = message.from_user.id
    if Data.databasemanager.get_server_account1(user_id):
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer(f'Напишите ваш вопрос или опишите проблему по следующей ссылке: {LINKSUPPORT}. Прежде чем написать в поддержку посмотрите пожалуйста раздел "F.A.Q.", возможно там уже есть решение вашего вопроса.',parse_mode='html')
        Data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Команда доступна только для авторизированных пользователей!')
        Data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == PROMOCODE)
@check_ban_user_message(Data.databasemanager)
async def text_handler7(message: Message):
    await message.delete()
    user_id = message.from_user.id
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    username = message.from_user.username
    users = Data()
    user_ids = users.update_user_ids()
    if user_id in user_ids:  
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Промокод принят! Выберите тариф:',reply_markup=kb.promotariffkey)
        Data.messages_to_delete[message.chat.id] = new_message.message_id
        data = f'User {user_id}, {firstname} {lastname}, {username} entered promocode.'
        Data.logger.log(data)
    else:
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Прежде чем ввести промокод нажмите кнопку <b>Подключить VPN</b>', parse_mode='html', reply_markup=kb.connectkeys)
        Data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == 'Выполнить рассылку сообщений ↗️')
async def text_handler8(message: Message):
    user_request = message.from_user.id
    if user_request == ADMIN:
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Для рассылки сообщения всем пользователям необходимо ввести команду "/broadcast Текст сообщения", после чего произвести отправку.', reply_markup=kb.backkey)
        Data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@dp.message(F.text == 'Банлист 🗑')
async def text_handler9(message: Message):
    user_request = message.from_user.id
    if user_request == ADMIN:
        await message.delete()
        if message.chat.id in Data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=Data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        new_message = await message.answer('Список забаненных пользователей:')
        user_ids = Data.databasemanager.getusers()
        for user_id in user_ids:
            ban = Data.databasemanager.get_ban(user_id)
            if ban == 1:
                firstlastname = Data.databasemanager.get_first_last_name(user_id)
                username = Data.databasemanager.get_username(user_id)
                new_message = await message.answer(f"{user_id}, {firstlastname}, @{username}.")
                Data.messages_to_delete[message.chat.id] = new_message.message_id
        new_message = await message.answer('Для того, чтобы забанить пользователя необходимо ввести команду "/ban user_id", после чего произвести отправку\n\nДля того, чтобы разбанить пользователя необходимо ввести команду "/unban user_id", после чего произвести отправку.', reply_markup=kb.backkey)
        Data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@dp.message(F.photo)
@check_ban_user_message(Data.databasemanager)
async def handle_photo(message: Message):
    # photo = message.photo[-1]
    # file_id = photo.file_id
    admin_id = ADMIN
    user_id = message.from_user.id
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    username = message.from_user.username
    await bot.forward_message(chat_id=admin_id, from_chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(admin_id, f'Скриншот оплаты от пользователя: <b>{firstname}</b> <b>{lastname}</b>, <b>@{username}</b>, user_id = <b>{user_id}</b>',parse_mode='html')
    data = f'Pay screenshot of user {user_id}, {firstname} {lastname}, {username} accepted.'
    Data.logger.log(data)
    await message.answer(f'Скриншот отправлен.')

@dp.message(F.document)
@check_ban_user_message(Data.databasemanager)
async def handle_photo_file(message: Message):
    admin_id = ADMIN
    user_id = message.from_user.id
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    username = message.from_user.username
    await bot.forward_message(chat_id=admin_id, from_chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(admin_id, f'Скриншот оплаты от пользователя: <b>{firstname}</b> <b>{lastname}</b>, <b>@{username}</b>, user_id = <b>{user_id}</b>',parse_mode='html')
    data = f'Pay screenshot of user {user_id}, {firstname} {lastname}, {username} accepted.'
    Data.logger.log(data)
    await message.answer(f'Скриншот отправлен.')

@dp.message(F.text != ['⚙️ Получить файл конфигурации',
                       '✔️ Сменить тариф',
                       '💳 Произвести оплату',
                       '❔ Помощь',
                       '💬 F.A.Q.',
                       '✉️ Написать обращение',
                       PROMOCODE,
                       'Выполнить рассылку сообщений ↗️',
                       'Банлист 🗑'])
@check_ban_user_message(Data.databasemanager)
async def text_handler9(message: Message):
    await message.answer('Неизвестные данные.')



@dp.callback_query(F.data == 'startvpn')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery): 
    await callback.message.delete()
    if callback.message.chat.id in Data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=Data.messages_to_delete[callback.message.chat.id])
        except Exception as e:
            print(f"Ошибка удаления: {e}")
    Data.userdata.clear()
    user_id = callback.from_user.id
    firstname = callback.from_user.first_name
    lastname = callback.from_user.last_name
    username = callback.from_user.username
    Data.userdata = [user_id, firstname, lastname, username]
    code = Data.databasemanager.adduser(Data.userdata)
    if code == 0 or code == 4:
        new_message = await callback.message.answer('Выберите тариф с помощью кнопки "Выбрать тариф"\nЕсли у вас есть промокод, нажмите кнопку "Ввести промокод"', reply_markup=kb.startkeys)
    elif code == 1 or code == 2:
        new_message = await callback.message.answer('Добро пожаловать! Вы уже являетесь пользователем сервиса Owl с активным аккаунтом, нажмите кнопку "Продолжить" для входа в главное меню бота.', reply_markup=kb.resumekey)
    elif code == 3:
        new_message = await callback.message.answer('Добро пожаловать! Вы уже являетесь пользователем сервиса Owl, но к сожалению наш аккаунт сейчас не активен.\n\nДля продолжения использования сервиса нажмите кнопку "Продолжить" чтобы войти в главное меню бота, после чего оплатите подписку через кнопку "Произвести оплату"', reply_markup=kb.resumekey)
    Data.messages_to_delete[callback.message.chat.id] = new_message.message_id
    
@dp.callback_query(F.data == 'mainchat')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()

@dp.callback_query(F.data == 'keyboard')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    startphoto = FSInputFile('./img/startphoto.jpg')
    await bot.send_photo(chat_id=callback.message.chat.id,photo=startphoto)
    with open('./txt/startmessage.txt','r',encoding="utf-8") as file:
            startmessage = file.read()
    await callback.message.answer(startmessage, parse_mode='html', disable_web_page_preview=True, reply_markup=kb.mainkeyboard)
    user_id = callback.from_user.id
    firstname = callback.from_user.first_name
    lastname = callback.from_user.last_name
    username = callback.from_user.username
    client_name = Data.databasemanager.get_client_name(user_id)
    tariff_number = Data.databasemanager.gettariff(user_id)
    pay_day = Data.databasemanager.get_pay_day(user_id)
    data = f'User {user_id}, {firstname} {lastname}, {username} received keyboard.'
    Data.logger.log(data)
    if tariff_number == 1:
        tariff = '1 аккаунт'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file)
    elif tariff_number == 2:
        tariff = '2 аккаунта'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
        file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file,caption="Файл 1:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file2,caption="Файл 2:")
    elif tariff_number == 3:
        tariff = '3 аккаунта'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
        file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
        file3 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}3/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file,caption="Файл 1:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file2,caption="Файл 2:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file3,caption="Файл 3:")
    elif tariff_number == 4:
        tariff = '1 аккаунт PROMO'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
        file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file,caption="Для смартфона:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file2,caption="Для PC:")
    elif tariff_number == 5:
        tariff = '2 аккаунта PROMO'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}/owlvpn.kz.conf")
        file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
        file3 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}3/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file,caption="Для смартфона:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file2,caption="Для смартфона:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file3,caption="Для PC:")
    elif tariff_number == 0:
        tariff = 'Бесплатный'
        file = FSInputFile(f"/home/vpnserver/user_configs/{client_name}1/owlvpn.kz.conf")
        file2 = FSInputFile(f"/home/vpnserver/user_configs/{client_name}2/owlvpn.kz.conf")
        await callback.message.answer(f'Ваш тариф: "{tariff}"\n\nЧисло оплаты: {pay_day}\n\nВаш конфигурационный файл(ы):')
        await bot.send_document(chat_id=callback.message.chat.id,document=file,caption="Для смартфона:")
        await bot.send_document(chat_id=callback.message.chat.id,document=file2,caption="Для PC:")
    else: 
        tariff = 'Не выбран'
        await callback.message.answer(f'Ваш тариф: "{tariff}".')

@dp.callback_query(F.data == 'promocode')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    new_message = await bot.send_message(callback.message.chat.id, 'Введите промокод и отправьте сообщение:',reply_markup=kb.backbtn)
    Data.messages_to_delete[callback.message.chat.id] = new_message.message_id

@dp.callback_query(F.data == 'choosetariff')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    new_message = await callback.message.answer(TARIFF, parse_mode='html', reply_markup=kb.choosetariffkeys)
    Data.messages_to_delete[callback.message.chat.id] = new_message.message_id

@dp.callback_query(F.data == 'choosepromotariff')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    new_message = await callback.message.answer(PROMOTARIFF, parse_mode='html', reply_markup=kb.choosepromotariffkeys)
    Data.messages_to_delete[callback.message.chat.id] = new_message.message_id

@dp.callback_query(F.data == 'tariff1')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 1
    user_id = callback.from_user.id
    Data.databasemanager.addtariff(tariff,user_id)
    Data.databasemanager.server_accounts(user_id,code=1)
    data = f'User {user_id}, {callback.from_user.first_name} {callback.from_user.last_name}, {callback.from_user.username} choosed tariff = 1.'
    Data.logger.log(data)
    await callback.message.answer(f'Тариф выбран. Для осуществления оплаты переведите <b>{TARIFF1}</b> по номеру карты (Сбербанк): <u>{CARDNUMBER}</u> без комментариев, отправьте скриншот с информацией о переводе средств в чат и нажмите кнопку "Оплачено".', parse_mode='html',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff2')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 2
    user_id = callback.from_user.id
    Data.databasemanager.addtariff(tariff,user_id)
    Data.databasemanager.server_accounts(user_id,code=1)
    Data.databasemanager.server_accounts(user_id,code=2)
    data = f'User {user_id}, {callback.from_user.first_name} {callback.from_user.last_name}, {callback.from_user.username} choosed tariff = 2.'
    Data.logger.log(data)
    await callback.message.answer(f'Тариф выбран. Для осуществления оплаты переведите <b>{TARIFF2}</b> по номеру карты (Сбербанк): <u>{CARDNUMBER}</u> без комментариев, отправьте скриншот с информацией о переводе средств в чат и нажмите кнопку "Оплачено".', parse_mode='html',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff3')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 3
    user_id = callback.from_user.id
    Data.databasemanager.addtariff(tariff,user_id)
    Data.databasemanager.server_accounts(user_id,code=1)
    Data.databasemanager.server_accounts(user_id,code=2)
    Data.databasemanager.server_accounts(user_id,code=3)
    data = f'User {user_id}, {callback.from_user.first_name} {callback.from_user.last_name}, {callback.from_user.username} choosed tariff = 3.'
    Data.logger.log(data)
    await callback.message.answer(f'Тариф выбран. Для осуществления оплаты переведите <b>{TARIFF3}</b> по номеру карты (Сбербанк): <u>{CARDNUMBER}</u> без комментариев, отправьте скриншот с информацией о переводе средств в чат и нажмите кнопку "Оплачено".', parse_mode='html',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff4')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 4
    user_id = callback.from_user.id
    Data.databasemanager.server_accounts(user_id,code=1)
    Data.databasemanager.server_accounts(user_id,code=2)
    Data.databasemanager.addtariff(tariff,user_id)
    data = f'User {user_id}, {callback.from_user.first_name} {callback.from_user.last_name}, {callback.from_user.username} choosed tariff = 4.'
    Data.logger.log(data)
    await callback.message.answer(f'Тариф выбран. Для осуществления оплаты переведите <b>{TARIFF4}</b> по номеру карты (Сбербанк): <u>{CARDNUMBER}</u> без комментариев, отправьте скриншот с информацией о переводе средств в чат и нажмите кнопку "Оплачено".', parse_mode='html',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff5')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 5
    user_id = callback.from_user.id
    Data.databasemanager.addtariff(tariff,user_id)
    Data.databasemanager.server_accounts(user_id,code=1)
    Data.databasemanager.server_accounts(user_id,code=2)
    Data.databasemanager.server_accounts(user_id,code=3)
    data = f'User {user_id}, {callback.from_user.first_name} {callback.from_user.last_name}, {callback.from_user.username} choosed tariff = 5.'
    Data.logger.log(data)
    await callback.message.answer(f'Тариф выбран. Для осуществления оплаты переведите <b>{TARIFF5}</b> по номеру карты (Сбербанк): <u>{CARDNUMBER}</u> без комментариев, отправьте скриншот с информацией о переводе средств в чат и нажмите кнопку "Оплачено".', parse_mode='html',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'chtariff1')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 1
    user_id = callback.from_user.id
    Data.databasemanager.addtariff(tariff,user_id)
    data = f'User {user_id}, {callback.from_user.first_name} {callback.from_user.last_name}, {callback.from_user.username} changed tariff = 1.'
    Data.logger.log(data)
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff2')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 2
    user_id = callback.from_user.id
    Data.databasemanager.addtariff(tariff,user_id)
    data = f'User {user_id}, {callback.from_user.first_name} {callback.from_user.last_name}, {callback.from_user.username} changed tariff = 2.'
    Data.logger.log(data)
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff3')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 3
    user_id = callback.from_user.id
    Data.databasemanager.addtariff(tariff,user_id)
    data = f'User {user_id}, {callback.from_user.first_name} {callback.from_user.last_name}, {callback.from_user.username} changed tariff = 3.'
    Data.logger.log(data)
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff4')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 4
    user_id = callback.from_user.id
    Data.databasemanager.addtariff(tariff,user_id)
    data = f'User {user_id}, {callback.from_user.first_name} {callback.from_user.last_name}, {callback.from_user.username} changed tariff = 4.'
    Data.logger.log(data)
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff5')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    tariff = 5
    user_id = callback.from_user.id
    Data.databasemanager.addtariff(tariff,user_id)
    data = f'User {user_id}, {callback.from_user.first_name} {callback.from_user.last_name}, {callback.from_user.username} changed tariff = 5.'
    Data.logger.log(data)
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'pay')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    admin_id = ADMIN
    user_id = callback.from_user.id
    firstname = callback.from_user.first_name
    lastname = callback.from_user.last_name
    username = callback.from_user.username
    client_name = Data.databasemanager.get_client_name(user_id)
    tariff = Data.databasemanager.gettariff(user_id)
    Data.databasemanager.set_next_month_0(user_id)
    payrequest = kb.InlineKeyboardMarkup(inline_keyboard=[
    [kb.InlineKeyboardButton(text='✅ Подтвердить платеж', callback_data=f'payconfirmed:{user_id}'),kb.InlineKeyboardButton(text='❌ Платеж не прошел', callback_data=f'payrejected:{user_id}')]
    ])
    await bot.send_message(admin_id, f'Запрос на подтверждение оплаты от пользователя: <b>{firstname}</b> <b>{lastname}</b>, <b>@{username}</b>, user_id = <b>{user_id}</b>',parse_mode='html',reply_markup=payrequest)
    await callback.message.delete()
    await callback.message.answer('Благодарим за оплату, запрос на подтверждение поступления средств отправлен!\n\nПлатеж будет проверен администратором в ближайшее время (2-3 часа), проверка может продлится максимум сутки, если прошло больше времени напишите пожалуйста в техподдержку через кнопку "Написать обращение" или через команду /support.\n\nНажмите кнопку "Продолжить", для доступа в главное меню. Пока платеж проходит обработку установите необходимые приложения и загрузите файл конфигурации по руководству в разделе "Помощь".\n\nПосле подтверждения платежа в чате бота ваш аккаунт будет активирован и вы получите доступ к VPN сервису.',reply_markup=kb.resumekey)
    Data.databasemanager.add_pay_day(user_id)
    Data.servermanager.manage_server_accounts(user_id,client_name,tariff)
    data = f'User {user_id}, {firstname} {lastname}, {username} payd.'
    Data.logger.log(data)

@dp.callback_query(F.data == 'pay2')
@check_ban_user_callback(Data.databasemanager)
async def callback(callback: CallbackQuery):
    admin_id = ADMIN
    user_id = callback.from_user.id
    firstname = callback.from_user.first_name
    lastname = callback.from_user.last_name
    username = callback.from_user.username
    client_name = Data.databasemanager.get_client_name(user_id)
    tariff = Data.databasemanager.gettariff(user_id)
    next_month = Data.databasemanager.next_month(user_id)
    if next_month == 1:
        payrequest = kb.InlineKeyboardMarkup(inline_keyboard=[
        [kb.InlineKeyboardButton(text='✅ Подтвердить платеж', callback_data=f'payconfirmed:{user_id}'),kb.InlineKeyboardButton(text='❌ Платеж не прошел', callback_data=f'payrejected:{user_id}')]
        ])
        await bot.send_message(admin_id, f'Запрос на подтверждение оплаты от пользователя: <b>{firstname}</b> <b>{lastname}</b>, <b>@{username}</b>, user_id = <b>{user_id}</b>',parse_mode='html',reply_markup=payrequest)
        await callback.message.delete()
        await callback.message.answer('Благодарим за оплату, запрос на подтверждение поступления средств отправлен!\n\nПлатеж будет проверен администратором в ближайшее время (2-3 часа), проверка может продлится максимум сутки, если прошло больше времени, напишите пожалуйста в техподдержку через кнопку "Написать обращение" или через команду /support.\n\nЕсли ваш аккаунт был деактивирован, он будет активирован вновь после подтверждения платежа.')
        Data.databasemanager.add_pay_day(user_id)
        Data.servermanager.manage_server_accounts(user_id,client_name,tariff)
        data = f'User {user_id}, {firstname} {lastname}, {username} payd.'
        Data.logger.log(data)
    elif next_month == 2:
        payrequest = kb.InlineKeyboardMarkup(inline_keyboard=[
        [kb.InlineKeyboardButton(text='✅ Подтвердить платеж', callback_data=f'payconfirmed:{user_id}'),kb.InlineKeyboardButton(text='❌ Платеж не прошел', callback_data=f'payrejected:{user_id}')]
        ])
        await bot.send_message(admin_id, f'Запрос на подтверждение оплаты от пользователя: <b>{firstname}</b> <b>{lastname}</b>, <b>@{username}</b>, user_id = <b>{user_id}</b>',parse_mode='html',reply_markup=payrequest)
        await callback.message.delete()
        await callback.message.answer('Благодарим за оплату, вы совершили платеж за следующий месяц, запрос на подтверждение поступления средств отправлен!\n\nПлатеж будет проверен администратором в ближайшее время (2-3 часа), проверка может продлится максимум сутки, если прошло больше времени, напишите пожалуйста в техподдержку через кнопку "Написать обращение" или через команду /support.')
        Data.databasemanager.add_pay_day(user_id)
        Data.servermanager.manage_server_accounts(user_id,client_name,tariff)
        data = f'User {user_id}, {firstname} {lastname}, {username} payd.'
        Data.logger.log(data)

@dp.callback_query(F.data.startswith('payconfirmed'))
async def callback(callback: CallbackQuery):
    user_id = callback.data.split(":")[1]
    active_status = Data.databasemanager.get_active_status(user_id)
    client_name = Data.databasemanager.get_client_name(user_id)
    firstlastname = Data.databasemanager.get_first_last_name(user_id)
    username = Data.databasemanager.get_username(user_id)
    if active_status == 0:
        await callback.message.delete()
        await bot.send_message(user_id, f'Благодарим. Ваш запрос на подтверждение оплаты одобрен! Аккаунт активирован.')
    else:
        await callback.message.delete()
        await bot.send_message(user_id, f'Благодарим. Ваш запрос на подтверждение оплаты одобрен!')
    Data.databasemanager.active_status(user_id,code=True)
    Data.servermanager.active_server_switch(user_id,client_name,active_status)
    await callback.message.answer(f'Уведомление о подтверждении оплаты отправлено пользователю: <b>{user_id}</b>, <b>{firstlastname}</b>, <b>@{username}</b> .',parse_mode='html')
    data = f'User {user_id}, {firstlastname}, {username}, pay confirmed.'
    Data.logger.log(data)

@dp.callback_query(F.data.startswith('payrejected'))
async def callback(callback: CallbackQuery):
    user_id = callback.data.split(":")[1]
    firstlastname = Data.databasemanager.get_first_last_name(user_id)
    username = Data.databasemanager.get_username(user_id)
    await callback.message.delete()
    await bot.send_message(user_id, f'Сожалеем. Ваш запрос на подтверждение оплаты был отклонен, средства не поступили, либо изображение не содержало информацию о подтверждении платежа.\n\nЕсли вы совершили оплату, сделайте скриншот чека из истории переводов, отправьте скриншот и снова нажмите кнопку "Оплачено" в пункте "Произвести оплату".')
    await callback.message.answer(f'Уведомление об отклонении оплаты отправлено пользователю: <b>{user_id}</b>, <b>{firstlastname}</b>, <b>@{username}</b> .',parse_mode='html')
    data = f'User {user_id}, {firstlastname}, {username}, pay rejected.'
    Data.logger.log(data)

if __name__ == '__main__':
    try:
        asyncio.run(main())
        message_sender = sheduler()
        asyncio.run(message_sender.sent_pay_message())
        counter = sheduler()
        asyncio.run(counter.countdown_shutdown())
    except KeyboardInterrupt:
        print('Exit')