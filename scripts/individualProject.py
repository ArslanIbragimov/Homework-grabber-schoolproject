# -*- coding: utf-8 -*-
import os
from datetime import date
from configobj import ConfigObj
from telethon import TelegramClient
import datetime

from telethon.tl.types import InputMessagesFilterEmpty


def path(pathToFile):
    pathMain = os.getcwd().replace('\\', '/').replace('/scripts', '') + pathToFile

    return pathMain


config = ConfigObj(path('/Important/config.ini'))

# Api data from - https://my.telegram.org/
# Данные об api_id , api_hash брать отсюда - https://my.telegram.org/
api_id = 0
api_hash = ''
session_name = 'HomeworkApp'


client = TelegramClient(session_name, api_id, api_hash)


async def main():
    filter_listFalse = {"False", "false", "f", "FALSE", "F", "0", "афдыу", "Афдыу", "АФДЫУ"}

    filter_listTrue = {"True", "true", "t", "TRUE", "T", "1", "екгу", "Екгу", "ЕКГУ"}
# Фильтр слов для ограничения данных (можно убрать, если в беседе говорят только по делу) 
    hWDict = {
        'упражнения', 'задание', 'уроки', 'работа', 'учёба', 'урок', 'тетрадь', 'занятие', 'дневник', 'учитель',
        'ученик',
        'задача',
        'школа', 'учебник', 'дз', 'Дз', 'дЗ', 'Домашка', 'Домашняя работа', 'домашка', 'домашняя работа', 'завтра',
        'принести', 'расписаться', 'расписание', 'на завтра', 'параграф', 'задачник', 'задали', 'математи', "физ",
        'русс',
        'англ',
        'литер', 'читать', 'прочитать', 'учить', 'выучить', 'Учить', 'Выучить', 'Читать', 'Прочитать', 'Письменно',
        'письменно',
        'Написать', 'написать', 'физику', 'докуменn', 'журнал', 'информатика', 'стра', 'стр'
    }
    if not await client.is_user_authorized():
        # Запрашиваем номер телефона пользователя приложением)
        phone_number = int(input('Enter phone number : '))
        await client.send_code_request(phone_number)
        # В личные сообщения телеграмма приходит сообщение, нужно его ввести
        await client.sign_in(phone_number, input('Enter code: '))
    # Создание сессии    
    await client.start()

    
    dayToday = datetime.datetime.now().day
    lastdays = 0

    if datetime.datetime.now().weekday() == 6:
        lastdays += 2
    else:
        lastdays += 1
    # Парсинг данных из конфига (название чата)
    chatName = config['TlAuth']['class_chat']
    dayMsg = datetime.datetime.now().day - lastdays
    monthMsg = datetime.datetime.now().month
    yearMsg = datetime.datetime.now().year
    dateMsg = date(year=yearMsg, month=monthMsg, day=dayMsg)

    if '@' in chatName:
        pass
    else:
        async for dialog in client.iter_dialogs():
            if dialog.name == chatName:
                chatName = dialog.name
                break
    f = open(path('/Result/Homework.txt'), 'w')
    
    # Парсинг данных из конфига (нужно ли использовать фильтр слов?)
    filter_messages = config['TlSettings']['use_filter']

    async for msg in client.iter_messages(entity=chatName, offset_date=dateMsg, limit=None, reverse=True,
                                          filter=InputMessagesFilterEmpty):
        if not msg.sticker and not msg.media and msg.text:
            second = msg.date.second
            minute = msg.date.minute
            hour = msg.date.hour
            entity = await client.get_entity(msg.from_id.user_id)
            hour = str(hour)
            minute = str(minute)
            second = str(second)
            frstName = str(entity.first_name)
            if dayMsg <= dayToday:
                if filter_messages in filter_listTrue:
                    if set(msg.text.split()) & set(hWDict):
                        print(str(hour + ':' + minute + ":" + second + ' [' + frstName + ']: ' + msg.text))
                        f.write(str(hour + ':' + minute + ":" + second + ' [' + frstName + ']: ' + msg.text))
                if filter_messages in filter_listFalse:
                    print(str(hour + ':' + minute + ":" + second + ' [' + frstName + ']: ' + msg.text))
                    f.write(str(hour + ':' + minute + ":" + second + ' [' + frstName + ']: ' + msg.text))
    # Закрытие потока для вывода информации в текстовый документ
    f.close()


with client:
    client.loop.run_until_complete(main())
