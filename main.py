import asyncio
from maxapi import Bot, Dispatcher
from maxapi.types import BotCommand
from config import Config
from handlers import commands, admins, raffles, message_created
from loggs import setup_logging
from database.database import create_database_tables

logger = setup_logging("main")
config = Config()
create_database_tables()

bot = Bot(token=config.token)
dp = Dispatcher()


def register_handlers():
    commands.register_handlers(dp, bot)
    admins.register_handlers(dp, bot)
    raffles.register_raffles(bot, config.admins)
    message_created.register_handlers(dp, bot)


async def main():
    logger.info('Запуск бота...')

    command = BotCommand(name="start", description="Вернуться в меню/Перезапустить бота")


    await bot.set_my_commands(command)
    # Удаляем webhook перед запуском polling
    try:
        await bot.delete_webhook()
        logger.info('Webhook успешно удалён')
    except Exception as e:
        logger.warning(f'Ошибка при удалении webhook: {e}')

    register_handlers()
    logger.info('Обработчики зарегистрированы')

    # Запускаем бота в режиме опроса обновлений
    await dp.start_polling(bot, skip_updates=True)
    logger.info('Бот остановлен')

if __name__ == '__main__':
    asyncio.run(main())
