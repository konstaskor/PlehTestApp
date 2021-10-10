import datetime
import random

import aiogram.bot.api
from aiogram import Bot, Dispatcher, executor, types
from asyncio import sleep
import logging
import utils
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import func
import os

API_TOKEN = str(os.getenv('BOT_TOKEN'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создаем массив сессий
globe_session = utils.Sessions()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)
#print(f"<Constructor {dp.__class__} > ")


@dp.message_handler(commands=['test'])
async def start_cmd_handler(message: types.Message):

    # Sessions for save data in memory
    global globe_session
    #globe_session = utils.Sessions()
    #print(len(globe_session))

    userid = message.from_user.id

    # global globe_session

    # print(userid)
    #print(globe_session)
    if globe_session.sessions.get(userid) is None:
        # добавляем юзера и генерим список вопросов
        globe_session.addUser(userid)



   # print(globe_session.__dict__)
    # print(globe_session.sessions[userid].questions)
    #print(f"{len(globe_session.sessions[userid].questions)} - {userid} INIT len")
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    await sleep(1)
    if len(globe_session.sessions[userid].questions) > 0:

        msg = globe_session.sessions[userid].questions.pop()
     #   print(f"{len(globe_session.sessions[userid].questions)} - {userid} len")
        # print(msg)

        # print(globe_session.sessions[userid].keyboard_available_button.get(msg[0]))

        globe_session.sessions[userid].current_question += 1
        # print(globe_session.sessions[userid].current_question)

        globe_session.sessions[userid].actual_question = msg[0]
        # print(globe_session.sessions[userid].actual_question)

        keyboard_markup.row(
            *(types.KeyboardButton(text) for text in
              globe_session.sessions[userid].keyboard_available_button.get(msg[0])))

        # Question on the screen
        message_q = f"Вопрос:{globe_session.sessions[userid].current_question} из {globe_session.sessions[userid].qsum} \n # {msg[0]}\n   {msg[1]}\n \n Ответы:\n"
        for it in msg[2]:
            message_q += f"{it} \n"
        await message.reply(message_q, reply_markup=keyboard_markup)
    else:
        await message.reply('Вопросов больше нет', reply_markup=keyboard_markup)
        # удаляем все по юзеру
        await globe_session.sessions.pop(userid)


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    userid = message.from_user.id
    global globe_session

    # logger.info('The answer is %r', button_text)  # print the text we've got

    if message.text in ('A', 'B', 'C', 'D', 'E'):
        globe_session.sessions[userid].vote(globe_session.sessions[userid].actual_question, message.text)
    else:
        await message.reply("Введите ответ.Это может быть только буква ABCDE в латинской раскладке",
                            reply_markup=types.ReplyKeyboardRemove())
        # сравнили ответ
    if utils.checkAnswer(globe_session.sessions[userid].actual_question, message.text):
        # обновим тотал
        globe_session.sessions[userid].total_score += utils.score(globe_session.sessions[userid].actual_question)
        # уменьшим оставш баллы
        globe_session.sessions[userid].rest_score -= utils.score(globe_session.sessions[userid].actual_question)
        reply_text = f"Верно! \n Итог: {globe_session.sessions[userid].total_score} \n Осталось вопросов:{len(globe_session.sessions[userid].questions)} \n Осталось баллов в вопросах:{globe_session.sessions[userid].rest_score}"
    else:
        # уменьшим оставш баллы
        globe_session.sessions[userid].rest_score -= utils.score(globe_session.sessions[userid].actual_question)
        reply_text = f"Неверно! \n Верный ответ : {func.getAnswer(globe_session.sessions[userid].actual_question)} \n Итог: {globe_session.sessions[userid].total_score} \n Осталось вопросов:{len(globe_session.sessions[userid].questions)} \n Осталось баллов в вопросах:{globe_session.sessions[userid].rest_score}"

    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())
    # with message, we send types.ReplyKeyboardRemove() to hide the keyboard
    if (globe_session.sessions[userid].rest_score + globe_session.sessions[userid].total_score) / 100 >= 0.8:
        await start_cmd_handler(message)
        if globe_session.sessions[userid].total_score > 80:
            message_success = f"Поздравляю! Тест сдан \n Всего баллов в билете:100 \n Баллов набрано:{globe_session.sessions[userid].total_score} \n Баллов осталось:{globe_session.sessions[userid].rest_score} \n Ваши ответы: { globe_session.sessions[userid].votes } \n Начать заново: /test "

            await message.reply(message_success, reply_markup=types.ReplyKeyboardRemove())
            globe_session.sessions.pop(userid)
    else:
        message_total = f"К сожалению, набрать вожделенные 80 баллов уже не получится:( Начинай сначала \n Всего баллов в билете:100 \n Баллов набрано:{globe_session.sessions[userid].total_score} \n Баллов осталось:{globe_session.sessions[userid].rest_score} \n Ваши ответы: { globe_session.sessions[userid].votes } \n Начать заново: /test "
        await message.reply(message_total, reply_markup=types.ReplyKeyboardRemove())
        globe_session.sessions.pop(userid)


@dp.message_handler()
async def unknown_message(message: types.Message):
    """Ответ на любое неожидаемое сообщение"""
    await message.answer(f"Не понимаю", reply_markup=types.ReplyKeyboardRemove())


async def on_shutdown(dp):
    logging.warning('Shutting down..')
