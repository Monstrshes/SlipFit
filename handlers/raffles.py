import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.database import *
from maxapi import Bot
from keyboards import users

# Создаём один глобальный планировщик
scheduler = AsyncIOScheduler()

def register_raffles(bot: Bot, admins: list):
    """Регистрирует задачи розыгрышей в планировщике"""

    # ========== Еженедельный розыгрыш (каждый понедельник в 21:00) ==========
    async def weekly_raffle_job():
        print("Запуск еженедельного розыгрыша...")
        winner_id = get_weekky_winner()
        if winner_id:
            await send_weekly_raffle_results(winner_id)
            print(f"Розыгрыш завершён. Победитель: {winner_id}")
        else:
            print("Нет участников для еженедельного розыгрыша")

    scheduler.add_job(
        weekly_raffle_job,
        trigger=CronTrigger(day_of_week='mon', hour=15, minute=55),
        id='weekly_raffle'
    )

    # ========== Ежемесячный розыгрыш (каждое воскресенье в 21:00) ==========
    async def monthly_raffle_job():
        print("Запуск ежемесячного розыгрыша...")
        winner_id = get_monthly_winner()  # предполагаемая функция из database
        if winner_id:
            await send_monthly_raffle_results(winner_id)
            print(f"Розыгрыш завершён. Победитель: {winner_id}")
        else:
            print("Нет участников для ежемесячного розыгрыша")

    scheduler.add_job(
        monthly_raffle_job,
        CronTrigger(day=28, hour=21, minute=0),
        id='monthly_raffle'
    )

    # Запускаем планировщик, если он ещё не запущен
    if not scheduler.running:
        scheduler.start()


    # ========== Функции отправки результатов ==========
    async def send_weekly_raffle_results(winner_id: int):
        """Отправляет результаты еженедельного розыгрыша"""
        try:
            # Сообщение победителю
            await bot.send_message(
                user_id=winner_id,  # или chat_id=winner_id – зависит от API
                text="🎉 Поздравляем! Вы выиграли в еженедельном розыгрыше! "
                     "Свяжитесь с организатором/менеджером для получения приза. "
                     "Его аккаунт можно найти в Меню -> Feedback",
                attachments=[users.to_menu()]  # клавиатура отдельно
            )

            participants = get_weekly_participants()  # предполагаемая функция
            announcement_text = (
                f"🤖 Результаты еженедельного розыгрыша!\n"
                f"Победитель: пользователь с ID {winner_id}\n"
            )
            for user_id in participants:
                try:
                    await bot.send_message(
                        user_id=user_id,
                        text=announcement_text,
                        attachments=[users.to_menu()]
                    )
                except Exception:
                    # Игнорируем ошибки отправки
                    pass

            # Уведомление администраторам
            for admin_id in admins:
                try:
                    await bot.send_message(
                        user_id=admin_id,
                        text=announcement_text,
                        attachments=[users.to_menu()]
                    )
                except Exception:
                    pass
        except Exception as e:
            print(f"Ошибка при отправке результатов еженедельного розыгрыша: {e}")

    async def send_monthly_raffle_results(winner_id: int):
        """Отправляет результаты ежемесячного розыгрыша"""
        try:
            await bot.send_message(
                user_id=winner_id,
                text="🎉 Поздравляем! Вы выиграли в ежемесячном розыгрыше! "
                     "Свяжитесь с организатором/менеджером для получения приза. "
                     "Его аккаунт можно найти в Меню -> Feedback",
                attachments=[users.to_menu()]
            )

            participants = get_monthly_participants()  # предполагаемая функция
            announcement_text = (
                f"🤖 Результаты ежемесячного розыгрыша!\n"
                f"Победитель: пользователь с ID {winner_id}\n"
            )
            for user_id in participants:
                try:
                    await bot.send_message(
                        user_id=user_id,
                        text=announcement_text,
                        attachments=[users.to_menu()]
                    )
                except Exception:
                    pass

            for admin_id in admins:
                try:
                    await bot.send_message(
                        user_id=admin_id,
                        text=announcement_text,
                        attachments=[users.to_menu()]
                    )
                except Exception:
                    pass
        except Exception as e:
            print(f"Ошибка при отправке результатов ежемесячного розыгрыша: {e}")