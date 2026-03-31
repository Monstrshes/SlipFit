from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types.attachments.buttons import CallbackButton, LinkButton


def admin_menu():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='👤 Пользователи', payload='APanelGetUsers'),
        CallbackButton(text='✉️ Рассылка', payload='APanelGetMessages')
    )

    builder.row(
        CallbackButton(text='🌟 Товары', payload='APanelCatalog'),
        CallbackButton(text='📹 Видео', payload='APanelVideo')
    )

    builder.row(
        CallbackButton(text='🌿 Рецепты', payload='APanelRecipes'),
        CallbackButton(text='🗝 Розыгрыши', payload='Areceips')
    )

    return builder.as_markup()
def back_to_video_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.row(CallbackButton(text="🔙 Назад", payload="video_cat"))
    return builder.as_markup()
def acatalog():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🚩Удалить категорию', payload='ADeletecategory'),
    )

    builder.row(CallbackButton(text='Добавить товар', payload='ANewProduct')
    )
    builder.row(

        CallbackButton(text='🔙 Назад', payload='Admin_Menu')
    )

    return builder.as_markup()




def delcatalog(lst: list, type):
    builder = InlineKeyboardBuilder()

    for i in lst:
        builder.row(
        CallbackButton(text=f'{i}', payload=f'ADel{type}:{i}')
    )
    builder.row(
        CallbackButton(text='🔙 Назад', payload='APanelCatalog')
    )

    return builder.as_markup()

def choice_catalog(lst: list):
    builder = InlineKeyboardBuilder()

    for i in lst:
        builder.row(
        CallbackButton(text=f'{i}', payload=f'AChoiceCat:{i}')
    )
    builder.row(CallbackButton(text='Добавить категорию', payload='ANewCategory'))
    builder.row(
        CallbackButton(text='🔙 Назад', payload='APanelCatalog')
    )

    return builder.as_markup()

def to_menu():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="В меню", payload="Admin_Menu"))

    return builder.as_markup()

def back1():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🔙 Назад', payload='APanelCatalog'))

    return builder.as_markup()
def back2():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🔙 Назад', payload='APanelVideo'))

    return builder.as_markup()
def avideo():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🚩Удалить категорию видео', payload='ADeleteVideoCategory'),
    )
    builder.row(
        CallbackButton(text='Добавить видео', payload='ANewVideo')
    )
    builder.row(
        CallbackButton(text='🔙 Назад', payload='Admin_Menu')
    )

    return builder.as_markup()

def delvideo_catalog(lst: list, type: str):
    builder = InlineKeyboardBuilder()

    for i in lst:
        builder.row(
            CallbackButton(text=f'{i}', payload=f'ADel{type}:{i}')
        )
    builder.row(
        CallbackButton(text='🔙 Назад', payload='APanelVideo')
    )

    return builder.as_markup()

def choice_video_catalog(lst: list):
    builder = InlineKeyboardBuilder()

    for i in lst:
        builder.row(
            CallbackButton(text=f'{i}', payload=f'AChoiceVideoCat:{i}')
        )
    builder.row(CallbackButton(text='Добавить категорию видео', payload='ANewVideoCategory'))
    builder.row(
        CallbackButton(text='🔙 Назад', payload='APanelVideo')
    )

    return builder.as_markup()

def video_navigation_keyboard(category_id: int, current_index: int, total_videos: int):
    builder = InlineKeyboardBuilder()
    buttons = [
        [
            CallbackButton(text="⬅️ Назад", payload=f"video:{category_id}:{current_index}"),
            CallbackButton(text=f"{current_index}/{total_videos}", payload="video:current"),
            CallbackButton(text="Вперёд ➡️", payload=f"video:{category_id}:{current_index}")
        ],
        [CallbackButton(text="Выбрать другую категорию", payload="video_cat")],
        [CallbackButton(text="Назад в меню", payload="Admin_Menu")]
    ]
    for row in buttons:
        builder.row(*row)
    return builder.as_markup()



def back3():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🔙 Назад', payload='APanelRecipes'))

    return builder.as_markup()

def back4():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🔙 Назад', payload='Areceips'))

    return builder.as_markup()
def areceipt():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text='🚩Удалить категорию рецептов', payload='ADeleteRecipeCategory'),
    )
    builder.row(
        CallbackButton(text='Добавить рецепт', payload='ANewRecipe')
    )
    builder.row(
        CallbackButton(text='🔙 Назад', payload='Admin_Menu')
    )

    return builder.as_markup()

def delrecipe_catalog(lst: list, type: str):
    builder = InlineKeyboardBuilder()

    for i in lst:
        builder.row(
            CallbackButton(text=f'{i}', payload=f'ADel{type}:{i}')
        )
    builder.row(
        CallbackButton(text='🔙 Назад', payload='APanelRecipes')
    )

    return builder.as_markup()

def choice_recipe_catalog(lst: list):
    builder = InlineKeyboardBuilder()

    for i in lst:
        builder.row(
            CallbackButton(text=f'{i}', payload=f'AChoiceRecipeCat:{i}')
        )
    builder.row(CallbackButton(text='Добавить категорию рецептов', payload='ANewRecipeCategory'))
    builder.row(
        CallbackButton(text='🔙 Назад', payload='APanelRecipes')
    )

    return builder.as_markup()

def recipe_navigation_keyboard(category_id: int, current_index: int, total_videos: int):
    builder = InlineKeyboardBuilder()
    buttons = [
        [
            CallbackButton(text="⬅️ Назад", payload=f"recipe:{category_id}:{current_index}"),
            CallbackButton(text=f"{current_index}/{total_videos}", payload="recipe:current"),
            CallbackButton(text="Вперёд ➡️", payload=f"recipe:{category_id}:{current_index}")
        ],
        [CallbackButton(text="Выбрать другую категорию", payload="recipe_cat")],
        [CallbackButton(text="Назад в меню", payload="start")]
    ]
    for row in buttons:
        builder.row(*row)
    return builder.as_markup()

def raffle_admin():
    builder = InlineKeyboardBuilder()

    builder.row(CallbackButton(text='Изменить пост розыгрыша', payload='AddRaffle'))
    builder.row(
        CallbackButton(text='🔙 Назад', payload='Admin_Menu')
    )

    return builder.as_markup()

def back_to_recipe_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.row(CallbackButton(text="🔙 Назад", payload="recipe_cat"))
    return builder.as_markup()