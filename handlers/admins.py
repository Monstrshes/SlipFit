
import sys
import os

# Получаем абсолютный путь к родительской папке проекта
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
import base64
from maxapi.types import MessageCreated, MessageCallback, Command, InputMediaBuffer
from maxapi import F
from fsm.admin import AFSM, UFSM
from maxapi.enums import parse_mode
from loggs import setup_logging
from config import Config
from keyboards import adminskb
from keyboards.users import menu as user_menu
from more_func.txtinexcel import get_users_buffer
from more_func.downphoto import download_photo_bytes

# Импортируем функции работы с БД
from database.database import *

fsm = AFSM()
fsm1 = UFSM()
admins = Config().admins
logger = setup_logging("admin_handler")

def register_handlers(dp, bot):

    @dp.message_callback(F.callback.payload == 'Admin_Menu')
    async def start_admin_w_callback(event: MessageCallback):
        if fsm.get_state(event.get_ids()[1]) == "add_product_photo":
            ddict = fsm.get_dict(event.get_ids()[1])
            category = ddict["category"]
            del ddict["category"]



            # Сохраняем товар в БД вместо posts
            success = create_product(
                name=ddict.get("product_text", ""),
                description=ddict.get("product_text", ""),
                link=ddict.get("product_link", ""),
                photo_url=ddict.get("product_photo", ""),
                category=category
            )
            if success:
                logger.info(f"Товар добавлен в категорию {category}")
            fsm.clear_dict(event.get_ids()[1])
            fsm.set_state(event.get_ids()[1], "default")
        else:
            fsm.clear_dict(event.get_ids()[1])
            fsm.set_state(event.get_ids()[1], "default")
        try:
            await event.message.delete()
        except Exception as e:
            logger.error(f"Ошибка удаления сообщения с командой /start_admin: {e}")
        fsm1.clear_dict(event.get_ids()[1])
        fsm1.set_state(event.get_ids()[1], "default")
        if event.get_ids()[1] in admins:
            cusers = 0

            text = f"""👋Добро пожаловать, {event.message.sender.first_name}
👉Ваш id: {event.get_ids()[1]}

Информация:
Версия: **1.0.0**
Последнее обновление: **10.03.2026**
Техническая поддержка: https://max.ru/u/f9LHodD0cOLBobEp6AuceJoG7VPihyfA7dDF3kT2gm6QQYE7ofacA3wTsmw

Зарегестрировано пользователей: {cusers}
Количество администраторов: {len(admins)}

👇Выберите дальнейшее действие:
"""
            await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text=text,
                attachments=[adminskb.admin_menu()],
                parse_mode=parse_mode.ParseMode.MARKDOWN
            )
        else:
            pass

    @dp.message_created(Command('start_admin'))
    async def start_admin(event: MessageCreated):
        if event.get_ids()[1] in admins:
            try:
                await event.message.delete()
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения с командой /start_admin: {e}")
            if event.get_ids()[1] in admins:
                cusers = len(get_all_users())
                text = f"""👋Добро пожаловать, {event.message.sender.first_name}
    👉Ваш id: {event.get_ids()[1]}

    Информация:
    Версия: **1.0.0**
    Последнее обновление: **10.03.2026**
    Техническая поддержка: https://max.ru/u/f9LHodD0cOLBobEp6AuceJoG7VPihyfA7dDF3kT2gm6QQYE7ofacA3wTsmw

    Зарегестрировано пользователей: {cusers}
    Количество администраторов: {len(admins)}

    👇Выберите дальнейшее действие:
    """
                fsm.clear_dict(event.get_ids()[1])
                fsm.set_state(event.get_ids()[1], "default")
                await bot.send_message(
                    chat_id=event.message.recipient.chat_id,
                    text=text,
                    attachments=[adminskb.admin_menu()],
                    parse_mode=parse_mode.ParseMode.MARKDOWN
                )
        else:
            await bot.send_message(
                    chat_id=event.message.recipient.chat_id,
                    text="Ты не админ",
                    parse_mode=parse_mode.ParseMode.MARKDOWN
                )

    @dp.message_callback(F.callback.payload == 'APanelGetUsers')
    async def get_list_with_users(event: MessageCallback):
        fsm.clear_dict(event.get_ids()[1])
        fsm.set_state(event.get_ids()[1], "default")
        if event.get_ids()[1] in admins:
            await event.answer()
            await bot.delete_message(
                message_id=event.message.body.mid
            )

            users = get_all_users()
            doc = get_users_buffer(users)
            file = InputMediaBuffer(doc, filename="users.xlsx")
            await bot.send_message(
                    chat_id=event.message.recipient.chat_id,
                    text="Список всех пользователей на данный момент",
                    attachments = [file, adminskb.to_menu()]

        )
        #     except Exception as e:
        #         logger.warning(f"Не удаётся получить список пользователей: {e}")
        #         await bot.send_message(
        #             chat_id=event.message.recipient.chat_id,
        #             text="Ошибка выгрузки пользователей",
        #             parse_mode=parse_mode.ParseMode.MARKDOWN
        # )


    @dp.message_callback(F.callback.payload == 'APanelCatalog')
    async def cat_catalog(event: MessageCallback):
        fsm.clear_dict(event.get_ids()[1])
        fsm.set_state(event.get_ids()[1], "default")
        if event.message.sender.user_id in admins:
            await event.answer()
            await bot.delete_message(
                message_id=event.message.body.mid
            )
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Выберите, что хотите сделать",
            attachments=[adminskb.acatalog()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )


    @dp.message_callback(F.callback.payload == 'ADeletecategory')
    async def delete_category_menu(event: MessageCallback):
        if event.callback.user.user_id in admins:
            await event.answer()
            await bot.delete_message(
                            message_id=event.message.body.mid
        )
        # Получаем список категорий из БД вместо posts.catalog.keys()
        categories = get_categories_from_db()  # Функция ниже
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Выберите категорию для удаления",
            parse_mode=parse_mode.ParseMode.MARKDOWN,
            attachments=[adminskb.delcatalog(categories, "Category")]
        )

    @dp.message_callback(F.callback.payload.startswith('ADelCategory:'))
    async def delete_category(event: MessageCallback):
        if event.callback.user.user_id in admins:
            await event.answer()
            await bot.delete_message(
                message_id=event.message.body.mid
            )
            category = event.callback.payload.split(":")[1]
            # Удаляем категорию из БД
            success = delete_category_from_db(category)
            if success:
                logger.info(f"Категория {category} удалена из БД")
                text = "Категория успешно удалена"
            else:
                text = "Ошибка при удалении категории"
            await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text=text,
                attachments=[adminskb.to_menu()],
                parse_mode=parse_mode.ParseMode.MARKDOWN
            )

    @dp.message_callback(F.callback.payload == "ANewProduct")
    async def add_new_product(event: MessageCallback):
        if event.callback.user.user_id in admins:
            await event.answer()
            await bot.delete_message(
                message_id=event.message.body.mid
            )
            # Получаем категории из БД
            categories = get_categories_from_db()
            await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text="Выберите категорию:",
                attachments=[adminskb.choice_catalog(categories)],
                parse_mode=parse_mode.ParseMode.MARKDOWN
            )

    @dp.message_callback(F.callback.payload == "ANewCategory")
    async def add_new_category(event: MessageCallback):
        if event.callback.user.user_id in admins:
            await event.answer()
            await bot.delete_message(
                message_id=event.message.body.mid
            )
            # Получаем категории из БД
            fsm.set_state(event.callback.user.user_id, "add_category")
            await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text="Введите название категории:",
                attachments=[adminskb.back1()],
                parse_mode=parse_mode.ParseMode.MARKDOWN
            )

    @dp.message_callback(F.callback.payload.startswith("AChoiceCat:"))
    async def choose_category_for_product(event: MessageCallback):
        if event.callback.user.user_id in admins:
            await event.answer()
            await bot.delete_message(
                message_id=event.message.body.mid
            )
            category = event.callback.payload.split(":")[1]
            fsm.append_dict(event.callback.user.user_id, "category", category)
            fsm.set_state(event.callback.user.user_id, "add_product_text")
            await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text="Введите описание товара:",
                attachments=[adminskb.back1()],
                parse_mode=parse_mode.ParseMode.MARKDOWN
            )

    @dp.message_callback(F.callback.payload == 'APanelVideo')
    async def panel_video(event: MessageCallback):
        if event.message.sender.user_id in admins:
            await event.answer()
            await bot.delete_message(
                message_id=event.message.body.mid
            )
        fsm.clear_dict(event.get_ids()[1])
        fsm.set_state(event.get_ids()[1], "default")
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Выберите, что хотите сделать",
            attachments=[adminskb.avideo()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )



    @dp.message_callback(F.callback.payload == "ADeleteVideoCategory")
    async def videos(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        categories = get_all_video_categories()
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Выберите категорию для удаления видео:",
            attachments=[adminskb.delvideo_catalog(categories, "Videocat")],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )
    @dp.message_callback(F.callback.payload.startswith("ADelVideocat"))
    async def delete_video_categories(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        category = event.callback.payload.split(":")[1]
        delete_videos_by_category(category)
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Успешно",
            attachments=[adminskb.to_menu()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )
    @dp.message_callback(F.callback.payload.startswith("AChoiceVideoCat"))
    async def choice_video_categories(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        category = event.callback.payload.split(":")[1]
        fsm.set_state(event.get_ids()[1], "add_video_title")
        fsm.append_dict(event.get_ids()[1], "video_category", category)
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Введите название видео:",
            attachments=[adminskb.back2()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )
    @dp.message_callback(F.callback.payload=="ANewVideo")
    async def new_video(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        categories = get_all_video_categories()
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Выберите категорию, где Вы хотите создать видео:",
            attachments=[adminskb.choice_video_catalog(categories)],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )
    @dp.message_callback(F.callback.payload=="ANewVideoCategory")
    async def choice_video_categories(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        fsm.set_state(event.get_ids()[1], "add_video_category")
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Введите название категории:",
            attachments=[adminskb.back2()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )

    @dp.message_callback(F.callback.payload=="APanelGetMessages")
    async def choice_video_categories(event: MessageCallback):
        await event.answer()
        fsm.set_state(event.get_ids()[1], "enter_text_message")
        await bot.delete_message(message_id=event.message.body.mid)
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Введите полный текст рассылки:",
            attachments=[adminskb.to_menu()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )





    @dp.message_callback(F.callback.payload == 'APanelRecipes')
    async def cet_recipes(event: MessageCallback):
        if event.message.sender.user_id in admins:
            await event.answer()
            await bot.delete_message(
                message_id=event.message.body.mid
            )
        fsm.clear_dict(event.get_ids()[1])
        fsm.set_state(event.get_ids()[1], "default")
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Выберите, что хотите сделать",
            attachments=[adminskb.areceipt()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )

    @dp.message_callback(F.callback.payload == "ADeleteRecipeCategory")
    async def recipes(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        categories = get_all_recipes_categories()
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Выберите категорию для удаления рецепта:",
            attachments=[adminskb.delrecipe_catalog(categories, "Recipescat")],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )
    @dp.message_callback(F.callback.payload.startswith("ADelRecipescat"))
    async def delete_recipe_categories(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        category = event.callback.payload.split(":")[1]
        delete_recipes_by_category(category)
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Успешно",
            attachments=[adminskb.to_menu()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )
    @dp.message_callback(F.callback.payload.startswith("AChoiceRecipeCat"))
    async def choice_recipe_categories(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        category = event.callback.payload.split(":")[1]
        fsm.set_state(event.get_ids()[1], "add_recipe_title")
        fsm.append_dict(event.get_ids()[1], "recipe_category", category)
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Введите название рецепта:",
            attachments=[adminskb.back3()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )
    @dp.message_callback(F.callback.payload=="ANewRecipe")
    async def new_recipe(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        categories = get_all_recipes_categories()
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Выберите категорию, где Вы хотите создать рецепт:",
            attachments=[adminskb.choice_recipe_catalog(categories)],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )
    @dp.message_callback(F.callback.payload=="ANewRecipeCategory")
    async def new_recipe_categories(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        fsm.set_state(event.get_ids()[1], "add_recipe_category")
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Введите название категории:",
            attachments=[adminskb.back3()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )

    @dp.message_callback(F.callback.payload=="Areceips")
    async def new_recipe_categories(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        fsm.set_state(event.get_ids()[1], "default")
        fsm.clear_dict(event.get_ids()[1])
        raffle = get_last_raffle_post()
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Текущий текст и фото розыгрыша:",
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )
        photo_bytes = await download_photo_bytes(raffle['photo'])
        photo = InputMediaBuffer(photo_bytes)
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text=raffle["text"],
            attachments = [photo, adminskb.raffle_admin()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )

    @dp.message_callback(F.callback.payload=="AddRaffle")
    async def new_recipe_categories(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        fsm.set_state(event.get_ids()[1], "add_raffle_text")

        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="Введите новый текст розыгрыша:",
            attachments = [adminskb.back4()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )
    @dp.message_callback(
    F.callback.payload.startswith("edit_video_name:")
)
    async def edit_video_name_prompt(event: MessageCallback):
        chat_id, user_id = event.get_ids()
        if user_id not in admins:
            return
        video_id = event.callback.payload.split(":")[1]
        fsm.append_dict(user_id, "video_id", video_id)
        fsm.set_state(user_id, "set_video_name")
        await bot.send_message(
            chat_id=chat_id,
            text="Введите новое название видео:",
            attachments=[adminskb.back_to_video_menu_kb()]
        )

    @dp.message_callback(
        F.callback.payload.startswith("edit_video_desc:")
    )
    async def edit_video_desc_prompt(event: MessageCallback):
        chat_id, user_id = event.get_ids()
        if user_id not in admins:
            return
        video_id = event.callback.payload.split(":")[1]
        fsm.append_dict(user_id, "video_id", video_id)
        fsm.set_state(user_id, "set_video_ds")
        await bot.send_message(
            chat_id=chat_id,
            text="Введите новое описание видео (можно оставить пустым):",
            attachments=[adminskb.back_to_video_menu_kb()]
        )
    @dp.message_callback(
    F.callback.payload.startswith("edit_recipe_name:")
)
    async def edit_recipe_name_prompt(event: MessageCallback):
        chat_id, user_id = event.get_ids()
        if user_id not in admins:
            return
        recipe_id = event.callback.payload.split(":")[1]
        fsm.append_dict(user_id, "recipe_id", recipe_id)
        fsm.set_state(user_id, "set_recipe_name")
        await bot.send_message(
            chat_id=chat_id,
            text="Введите новое название рецепта:",
            attachments=[adminskb.back_to_recipe_menu_kb()]
        )

    @dp.message_callback(
        F.callback.payload.startswith("edit_recipe_desc:")
    )
    async def edit_recipe_desc_prompt(event: MessageCallback):
        chat_id, user_id = event.get_ids()
        if user_id not in admins:
            return
        recipe_id = event.callback.payload.split(":")[1]
        fsm.append_dict(user_id, "recipe_id", recipe_id)
        fsm.set_state(user_id, "set_recipe_ds")
        await bot.send_message(
            chat_id=chat_id,
            text="Введите новое описание рецепта (можно оставить пустым):",
            attachments=[adminskb.back_to_recipe_menu_kb()]
        )