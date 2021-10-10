from aiogram import executor

import bot

# import utils
# print('---1-----')


# print('---2-----')
executor.start_polling(bot.dp,
                       skip_updates=True,
                       on_shutdown=bot.on_shutdown)
# print('-----3---')
