import sys
import os

# Получаем абсолютный путь к родительской папке проекта
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from maxapi.types import MessageCreated
from maxapi.enums import parse_mode
from dict.messages import messagess
from keyboards import users, adminskb
from loggs import setup_logging
from config import Config
from fsm.admin import UFSM, AFSM
from datetime import datetime
from more_func.downphoto import save_video_to_disk


from database.database import *

fsm = UFSM()
afsm = AFSM()
admins = Config().admins




def register_handlers(dp, bot):
    @dp.message_created()
    async def text_message(event: MessageCreated):
                if fsm.get_state(event.get_ids()[1]) != "default":
                    state = fsm.get_state(event.get_ids()[1])
                    if state == "input_age":
                        try:
                            age = int(event.message.body.text)
                            if 5 <= age <= 100:
                                await bot.delete_message(message_id=event.message.body.mid)
                                await bot.send_message(
                                        chat_id=event.message.recipient.chat_id,
                                        text="Введите Ваш рост в см:",
                                        attachments = [users.back_to_r()]
                                    )
                                fsm.append_dict(event.get_ids()[1], "age", age)
                                fsm.set_state(event.get_ids()[1], "input_height")
                            else:
                                await bot.delete_message(message_id=event.message.body.mid)
                                fsm.clear_dict(event.get_ids()[1])
                                fsm.set_state(event.get_ids()[1], "default")
                                await bot.send_message(
                                        chat_id=event.message.recipient.chat_id,
                                        text="Неккоректный возраст\n\nВозраст должен быть в пределах [5; 100]",
                                        attachments = [users.back_to_r()]
                                    )
                        except Exception as e:
                            await bot.delete_message(message_id=event.message.body.mid)
                            fsm.clear_dict(event.get_ids()[1])
                            fsm.set_state(event.get_ids()[1], "default")
                            await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Возраст должен быть целым числом!!!",
                                    attachments = [users.back_to_r()]
                                )
                    elif state == "input_weight":
                        try:
                            weight = int(event.message.body.text)
                            if 30 <= weight <= 300:
                                await bot.delete_message(message_id=event.message.body.mid)
                                fsm.append_dict(event.get_ids()[1], "weight", weight)
                                await bot.send_message(
                                        chat_id=event.message.recipient.chat_id,
                                        text=messagess["daily_activity"],
                                        attachments = [users.pick_daily_act()]
                                    )
                            else:
                                await bot.delete_message(message_id=event.message.body.mid)
                                fsm.clear_dict(event.get_ids()[1])
                                fsm.set_state(event.get_ids()[1], "default")
                                await bot.send_message(
                                        chat_id=event.message.recipient.chat_id,
                                        text="Неккоректный вес\n\nВес должен быть в пределах [30; 300]",
                                        attachments = [users.back_to_r()]
                                    )
                        except:
                            await bot.delete_message(message_id=event.message.body.mid)
                            fsm.clear_dict(event.get_ids()[1])
                            fsm.set_state(event.get_ids()[1], "default")
                            await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Вес должен быть числом!!!",
                                    attachments = [users.pick_gender()]
                                )

