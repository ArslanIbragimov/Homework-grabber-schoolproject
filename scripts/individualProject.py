# -*- coding: utf-8 -*-
import os
from datetime import date
from configobj import ConfigObj
from telethon import TelegramClient
import datetime
import emoji


def path(pathToFile):
    pathMain = os.getcwd().replace('\\', '/').replace('/scripts', '') + pathToFile

    return pathMain


config = ConfigObj(path('/Important/config.ini'))

# Api data from - https://my.telegram.org/

api_id =
api_hash = ''
session_name = ''

client = TelegramClient(session_name, api_id, api_hash)


async def main():
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
        phone_number = int(input('Enter phone number : '))
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Enter code: '))
    await client.start()

    dayToday = datetime.datetime.now().day
    lastdays = 0

    if datetime.datetime.now().weekday() == 6:
        lastdays += 2
    else:
        lastdays += 1

    chatName = config['TlAuth']['class_chat']
    dayMsg = datetime.datetime.now().day - lastdays
    monthMsg = datetime.datetime.now().month
    yearMsg = datetime.datetime.now().year
    dateMsg = date(year=yearMsg, month=monthMsg, day=dayMsg)

    if '@' in chatName:
        chatName
    else:
        async for dialog in client.iter_dialogs():
            if dialog.name == chatName:
                chatName = dialog.name
                break
    f = open(path('/Result/Homework.txt'), 'w')
    async for msg in client.iter_messages(entity=chatName, offset_date=dateMsg, limit=None, reverse=True):
        second = msg.date.second
        minute = msg.date.minute
        hour = msg.date.hour
        entity = await client.get_entity(msg.from_id.user_id)
        hour = str(hour)
        minute = str(minute)
        second = str(second)
        frstName = str(entity.first_name)
        if dayMsg < dayToday:
            if set(msg.text.split()) & set(hWDict):
                print(emoji.emojize(emoji.demojize(str(hour + ':' + minute + ":" + second + ' ' + frstName + ':' + msg.text))))
                f.write(emoji.demojize(str(hour + ':' + minute + ":" + second + ' ' + frstName + ':' + msg.text)))

    f.close()


with client:
    client.loop.run_until_complete(main())
