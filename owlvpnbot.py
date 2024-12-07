from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile
import asyncio
import logging
from config import TOKEN
from config import ADMIN
from config import LINKSUPPORT
from config import TARIFF
from config import PROMOCODE
from config import PROMOTARIFF
from asyncio import sleep
import app.keyboards as kb
from app.owlvpnbackend import managebot
from app.owlvpndatabase import database

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

class data:
    managedatabase = database()
    userdata = []
    messages_to_delete = {}
    user_ids = [ADMIN]#do_later

@dp.message(Command('start'))
async def start(message: Message):
    if message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
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

@dp.message(Command('admin'))#do_later
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN:
        await message.answer('Добро пожаловать в режим администратора!', reply_markup=kb.adminkeyboard)
    else:
        message.answer("У вас нет прав на выполнение этой команды.")

@dp.message(Command('broadcast'))#do_later
async def broadcast(message: Message):
    if message.from_user.id != ADMIN:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return

    if len(message.text.split()) < 2:
        await message.answer('Пожалуйста, укажите текст для рассылки:\n"/broadcast Текст сообщения"')
        return
    
    text = message.text.split(maxsplit=1)[1]

    # Получаем всех пользователей из базы данных
    #cursor.execute("SELECT id FROM users")
    #users = cursor.fetchall()

    successful = 0
    failed = 0

    for user_id in data.user_ids:
        try:
            await bot.send_message(user_id, text)
            successful += 1
            await sleep(0.1)  # Задержка для предотвращения лимитов Telegram
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
            failed += 1

    await message.answer(f"Рассылка завершена.\nУспешно: {successful}, Не удалось: {failed}.")

@dp.message(F.text == '⚙️ Получить файл конфигурации')#do_later
async def text_handler1(message: Message):
    await message.delete()
    if message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    await message.answer(f'Ваш тариф:{1} Ваш конфигурационный файл(ы): {2}')

@dp.message(F.text == '✔️ Сменить тариф')#do_later
async def text_handler2(message: Message):
    await message.delete()
    if message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    new_message = await message.answer(f'Ваш тариф: {1}\n\nВыберете тариф с помощью кнопки "Выбрать тариф"\n\nЕсли у вас есть промокод введите его в поле ниже и отправьте сообщение',reply_markup=kb.tariffkeys)
    data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '💳 Произвести оплату')
async def text_handler3(message: Message):
    await message.delete()
    if message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    new_message = await message.answer("Нажмите кнопку оплатить, чтобы произвести оплату:", reply_markup=kb.paykey)
    data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '❔ Помощь')#do_later
async def text_handler4(message: Message):
    await message.delete()
    if message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    with open('./txt/help.txt','r',encoding="utf-8") as file:
        help = file.read()
        new_message = await message.answer(help, parse_mode='html')
    data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '💬 F.A.Q.')#do_later
async def text_handler5(message: Message):
    await message.delete()
    if message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    with open('./txt/faq.txt','r',encoding="utf-8") as file:
        faq = file.read()
        new_message = await message.answer(faq, parse_mode='html')
    data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '✉️ Написать обращение')#do_later
async def text_handler6(message: Message):
    await message.delete()
    if message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    new_message = await message.answer(f'Напишите ваш вопрос или опишите проблему по слудующей ссылке: {LINKSUPPORT}. Прежде чем написать в поддержку посмотрите пожалуйста раздел "F.A.Q.", возможно там уже есть решение вашего вопроса.',parse_mode='html')
    data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == PROMOCODE)#do_later
async def text_handler7(message: Message):
    await message.delete()
    if ADMIN: #do_later   
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")
        new_message = await message.answer('Промокод принят! Выберите тариф:',reply_markup=kb.promotariffkey)
        data.messages_to_delete[message.chat.id] = new_message.message_id
    else:
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")
        new_message = await message.answer('Прежде чем ввести промокод нажмите кнопку "Подключить VPN"')
        data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == 'Выполнить рассылку сообщения всем пользователям ↗️')#do_later
async def text_handler8(message: Message):
    await message.delete()
    if message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    new_message = await message.answer('Для рассылки сообщения всем пользователям необходимо ввести команду "broadcast" через slash и текст сообщения после неё, после чего произвести отправку', reply_markup=kb.backbtn)
    data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text != ['⚙️ Получить файл конфигурации',
                       '✔️ Сменить тариф',
                       '💳 Произвести оплату',
                       '❔ Помощь',
                       '💬 F.A.Q.',
                       '✉️ Написать обращение',
                       PROMOCODE,
                       'Выполнить рассылку сообщения всем пользователям ↗️'])
async def text_handler9(message: Message):
    await message.answer('Неизвестные данные.')

@dp.callback_query(F.data == 'startvpn')
async def callback(callback: CallbackQuery): 
    await callback.message.delete()
    if callback.message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=data.messages_to_delete[callback.message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    data.userdata.clear()
    user_id = callback.from_user.id
    firstname = callback.from_user.first_name
    lastname = callback.from_user.last_name
    username = callback.from_user.username
    data.userdata = [user_id, firstname, lastname, username]
    data.managedatabase.adduser(data.userdata)
    data.userdata.clear()
    code = data.userdata.clear()
    if code == 0 or 4:
        new_message = await callback.message.answer('Выберете тариф с помощью кнопки "Выбрать тариф"\nЕсли у вас есть промокод, нажмите кнопку "Ввести промокод"', reply_markup=kb.startkeys)
    elif code == 1 or 2:
        new_message = await callback.message.answer('Добро пожаловать! Вы уже являетесь пользователем сервиса Owl с активным аккаунтом, нажмите кнопку "Продолжить" для входа в главное меню бота.', reply_markup=kb.resumekey)
    elif code == 3:
        new_message = await callback.message.answer('Добро пожаловать! Вы уже являетесь пользователем сервиса Owl, но к сажелению наш аккаунт сейчас не активен.\n\nДля продолжения использования сервиса нажмите кнопку "Продолжить" чтобы войти в главное меню бота, после чего оплатите подписку через кнопку "Произвести оплату"', reply_markup=kb.resumekey)
    data.messages_to_delete[callback.message.chat.id] = new_message.message_id
    
@dp.callback_query(F.data == 'mainchat')
async def callback(callback: CallbackQuery):
    await callback.message.delete()

@dp.callback_query(F.data == 'keyboard')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    startphoto = FSInputFile('./img/startphoto.jpg')
    await bot.send_photo(chat_id=callback.message.chat.id,photo=startphoto)
    with open('./txt/startmessage.txt','r',encoding="utf-8") as file:
            startmessage = file.read()
    await callback.message.answer(startmessage, parse_mode='html', disable_web_page_preview=True, reply_markup=kb.mainkeyboard)

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

@dp.callback_query(F.data == 'changetariff')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(TARIFF, parse_mode='html', reply_markup=kb.changetariffkeys)

@dp.callback_query(F.data == 'changepromotariff')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(PROMOTARIFF, parse_mode='html', reply_markup=kb.changepromotariffkeys)

@dp.callback_query(F.data == 'tariff1')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff2')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff3')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff4')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tariff5')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'chtariff1')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff2')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff3')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff4')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'chtariff5')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату" и получите новый файл(ы) конфигурации')

@dp.callback_query(F.data == 'pay')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Оплата прошла успешно! Нажмите кнопку "Продолжить"',reply_markup=kb.resumekey)

@dp.callback_query(F.data == 'pay2')#do_later
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Оплата прошла успешно!')

    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')