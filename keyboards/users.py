import sys
import os

# Получаем абсолютный путь к родительской папке проекта
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types.attachments.buttons import CallbackButton, LinkButton
from database.database import *


def menu():
    """Простая клавиатура с основными кнопками"""
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🌟 Наши товары', payload='catalog_cat'),
        CallbackButton(text='📹 Тренировки', payload='video_cat')
    )

    builder.row(
        CallbackButton(text='🌿 ПП рецепты', payload='recipe_cat'),
        CallbackButton(text='👫 Новости ', payload='news')
    )

    builder.row(
        CallbackButton(text='🔥 Розыгрыш', payload='raffle'),
        CallbackButton(text='ℹ️ Feedback', payload='feedback')
    )

    return builder.as_markup()

def to_menu():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='В меню', payload='start'))

    return builder.as_markup()
def catalog_cat():
    all_cats = get_categories_from_db()
    builder = InlineKeyboardBuilder()
    for cat in range(len(all_cats)):
            builder.row(
                CallbackButton(text=f'{all_cats[cat]}', payload=f'catalog:{all_cats[cat]}:1'))


    builder.row(
        CallbackButton(text='🔙 Назад', payload='start'),
        LinkButton(text='Смотреть на WB', url="https://www.wildberries.ru/brands/311459479-atlix")
        )

    return builder.as_markup()

def catalog(cat, len_catalog, wburl, item=1):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='◀️', payload=f'catalog:{cat}:{item-1}'),
        CallbackButton(text=f'{item}|{len_catalog}'),
        CallbackButton(text='▶️', payload=f'catalog:{cat}:{item+1}'))

    builder.row(
        CallbackButton(text='🔙 Назад', payload='catalog_cat'),
        LinkButton(text='Смотреть на WB', url=wburl)
        )

    return builder.as_markup()

def video_cat():
    all_cats = get_all_video_categories()
    builder = InlineKeyboardBuilder()
    for cat in range(len(all_cats)):
        try:
            builder.row(
                CallbackButton(text=f'{all_cats[cat]}', payload=f'vcatalog:{all_cats[cat]}:1'))

        except Exception:
            builder.row(
                CallbackButton(text=f'{all_cats[cat]}', payload=f'vcatalog:{cat}:1'))

    builder.row(
        CallbackButton(text='🔙 Назад', payload='start')
        )

    return builder.as_markup()

def viseo_catalog(cat, len_catalog, item=1, isadmin=0, video_id=0):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='◀️', payload=f'vcatalog:{cat}:{item-1}'),
        CallbackButton(text=f'{item}|{len_catalog}', payload = "wsjdklasj;"),
        CallbackButton(text='▶️', payload=f'vcatalog:{cat}:{item+1}'))

    builder.row(
        CallbackButton(text='🔙 Назад', payload='video_cat')
        )
    if isadmin:
        builder.row(
                CallbackButton(text="✏️ Название", payload=f"edit_video_name:{video_id}"),
                CallbackButton(text="📝 Описание", payload=f"edit_video_desc:{video_id}")
            )

    return builder.as_markup()

def recipe_cat():
    all_cats = get_all_recipes_categories()
    builder = InlineKeyboardBuilder()
    for cat in range(len(all_cats)):

            builder.row(
                CallbackButton(text=f'{all_cats[cat]}', payload=f'rcatalog:{all_cats[cat]}:1'))

    builder.row(
        CallbackButton(text='Калькулятор калорий', payload='pick_gender'))
    builder.row(
        CallbackButton(text='🔙 Назад', payload='start')
        )

    return builder.as_markup()
def wb_ozon():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🟪WildBerries', payload=f'platform:wb'),
        CallbackButton(text='🟦Ozon', payload=f'platform:ozon'))
    builder.row(
        CallbackButton(text='🔙 Назад', payload='raffle')
        )
    return builder.as_markup()

def recipe_catalog(cat, len_catalog, item=1, isadmin=0, recipe_id=0):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='◀️', payload=f'rcatalog:{cat}:{item-1}'),
        CallbackButton(text=f'{item}|{len_catalog}', payload = "hsjhdal"),
        CallbackButton(text='▶️', payload=f'rcatalog:{cat}:{item+1}'))
    if isadmin:
        builder.row(
                CallbackButton(text="✏️ Название", payload=f"edit_recipe_name:{recipe_id}"),
                CallbackButton(text="📝 Описание", payload=f"edit_recipe_desc:{recipe_id}")
            )
    builder.row(
        CallbackButton(text='🔙 Назад', payload='recipe_cat')
        )

    return builder.as_markup()

def pick_gender():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='♂️Мужской', payload='gender:male'),
        CallbackButton(text='♀️Женский', payload="gender:female"),
    )

    builder.row(
        CallbackButton(text='🔙 Назад', payload='recipe_cat')
        )

    return builder.as_markup()

def back_to_r():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🔙 Назад', payload='recipe_cat')
        )

    return builder.as_markup()

def pick_daily_act():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='Очень низкая', payload='activity:1.2'),
        CallbackButton(text='Низкая', payload='activity:1.375')
        )
    builder.row(
        CallbackButton(text='Средняя', payload='activity:1.55'),
        CallbackButton(text='Высокая', payload='activity:1.725')
        )
    builder.row(
        CallbackButton(text='Очень высокая', payload='activity:1.9'))
    builder.row(
        CallbackButton(text='🔙 Назад', payload='recipe_cat')
        )

    return builder.as_markup()

def pick_goal():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='Похудеть', payload='goal:0.85'))

    builder.row(
        CallbackButton(text='Поддерживать вес', payload='goal:1'))
    builder.row(
        CallbackButton(text='Набрать массу', payload='goal:1.15'))
    builder.row(
        CallbackButton(text='🔙 Назад', payload='recipe_cat')
        )



    return builder.as_markup()

def raffle_menu():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='Участвовать', payload='join_raffle'))

    builder.row(
        CallbackButton(text='🔙 Назад', payload='start')
        )
    return builder.as_markup()

def srid_raffle():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='Ввести srid', payload='input_srid'),
        CallbackButton(text='Инструкция', payload='instruction_strid')
        )

    builder.row(
        CallbackButton(text='🔙 Назад', payload='join_raffle')
        )
    return builder.as_markup()

def back4(platform):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🔙 Назад', payload=f'platform:{platform}')
        )
    return builder.as_markup()

def back5():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🔙 Назад', payload=f'join_raffle')
        )
    return builder.as_markup()

def instrucntion_srid(platform):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='Инструкция', payload=f'instruction:{platform}')
        )
    builder.row(
        CallbackButton(text='🔙 Назад', payload=f'join_raffle')
        )
    return builder.as_markup()