#!!!
                    elif state == "input_srid":
                        try:
                            srid = (event.message.body.text)
                            if len(srid) > 10:
                                strid = event.message.body.text
                                if not(check_strid_exists(strid)):
                                    current_date = datetime.now().date()
                                    add_user_to_monthly_raffle(event.get_ids()[1], current_date, strid)
                                    await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Вы успешно зарегистрировались в розыгрыше! Мы оповестим Вас о результате!",
                                    attachments = [users.to_menu()]
                                )
                                    fsm.set_state(event.get_ids()[1], "default")
                                else:
                                    await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Данный код уже использовался для участия в розыгрыше! Повторное использование запрещено!",
                                    attachments = [users.back5()]
                                )

                            else:
                                await bot.delete_message(message_id=event.message.body.mid)
                                fsm.clear_dict(event.get_ids()[1])
                                fsm.set_state(event.get_ids()[1], "default")
                                await bot.send_message(
                                        chat_id=event.message.recipient.chat_id,
                                        text="Некорректный srid/чек",
                                        attachments = [users.back5()]
                                    )
                        except Exception as e:
                            await bot.delete_message(message_id=event.message.body.mid)
                            fsm.clear_dict(event.get_ids()[1])
                            fsm.set_state(event.get_ids()[1], "default")
                            await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text=f"Ошибка {e}!!!",
                                    attachments = [users.to_menu()]
                                )

                    elif state == "input_height":
                        try:
                            height = int(event.message.body.text)
                            if 130 <= height <= 210:
                                await bot.delete_message(message_id=event.message.body.mid)
                                fsm.append_dict(event.get_ids()[1], "height", height)
                                fsm.set_state(event.get_ids()[1], "input_weight")
                                await bot.send_message(
                                        chat_id=event.message.recipient.chat_id,
                                        text="Введите Ваш вес:",
                                        attachments = [users.back_to_r()]
                                    )
                            else:
                                await bot.delete_message(message_id=event.message.body.mid)
                                fsm.clear_dict(event.get_ids()[1])
                                fsm.set_state(event.get_ids()[1], "default")
                                await bot.send_message(
                                        chat_id=event.message.recipient.chat_id,
                                        text="Неккоректный рост\n\nРост должен быть в пределах [130; 210]",
                                        attachments = [users.back_to_r()]
                                    )
                        except Exception as e:
                            print(e)
                            await bot.delete_message(message_id=event.message.body.mid)
                            fsm.clear_dict(event.get_ids()[1])
                            fsm.set_state(event.get_ids()[1], "default")
                            await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Рост должен быть числом!!!",
                                    attachments = [users.pick_gender()]
                                )

                if event.get_ids()[1] in admins and afsm.get_state(event.get_ids()[1]) != "default":
                        state = afsm.get_state(event.get_ids()[1])
                        if state == "add_category":
                            category_name = event.message.body.text.strip()

                            try:
                                    all_categories = get_categories_from_db()
                                    if category_name not in all_categories:
                                        afsm.append_dict(event.get_ids()[1], "category", category_name)
                                        afsm.set_state(event.get_ids()[1], "add_product_text")

                                        await bot.send_message(
                                        chat_id=event.message.recipient.chat_id,
                                text="Введите описание товара:",
                                attachments=[adminskb.back1()],
                                parse_mode=parse_mode.ParseMode.MARKDOWN
                            )
                            except:
                                    await bot.send_message(
                                chat_id=event.message.recipient.chat_id,
                                text="Категория с таким названием уже существует",
                        attachments=[adminskb.back1()],
                        parse_mode=parse_mode.ParseMode.MARKDOWN
                    )
                        elif state == "add_product_text":
                            product_text = event.message.body.text
                            if len(product_text) <= 10:
                                product_text = ""
                            afsm.append_dict(event.get_ids()[1], "product_text", product_text)
                            afsm.set_state(event.get_ids()[1], "add_product_link")
                            await bot.send_message(
                        chat_id=event.message.recipient.chat_id,
                        text="Введите ссылку на товар:",
                        attachments=[adminskb.back1()],
                        parse_mode=parse_mode.ParseMode.MARKDOWN
                    )
                        # ========== ОБРАБОТКА ТЕКСТОВЫХ СОСТОЯНИЙ ==========
                        if state == "add_product_link":
                            link = event.message.body.text
                            if len(link) > 4 and link.startswith("https"):
                                afsm.append_dict(event.get_ids()[1], "product_link", link)
                                afsm.set_state(event.get_ids()[1], "add_product_photo")
                                await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Отправьте фото товара:",
                                    attachments=[adminskb.back1()],
                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                )
                            else:
                                await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Ссылка должна начинаться с https и быть длиннее 4 символов",
                                    attachments=[adminskb.back1()],
                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                )

                        elif state == "add_video_category":
                            category_name = event.message.body.text.strip()
                            all_categories = get_all_video_categories()
                            if 4 < len(category_name) < 50 and category_name not in all_categories:
                                afsm.append_dict(event.get_ids()[1], "video_category", category_name)
                                afsm.set_state(event.get_ids()[1], "add_video_title")
                                await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Введите название видео:",
                                    attachments=[adminskb.back2()],
                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                )
                            else:
                                await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Название категории должно быть от 4 до 50 символов",
                                    attachments=[adminskb.back2()],
                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                )

                        elif state == "add_video_title":
                            title = event.message.body.text.strip()
                            if 4 < len(title) < 100:
                                afsm.append_dict(event.get_ids()[1], "video_name", title)
                                afsm.set_state(event.get_ids()[1], "add_video_description")
                                await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Введите описание видео:",
                                    attachments=[adminskb.back2()],
                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                )
                            else:
                                await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Название должно быть от 4 до 100 символов",
                                    attachments=[adminskb.back2()],
                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                )

                        elif state == "add_video_description":
                            description = event.message.body.text.strip()
                            afsm.append_dict(event.get_ids()[1], "video_text", description)
                            afsm.set_state(event.get_ids()[1], "add_video")
                            await bot.send_message(
                                chat_id=event.message.recipient.chat_id,
                                text="Отправьте видео, которое хотите добавить:",
                                attachments=[adminskb.back2()],
                                parse_mode=parse_mode.ParseMode.MARKDOWN
                            )

                        elif state == "enter_text_message":
                            description = event.message.body.text.strip()
                            afsm.append_dict(event.get_ids()[1], "text_message", description)
                            afsm.set_state(event.get_ids()[1], "add_photo_messages")
                            await bot.send_message(
                                chat_id=event.message.recipient.chat_id,
                                text="Отправьте фото, которое хотите добавить в рассылку:",
                                attachments=[adminskb.to_menu()],
                                parse_mode=parse_mode.ParseMode.MARKDOWN
                            )





                        #!!

                        elif state == "add_recipe_category":
                            category_name = event.message.body.text.strip()
                            all_categories = get_all_recipes_categories()
                            if 4 < len(category_name) < 50 and category_name not in all_categories:
                                afsm.append_dict(event.get_ids()[1], "recipe_category", category_name)
                                afsm.set_state(event.get_ids()[1], "add_recipe_title")
                                await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Введите название рецепта:",
                                    attachments=[adminskb.back3()],
                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                )
                            else:
                                await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Название категории должно быть от 4 до 50 символов",
                                    attachments=[adminskb.back3()],
                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                )

                        elif state == "add_recipe_title":
                            title = event.message.body.text.strip()
                            if 4 < len(title) < 100:
                                afsm.append_dict(event.get_ids()[1], "recipe_name", title)
                                afsm.set_state(event.get_ids()[1], "add_recipe_description")
                                await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Введите описание рецепта:",
                                    attachments=[adminskb.back3()],
                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                )
                            else:
                                await bot.send_message(
                                    chat_id=event.message.recipient.chat_id,
                                    text="Название должно быть от 4 до 100 символов",
                                    attachments=[adminskb.back3()],
                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                )

                        elif state == "add_recipe_description":
                            description = event.message.body.text.strip()
                            afsm.append_dict(event.get_ids()[1], "recipe_text", description)
                            afsm.set_state(event.get_ids()[1], "add_recipe_video")
                            await bot.send_message(
                                chat_id=event.message.recipient.chat_id,
                                text="Отправьте видео, которое хотите добавить для рецепта:",
                                attachments=[adminskb.back3()],
                                parse_mode=parse_mode.ParseMode.MARKDOWN
                            )

                        elif state == "add_raffle_text":
                            text = event.message.body.text.strip()
                            afsm.append_dict(event.get_ids()[1], "raffle_text", text)
                            afsm.set_state(event.get_ids()[1], "add_raffle_photo")
                            await bot.send_message(
                                chat_id=event.message.recipient.chat_id,
                                text="Отправьте фото, которое хотите добавить для розыгрыша:",
                                attachments=[adminskb.back4()],
                                parse_mode=parse_mode.ParseMode.MARKDOWN
                            )
                        # ========== ОБРАБОТКА СОСТОЯНИЙ С МЕДИАФАЙЛАМИ ==========
                        elif event.message.body.attachments:

                            # Состояние для добавления ВИДЕО
                            if state == "add_video":
                                for attachment in event.message.body.attachments:
                                    if attachment.type.lower() == "video":
                                        video_url =  attachment.payload.url
                                        token = attachment.payload.token
                                        # path = await save_video_to_disk(video_url)
                                        # afsm.append_dict(event.get_ids()[1], "video", path )
                                        afsm.append_dict(event.get_ids()[1], "token", token )
                                        # Получаем все данные
                                        ddict = afsm.get_dict(event.get_ids()[1])

                                        # Проверяем наличие всех ключей
                                        if all(k in ddict for k in ["video_category", "video_name", "video_text", "token"]):
                                            create_video(
                                                name=ddict["video_name"],
                                                text=ddict["video_text"],
                                                token=ddict["token"],
                                                category=ddict["video_category"]
                                            )

                                            await bot.send_message(
                                                chat_id=event.message.recipient.chat_id,
                                                text="✅ Видео успешно добавлено",
                                                attachments=[adminskb.to_menu()],
                                                parse_mode=parse_mode.ParseMode.MARKDOWN
                                            )

                                            # Очищаем данные
                                            afsm.clear_dict(event.get_ids()[1])
                                            afsm.set_state(event.get_ids()[1], "default")
                                        else:
                                            await bot.send_message(
                                                chat_id=event.message.recipient.chat_id,
                                                text="❌ Ошибка: не все данные видео заполнены",
                                                attachments=[adminskb.back2()],
                                                parse_mode=parse_mode.ParseMode.MARKDOWN
                                            )
                                        break  # Выходим после обработки первого видео

                            # Состояние для добавления ФОТО товара
                            elif state == "add_product_photo":
                                for attachment in event.message.body.attachments:
                                    if attachment.type.lower() == "image":
                                        photo_url = attachment.payload.url
                                        afsm.append_dict(event.get_ids()[1], "product_photo", photo_url)

                                        # Получаем все данные
                                        ddict = afsm.get_dict(event.get_ids()[1])

                                        # Проверяем наличие всех ключей
                                        if all(k in ddict for k in ["product_link", "product_photo", "category"]):
                                            # Сохраняем товар в БД
                                            success = create_product(
                                                description=ddict["product_text"], # Если нужно отдельное описание - создайте отдельное поле
                                                link=ddict["product_link"],
                                                photo_url=ddict["product_photo"],
                                                category=ddict["category"]
                                            )

                                            if success:
                                                await bot.send_message(
                                                    chat_id=event.message.recipient.chat_id,
                                                    text="✅ Товар успешно добавлен",
                                                    attachments=[adminskb.to_menu()],
                                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                                )
                                            else:
                                                await bot.send_message(
                                                    chat_id=event.message.recipient.chat_id,
                                                    text="❌ Ошибка при добавлении товара",
                                                    attachments=[adminskb.back1()],
                                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                                )

                                            # Очищаем данные в любом случае
                                            afsm.clear_dict(event.get_ids()[1])
                                            afsm.set_state(event.get_ids()[1], "default")
                                        else:
                                            await bot.send_message(
                                                chat_id=event.message.recipient.chat_id,
                                                text="❌ Ошибка: не все данные товара заполнены",
                                                attachments=[adminskb.back1()],
                                                parse_mode=parse_mode.ParseMode.MARKDOWN
                                            )
                                        break  # Выходим после обработки первого фото
                            elif state == "add_recipe_video":
                                for attachment in event.message.body.attachments:
                                    if attachment.type.lower() == "video":
                                        video_url =  attachment.payload.url
                                        token = attachment.payload.token
                                        # path = await save_video_to_disk(video_url)
                                        # afsm.append_dict(event.get_ids()[1], "video", path )
                                        afsm.append_dict(event.get_ids()[1], "video_url", token )
                                        # Получаем все данные
                                        ddict = afsm.get_dict(event.get_ids()[1])

                                        # Проверяем наличие всех ключей
                                        if all(k in ddict for k in ["recipe_name", "recipe_text", "recipe_category", "video_url"]):
                                            create_recipe(
                                                name=ddict["recipe_name"],
                                                text=ddict["recipe_text"],
                                                video_url=ddict["video_url"],
                                                category=ddict["recipe_category"]
                                            )

                                            await bot.send_message(
                                                chat_id=event.message.recipient.chat_id,
                                                text="✅ Рецепт успешно добавлен",
                                                attachments=[adminskb.to_menu()],
                                                parse_mode=parse_mode.ParseMode.MARKDOWN
                                            )

                                            # Очищаем данные
                                            afsm.clear_dict(event.get_ids()[1])
                                            afsm.set_state(event.get_ids()[1], "default")
                                        else:
                                            await bot.send_message(
                                                chat_id=event.message.recipient.chat_id,
                                                text="❌ Ошибка: не все данные видео заполнены",
                                                attachments=[adminskb.back3()],
                                                parse_mode=parse_mode.ParseMode.MARKDOWN
                                            )
                                        break  # Выходим после обработки первого видео
                            elif state == "add_photo_messages":
                                for attachment in event.message.body.attachments:
                                    if attachment.type.lower() == "image":
                                        photo_url = attachment.payload.url
                                        afsm.append_dict(event.get_ids()[1], "photo_message", photo_url)

                                        # Получаем все данные
                                        ddict = afsm.get_dict(event.get_ids()[1])

                                        # Проверяем наличие всех ключей
                                        if all(k in ddict for k in ["photo_message", "text_message"]):
                                            # Сохраняем товар в БД
                                            all_users = get_all_users()
                                            c = 0
                                            for user_id in all_users:
                                                try:
                                                    await bot.send_message(
                                                chat_id=user_id,
                                                text=ddict["text_message"],
                                                attachments=[ddict["photo_message"], users.menu()],
                                                parse_mode=parse_mode.ParseMode.MARKDOWN
                                            )
                                                    c += 1
                                                except:
                                                    continue


                                            # Очищаем данные в любом случае
                                            afsm.clear_dict(event.get_ids()[1])
                                            afsm.set_state(event.get_ids()[1], "default")
                                            await bot.send_message(
                                                chat_id=event.message.recipient.chat_id,
                                                text=f"Ваше сообщение было разослано {c} пользователям.",
                                                attachments=[adminskb.to_menu()],
                                                parse_mode=parse_mode.ParseMode.MARKDOWN
                                            )
                                        break  # Выходим после обработки первого фото
                            elif state == "add_raffle_photo":
                                for attachment in event.message.body.attachments:
                                    if attachment.type.lower() == "image":
                                        photo_url = attachment.payload.url
                                        afsm.append_dict(event.get_ids()[1], "raffle_photo", photo_url)

                                        # Получаем все данные
                                        ddict = afsm.get_dict(event.get_ids()[1])

                                        # Проверяем наличие всех ключей
                                        if all(k in ddict for k in ["raffle_photo", "raffle_text"]):
                                            # Сохраняем товар в БД
                                            success = add_new_raffle(
                                                text=ddict["raffle_text"], # Если нужно отдельное описание - создайте отдельное поле
                                                photo=ddict["raffle_photo"]
                                            )

                                            if success:
                                                await bot.send_message(
                                                    chat_id=event.message.recipient.chat_id,
                                                    text="✅ Информация о розыгрыше успешно изменена",
                                                    attachments=[adminskb.to_menu()],
                                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                                )
                                            else:
                                                await bot.send_message(
                                                    chat_id=event.message.recipient.chat_id,
                                                    text="❌ Ошибка при изменении информации о розыгрыше",
                                                    attachments=[adminskb.back4()],
                                                    parse_mode=parse_mode.ParseMode.MARKDOWN
                                                )

                                            # Очищаем данные в любом случае
                                            afsm.clear_dict(event.get_ids()[1])
                                            afsm.set_state(event.get_ids()[1], "default")
                                        else:
                                            await bot.send_message(
                                                chat_id=event.message.recipient.chat_id,
                                                text="❌ Ошибка: не все данные  заполнены",
                                                attachments=[adminskb.back4()],
                                                parse_mode=parse_mode.ParseMode.MARKDOWN
                                            )
                                        break  # Выходим после обработки первого фото
