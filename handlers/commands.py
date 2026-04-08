import sys
import os

# Получаем абсолютный путь к родительской папке проекта
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from maxapi.types import MessageCreated, MessageCallback, BotStarted, Command, InputMedia, InputMediaBuffer
from maxapi.types.attachments.upload import AttachmentUpload, AttachmentPayload
from maxapi.enums.upload_type import UploadType
from maxapi import F
from maxapi.enums import parse_mode
from dict.messages import messagess
from keyboards import users
from loggs import setup_logging
from config import Config
from more_func.downphoto import download_photo_bytes, download_video_bytes
from fsm.admin import UFSM, AFSM
# Импортируем функции работы с БД
from database.database import *

fsm = UFSM()
afsm = AFSM()
admins = Config().admins
logger = setup_logging("users_handler")

def register_handlers(dp, bot):
    @dp.message_callback(F.callback.payload == "start")
    async def start_from_callback(event: MessageCallback):

        if event.get_ids()[1] in admins:
            afsm.set_state(event.get_ids()[1], "default")
            afsm.clear_dict(event.get_ids()[1])
        await event.answer()
        await bot.delete_message(
            message_id=event.message.body.mid
        )
        if event.get_ids()[1] in fsm.user_states.keys():
            fsm.clear_dict(event.get_ids()[1])
            fsm.set_state(event.get_ids()[1], "default")
        else:
            fsm.new_user(event.get_ids()[1])
        photo = InputMedia("static/img/main.jpg")
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text=messagess["start_message"],
            attachments=[photo, users.menu()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )


    @dp.bot_started()
    async def start_from_button(event: BotStarted):
        if event.get_ids()[1] in admins:
            afsm.set_state(event.get_ids()[1], "default")
            afsm.clear_dict(event.get_ids()[1])
        if event.get_ids()[1] not in admins:
            all_users = get_all_users()
            if event.get_ids()[1] not in all_users:
                add_user_to_db(event.get_ids()[1])
        if event.get_ids()[1] in fsm.user_states.keys():
            fsm.clear_dict(event.get_ids()[1])
            fsm.set_state(event.get_ids()[1], "default")
        else:
            fsm.new_user(event.get_ids()[1])
        photo = InputMedia("static/img/main.jpg")
        await bot.send_message(
            chat_id=event.chat_id,
            text=messagess["start_message"],
            attachments=[photo, users.menu()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )

    @dp.message_created(Command('start'))
    async def start_from_command(event: MessageCreated):
        if event.get_ids()[1] in admins:
            afsm.set_state(event.get_ids()[1], "default")
            afsm.clear_dict(event.get_ids()[1])
        elif event.get_ids()[1] not in admins:
            all_users = get_all_users()
            if event.get_ids()[1] not in all_users:
                add_user_to_db(event.get_ids()[1])
        if event.get_ids()[1] in fsm.user_states.keys():
            fsm.clear_dict(event.get_ids()[1])
            fsm.set_state(event.get_ids()[1], "default")
        else:
            fsm.new_user(event.get_ids()[1])
        try:
            await bot.delete_message(
                message_id=event.message.body.mid
            )
        except Exception as e:
            logger.error(f"Ошибка удаления сообщения с командой /start: {e}")
        if event.get_ids()[1] in fsm.user_states.keys():
            fsm.clear_dict(event.get_ids()[1])
            fsm.set_state(event.get_ids()[1], "default")
        else:
            fsm.new_user(event.get_ids()[1])
        photo = InputMedia("static/img/main.jpg")

        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text=messagess["start_message"],
            attachments=[photo, users.menu()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )

    @dp.message_created(Command('end_admin'))
    async def start_from_command(event: MessageCreated):
        if event.get_ids()[1] in admins:
            afsm.set_state(event.get_ids()[1], "default")
            afsm.clear_dict(event.get_ids()[1])
        try:
            await bot.delete_message(
                message_id=event.message.body.mid
            )
        except Exception as e:
            logger.error(f"Ошибка удаления сообщения с командой /start: {e}")
        if event.get_ids()[1] in fsm.user_states.keys():
            fsm.clear_dict(event.get_ids()[1])
            fsm.set_state(event.get_ids()[1], "default")
        else:
            fsm.new_user(event.get_ids()[1])
        photo = InputMedia("static/img/main.jpg")

        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text=messagess["start_message"],
            attachments=[photo, users.menu()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )

    @dp.message_callback(F.callback.payload == "catalog_cat")
    async def catalog_cat(event: MessageCallback):
        await event.answer()
        await bot.delete_message(
            message_id=event.message.body.mid
        )
        photo = InputMedia("static/img/catalog_cat.jpg")
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text=messagess["catalog_cat"],
            attachments=[photo, users.catalog_cat()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )

    @dp.message_callback(F.callback.payload.startswith('catalog:'))
    async def handle_catalog_items(event: MessageCallback):
        await event.answer()
        category = event.callback.payload.split(':')[1]
        item_id = int(event.callback.payload.split(':')[2])

        products = get_products_by_category(category)
        total_items = len(products)

        if total_items == 0:
            await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text="В этой категории пока нет товаров",
                attachments=[users.catalog_cat()],
                parse_mode=parse_mode.ParseMode.MARKDOWN
            )
            return

        if item_id > total_items:
            item_id = 1
        elif item_id < 1:
            item_id = total_items

        await bot.delete_message(
            message_id=event.message.body.mid
        )

        product = get_product_by_index(category, item_id - 1)
        if not product:
            return
        if len(product['description']) > 5:
            text = f"{product['description']}\n\nПосмотреть этот товар на WB: {product['link']}"
        else:
            text = f"\n\nПосмотреть этот товар на WB: {product['link']}"

        photo_bytes = await download_photo_bytes(product['photo_url'])
        photo = InputMediaBuffer(photo_bytes)
        await bot.send_message(
        chat_id=event.message.recipient.chat_id,
        text=text,
        attachments=[photo, users.catalog(category, total_items, product["link"], item_id)],
        parse_mode=parse_mode.ParseMode.MARKDOWN
    )


    @dp.message_callback(F.callback.payload == 'news')
    async def news(event: MessageCallback):
        await event.answer()
        await bot.delete_message(
        message_id=event.message.body.mid)
        photo = InputMedia("static/img/news.jpg")
        await bot.send_message(
        chat_id=event.message.recipient.chat_id,
        text=messagess["news"],
        attachments=[photo, users.menu()],
        parse_mode=parse_mode.ParseMode.MARKDOWN
    )

    @dp.message_callback(F.callback.payload == 'feedback')
    async def feedback(event: MessageCallback):
        await event.answer()
        await bot.delete_message(
        message_id=event.message.body.mid
    )
        photo = InputMedia("static/img/feedback.jpg")
        await bot.send_message(
        chat_id=event.message.recipient.chat_id,
        text=messagess["feedback"],
        attachments=[photo, users.menu()],
        parse_mode=parse_mode.ParseMode.MARKDOWN
    )

    @dp.message_callback(F.callback.payload == "video_cat")
    async def show_video_categories(event: MessageCallback):
        """Показывает список категорий видео"""
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        categories = get_all_video_categories()
        if not categories:
            await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text="Категории видео пока не созданы",
                attachments = [users.to_menu()]
            )
            return

        image = InputMedia("static/img/vide_cat.jpg")
        user_id = event.get_ids()[1]
        is_admin = user_id in admins

        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text=messagess["video_cat"],
            attachments = [image, users.video_cat(is_admin)],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )


    @dp.message_callback(F.callback.payload.startswith('vcatalog:'))
    async def show_videos_in_category(event: MessageCallback):
        category = event.callback.payload.split(':')[1]
        item_id = int(event.callback.payload.split(':')[2])

        videos = get_videos_by_category(category)
        total_items = len(videos)

        if item_id > total_items:
            item_id = 1
        elif item_id < 1:
            item_id = total_items

        if len(videos) == 2:
            empty_video = None
            for v in videos:
                if not v.get('name') or v['name'].strip() == '':
                    empty_video = v
                    break
            if empty_video:
                delete_video(empty_video['id'])   # предполагается, что такая функция существует
                # Обновляем список видео после удаления
                videos = get_videos_by_category(category)
                total_items = len(videos)
                # Корректируем item_id, если удалённое видео было текущим
                if item_id > total_items:
                    item_id = total_items
                if item_id < 1:
                    item_id = 1

        await bot.delete_message(message_id=event.message.body.mid)

        video = get_video_in_category(category, item_id)
        if not video or len(video['name']) < 3:
            is_admin = event.get_ids()[1]  in admins
            await bot.send_message(
                chat_id = event.get_ids()[0],
                text="В это категории пока что ничего нет(. Возвращайтесь сюда позже.",
                attachments = [users.back_to_videos_cat(is_admin, category)]
            )
            return

        user_id = event.get_ids()[1]
        is_admin = user_id in admins   # функция из database.users

        # Формируем текст
        if len(video.get('text', '')) > 5:
            text = f"{video['name']}\n\n{video['text']}"
        else:
            text = video['name']

        # Медиа-вложение
        token = video.get("token")
        if token:
            video_att = AttachmentUpload(
                type=UploadType.VIDEO,
                payload=AttachmentPayload(token=token)
            )
        else:
            video_att = InputMedia(video["video_url"])



        kb = users.viseo_catalog(category, total_items, item_id, is_admin, video["id"])

        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text=text,
            attachments=[video_att, kb],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )



    @dp.message_callback(F.callback.payload == "recipe_cat")
    async def show_recipes_categories(event: MessageCallback):
        """Показывает список категорий видео"""
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        categories = get_all_recipes_categories()
        if not categories:
            await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text="Категории видео пока не созданы",
                attachments = [users.to_menu()]
            )
            return
        fsm.clear_dict(event.get_ids()[1])
        fsm.set_state(event.get_ids()[1], "default")
        image = InputMedia("static/img/recipes_cat.jpg")

        user_id = event.get_ids()[1]
        is_admin = user_id in admins

        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text=messagess["recipes_cat"],
            attachments = [image, users.recipe_cat(is_admin)],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )




    @dp.message_callback(F.callback.payload.startswith('rcatalog:'))
    async def show_recipes_in_category(event: MessageCallback):
        """Показывает видео в выбранной категории"""
        category = event.callback.payload.split(':')[1]
        item_id = int(event.callback.payload.split(':')[2])

        recipes = get_recipes_by_category(category)
        total_items = len(recipes)

        if total_items == 0:
            await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text="В этой категории рецептов",
                attachments=[users.recipe_cat()],
                parse_mode=parse_mode.ParseMode.MARKDOWN
            )
            return

        if item_id > total_items:
            item_id = 1
        elif item_id < 1:
            item_id = total_items

        if len(recipes) == 2:
            empty_recipe = None
            for r in recipes:
                if not r.get('name') or r['name'].strip() == '':
                    empty_recipe = r
                    break
            if empty_recipe:
                delete_recipe(empty_recipe['id'])
                # Обновляем список рецептов после удаления
                recipes = get_recipes_by_category(category)
                total_items = len(recipes)
                # Корректируем item_id, если удалённый рецепт был текущим
                if item_id > total_items:
                    item_id = total_items
                if item_id < 1:
                    item_id = 1

        await bot.delete_message(message_id=event.message.body.mid)

        recipe = get_recipe_in_category(category, item_id)
        if not recipe or len(recipe["name"]) < 3:
            is_admin = event.get_ids()[1]  in admins
            await bot.send_message(
                    chat_id = event.get_ids()[0],
                    text="В это категории пока что ничего нет(. Возвращайтесь сюда позже.",
                    attachments = [users.back_to_recipes_cat(is_admin, category)]
                )
            return



        user_id = event.get_ids()[1]
        is_admin = user_id in admins

        # Формируем текст
        if len(recipe.get('text', '')) > 5:
            text = f"{recipe['name']}\n\n{recipe['text']}"
        else:
            text = recipe['name']

        # Медиа-вложение
        token = recipe.get("video_url")   # предполагаем, что здесь токен, а не ссылка
        if token and token.startswith("http"):   # если это ссылка, то используем InputMedia
            video_att = InputMedia(token)
        elif token:
            video_att = AttachmentUpload(
                type=UploadType.VIDEO,
                payload=AttachmentPayload(token=token)
            )
        else:
            video_att = None   # или что-то по умолчанию

        # Клавиатура

        kb = users.recipe_catalog(category, total_items, item_id, is_admin, recipe["id"])

        # Отправляем сообщение
        attachments = []
        if video_att:
            attachments.append(video_att)
        attachments.append(kb)

        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text=text,
            attachments=attachments,
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )

    @dp.message_callback(F.callback.payload == "pick_gender")
    async def pick_male_female(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text="""Рассчитайте сколько калорий вам нужно потреблять ежедневно для поддержания веса, похудения или набора массы.

Выберите ваш пол:""",
                attachments = [users.pick_gender()]
            )

    @dp.message_callback(F.callback.payload.startswith("gender:"))
    async def pick_male_female(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        gender = event.callback.payload.split(":")[1]
        fsm.append_dict(event.get_ids()[1], "gender", gender)
        fsm.set_state(event.get_ids()[1], "input_age")
        await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text="Введите Ваш возраст:",
                attachments = [users.back_to_r()]
            )

    @dp.message_callback(F.callback.payload.startswith("activity:"))
    async def pick_activity(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        cf = float(event.callback.payload.split(":")[1])
        fsm.append_dict(event.get_ids()[1], "coef", cf)
        await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text="Введите Вашу цель:",
                attachments = [users.pick_goal()]
            )

    @dp.message_callback(F.callback.payload.startswith("goal:"))
    async def pick_goal(event: MessageCallback):
        await event.answer()
        await bot.delete_message(message_id=event.message.body.mid)
        cf = float(event.callback.payload.split(":")[1])
        ddict = fsm.get_dict(event.get_ids()[1])
        imt = ddict['weight'] / ((ddict['height'] / 100) ** 2)
        if ddict["gender"] == "male":
            imb = 88.36 + 13.4 * ddict["weight"] + 4.8 * ddict["height"] - 5.7 * ddict["age"]
        else:
            imb = 447.6 + 9.2 * ddict["weight"] + 3.1 * ddict["height"] - 4.3 * ddict["age"]
        imb *= ddict["coef"]
        imb *= cf
        await bot.send_message(
                chat_id=event.message.recipient.chat_id,
                text=messagess["calories"].format(imt, imb),
                attachments = [users.back_to_r()],
                parse_mode=parse_mode.ParseMode.MARKDOWN
            )
        fsm.set_state(event.get_ids()[1], "default")
        fsm.clear_dict(event.get_ids()[1])

    #===========РОЗЫГРЫШ=====================

    @dp.message_callback(F.callback.payload == "raffle")
    async def raffle_menu(event: MessageCallback):
        await event.answer()
        await bot.delete_message(
            message_id=event.message.body.mid
        )
        raffle = get_last_raffle_post()
        photo_bytes = await download_photo_bytes(raffle['photo'])
        photo = InputMediaBuffer(photo_bytes)
        text = raffle["text"]
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text=messagess["raffle"].format(text),
            attachments=[photo, users.raffle_menu()],
            parse_mode=parse_mode.ParseMode.MARKDOWN
        )

    @dp.message_callback(F.callback.payload == "join_raffle")
    async def join_raffle(event: MessageCallback):
        await event.answer()
        await bot.delete_message(
            message_id=event.message.body.mid
        )

        await bot.send_message(
                    chat_id=event.message.recipient.chat_id,
                    text="Выберите платформу, где покупали наш товар:",
                    attachments=[users.wb_ozon()],
                    parse_mode=parse_mode.ParseMode.MARKDOWN
                )


    @dp.message_callback(F.callback.payload.startswith("platform:"))
    async def platform_picked(event: MessageCallback):
        await event.answer()
        await bot.delete_message(
                message_id=event.message.body.mid
            )
        platform = event.callback.payload.split(":")[1]
        if platform == "wb":
            w = "srid"
        elif platform == "ozon":
            w = "код"
        fsm.set_state(event.get_ids()[1], "input_srid")
        await bot.send_message(
                    chat_id=event.message.recipient.chat_id,
                    text="Введите {} покупки **нашего** товара:".format(w),
                    attachments=[users.instrucntion_srid(platform)],
                    parse_mode=parse_mode.ParseMode.MARKDOWN)


    @dp.message_callback(F.callback.payload.startswith("instruction:"))
    async def instruction_strid(event: MessageCallback):
        await event.answer()
        await bot.delete_message(
                message_id=event.message.body.mid
            )
        platform = event.callback.payload.split(":")[1]
        if platform == "wb":
            instr1 = InputMedia("static/img/instr1.png")
            instr2 = InputMedia("static/img/instr2.png")
            instr3 = InputMedia("static/img/instr3.png")
            instr4 = InputMedia("static/img/instr4.png")
            instr5 = InputMedia("static/img/instr5.png")
            instr6 = InputMedia("static/img/instr6.png")
            await bot.send_message(
                        chat_id=event.message.recipient.chat_id,
                        text=messagess["instruction_strid_wb"],
                        attachments=[instr1, instr2, instr3, instr4, instr5, instr6, users.back4(platform)],
                        parse_mode=parse_mode.ParseMode.MARKDOWN)
        elif platform == "ozon":
            instr1 = InputMedia("static/img/chek1.png")
            instr2 = InputMedia("static/img/chek2.png")
            instr3 = InputMedia("static/img/chek3.png")
            instr4 = InputMedia("static/img/chek4.png")
            instr5 = InputMedia("static/img/chek5.png")
            instr6 = InputMedia("static/img/chek6.png")
            await bot.send_message(
                        chat_id=event.message.recipient.chat_id,
                        text=messagess["instruction_strid_ozon"],
                        attachments=[instr1, instr2, instr3, instr4, instr5, instr6, users.back4(platform)],
                        parse_mode=parse_mode.ParseMode.MARKDOWN)
