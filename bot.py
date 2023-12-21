import asyncio
import configparser

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers.mult_table import register_handlers_mult_table
from handlers.common import register_handlers_common


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать тренировку")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Парсинг файла конфигурации
    config = configparser.ConfigParser()
    config.read('config/bot.ini')

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config["tg_bot"]["token"])
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_mult_table(dp)


    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())