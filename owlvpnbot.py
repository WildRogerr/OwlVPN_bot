from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile
import asyncio
import logging
from config import TOKEN
from config import ADMIN
from config import LINKSUPPORT
from config import TARIF
from config import PROMOCODE
from config import PROMOTARIF
from asyncio import sleep
import app.keyboards as kb
from app.owlvpnbackend import managebot

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

class data:
    messages_to_delete = {}
    user_ids = [ADMIN]#Временно

@dp.message(Command('start'))
async def start(message: Message):
    with open('./txt/welcome.txt','r',encoding="utf-8") as file:
        welcome = file.read()
    await message.answer(welcome, parse_mode='html', reply_markup=kb.connectkeys)

@dp.message(Command('help'))
async def help(message: Message): 
    with open('./txt/help.txt','r',encoding="utf-8") as file:
        help = file.read()
        await message.answer(help, parse_mode='html')
    
@dp.message(Command('support'))
async def support(message: Message): 
    await message.answer(f'Напишите ваш вопрос или опишите проблему по слудующей ссылке: {LINKSUPPORT}',parse_mode='html')

@dp.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN:
        await message.answer('Добро пожаловать в режим администратора!', reply_markup=kb.adminkeyboard)
    else:
        message.answer("У вас нет прав на выполнение этой команды.")

@dp.message(Command('broadcast'))
async def broadcast(message: Message):
    if message.from_user.id != ADMIN:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return

    # Проверяем, что администратор указал текст для рассылки
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

@dp.message(F.text == '⚙️ Получить файл конфигурации')
async def text_handler1(message: Message):
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")
        new_message = await message.answer(f'Ваш тариф:{1} Ваш конфигурационный файл(ы): {2}')
        data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == '✔️ Сменить тариф')
async def text_handler2(message: Message):
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")
        new_message = await message.answer('Выберете тариф с помощью кнопки "Выбрать тариф"\nЕсли у вас есть промокод, нажмите кнопку "Ввести промокод"',reply_markup=kb.chosetarifkeys)
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

@dp.message(F.text == '❔ Помощь')
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

@dp.message(F.text == '💬 F.A.Q.')
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

@dp.message(F.text == '✉️ Написать обращение')
async def text_handler6(message: Message):
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")
        new_message = await message.answer(f'Напишите ваш вопрос или опишите проблему по слудующей ссылке: {LINKSUPPORT}',parse_mode='html')
        data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == PROMOCODE)
async def text_handler7(message: Message):
        await message.delete()
        if message.chat.id in data.messages_to_delete:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=data.messages_to_delete[message.chat.id])
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")
        new_message = await message.answer('Промокод принят! Выберите тариф:',reply_markup=kb.chosepromotarifkey)
        data.messages_to_delete[message.chat.id] = new_message.message_id

@dp.message(F.text == 'Выполнить рассылку сообщения всем пользователям ↗️')
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
    await callback.message.answer('''Выберете тариф с помощью кнопки "Выбрать тариф"\nЕсли у вас есть промокод, нажмите кнопку "Ввести промокод"''', reply_markup=kb.startkeys)
    
@dp.callback_query(F.data == 'mainchat')
async def callback(callback: CallbackQuery):
    await callback.message.delete()

@dp.callback_query(F.data == 'paymessage')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Оплата прошла успешно!')

@dp.callback_query(F.data == 'keyboard')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    startphoto = FSInputFile('./img/startphoto.jpg')
    await bot.send_photo(chat_id=callback.message.chat.id,photo=startphoto)
    with open('./txt/startmessage.txt','r',encoding="utf-8") as file:
            startmessage = file.read()
    await callback.message.answer(startmessage, parse_mode='html', disable_web_page_preview=True, reply_markup=kb.mainkeyboard)

@dp.callback_query(F.data == 'paymessage')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Оплата прошла успешно!')

@dp.callback_query(F.data == 'promocode')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    if callback.message.chat.id in data.messages_to_delete:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=data.messages_to_delete[callback.message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    new_message = await bot.send_message(callback.message.chat.id, 'Введите промокод и отправьте сообщение:',reply_markup=kb.backbtn)
    data.messages_to_delete[callback.message.chat.id] = new_message.message_id

@dp.callback_query(F.data == 'choosetarif')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(TARIF,reply_markup=kb.tarifkeys)

@dp.callback_query(F.data == 'choosepromotarif')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(PROMOTARIF,reply_markup=kb.promotarifkeys)

@dp.callback_query(F.data == 'changetarif')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(TARIF,reply_markup=kb.changetarifkeys)

@dp.callback_query(F.data == 'changepromotarif')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(PROMOTARIF,reply_markup=kb.chpromotarifkeys)

@dp.callback_query(F.data == 'tarif1')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tarif2')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tarif3')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tarif4')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'tarif5')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Нажмите кнопку "Оплатить" для осуществления оплаты',reply_markup=kb.paykeys)

@dp.callback_query(F.data == 'chtarif1')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату"')

@dp.callback_query(F.data == 'chtarif2')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату"')

@dp.callback_query(F.data == 'chtarif3')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату"')

@dp.callback_query(F.data == 'chtarif4')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату"')

@dp.callback_query(F.data == 'chtarif5')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тариф выбран. Для оплаты следующего месяца нажмите кнопку "Произвести оплату"')

@dp.callback_query(F.data == 'pay')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Оплата прошла успешно! Нажмите кнопку "Продолжить"',reply_markup=kb.resumekey)

@dp.callback_query(F.data == 'pay2')
async def callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Оплата прошла успешно!')

    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')