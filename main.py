import aiogram.bot.api
from aiogram import Bot, Dispatcher, executor, types
from asyncio import sleep
import logging
import func
import os

API_TOKEN = str(os.getenv('BOT_TOKEN'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# global
actual_question = ''
total_score = 0
rest_score = 100
current_question = 0


def calcRestScore(rest_score: int, curr_score: int):
    return rest_score - curr_score


@dp.message_handler(commands=['test'])
async def start_cmd_handler(message: types.Message):
    global current_question
    questions = func.getQuestionList4Answers()
    qsum = len(questions)
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    # default row_width is 3, so here we can omit it actually
    # kept for clearness
    # await message.reply('Хочешь сыграть в игру? ', reply_markup=types.ReplyKeyboardRemove())
    await sleep(1)
    if len(questions) > 0:
        msg = questions.pop()
        current_question += 1
        # print(len(questions))
        global actual_question
        actual_question = msg[0]

        #logger.info('The question is %r', msg[0])  # print the text we've got
        # only enabled answers
        btns_text = ('A', 'B', 'C', 'D', 'E')[0:len(msg[2])]
        keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

        # Question on the screen
        message_q = f"Вопрос:{current_question} из {qsum} \n #: {msg[0]}\n   {msg[1]}\n \n Ответы:\n"
        for it in msg[2]:
            message_q += f"{it} \n"
        await message.reply(message_q, reply_markup=keyboard_markup)
    else:
        await message.reply('Вопросов больше нет', reply_markup=keyboard_markup)


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    # pressing of a KeyboardButton is the same as sending the regular message with the same text
    # so, to handle the responses from the keyboard, we need to use a message_handler
    # in real bot, it's better to define message_handler(text="...") for each button
    # but here for the simplicity only one handler is defined
    global total_score
    global rest_score
    button_text = message.text
    #logger.info('The answer is %r', button_text)  # print the text we've got

    if button_text == 'A':
        res = func.voteQuestion(actual_question, 'A', total_score)
    elif button_text == 'B':
        res = func.voteQuestion(actual_question, 'B', total_score)
    elif button_text == 'C':
        res = func.voteQuestion(actual_question, 'C', total_score)
    elif button_text == 'D':
        res = func.voteQuestion(actual_question, 'D', total_score)
    elif button_text == 'E':
        res = func.voteQuestion(actual_question, 'E', total_score)
    else:
        res = "Keep calm...Everything is fine"
    # print(res)
    total_score = res[2]
    rest_score = calcRestScore(rest_score, res[1])
    reply_text = f"{res[0]} на {res[1]} балла \n Итог: {total_score} \n Осталось баллов в вопросах:{rest_score}"
    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())
    # with message, we send types.ReplyKeyboardRemove() to hide the keyboard
    if (rest_score + total_score) / 100 >= 0.8:
        await start_cmd_handler(message)
        if total_score > 80:
            message_success = f"Поздравляю! Тест сдан \n Всего баллов в билете:100 \n Баллов набрано:{total_score} \n Баллов осталось:{rest_score} \n Начать заново: /test "
            await message.reply(message_success, reply_markup=types.ReplyKeyboardRemove())
            # executor.stop_polling(dp)
    else:
        message_total = f"Шансов больше нет..:( Начинай сначала \n Всего баллов в билете:100 \n Баллов набрано:{total_score} \n Баллов осталось:{rest_score} \n Начать заново: /test "
        await message.reply(message_total, reply_markup=types.ReplyKeyboardRemove())
        # executor.stop_polling(dp)


if __name__ == '__main__':
    # executor.start_polling(dp, skip_updates=True)
    executor.start_polling(dp, skip_updates=True, )
