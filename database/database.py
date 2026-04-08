import sqlite3
import os
from typing import  List, Optional, Dict
from datetime import datetime, timedelta, date
import random

import os
import sqlite3

def create_database_tables():
    """
    Создаёт базу данных database/base.db и таблицы:
    - users (user_id)
    - catalog (name, description, link, photo_url, category)
    - video (name, text, video_url, category)
    - recepts (name, text, video_url, category)
    - everyday_raffles (date, strid_id)

    """
    # Создаём директорию database, если её нет
    os.makedirs("database", exist_ok=True)

    # Подключаемся к базе данных (файл создастся автоматически)
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()


    try:
        # Таблица users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY
            )
        ''')

        # Таблица catalog
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS catalog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                link TEXT,
                photo_url TEXT,
                category TEXT
            )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS raffles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            photo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

        # Таблица video
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS video (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                text TEXT,
                video_url TEXT NOT NULL,
                category TEXT
            )
        ''')

        # Таблица recepts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                text TEXT,
                video_url TEXT,
                category TEXT
            )
        ''')

        # Таблица everyday_raffles
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS everyday_raffles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL UNIQUE,
        user_id TEXT DEFAULT '',
        strid TEXT UNIQUE NOT NULL
    )
''')

        conn.commit()
        print("Все таблицы успешно созданы или уже существуют")

    except sqlite3.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
        conn.rollback()

    finally:
        conn.close()


def create_product(
    description: str,
    link: str,
    photo_url: str,
    category: str
) -> Optional[int]:
    """
    Создаёт новый товар в таблице catalog базы данных.

    Args:
        description (str): Описание товара.
        link (str): Ссылка на товар.
        photo_url (str): URL фото товара.
        category (str): Категория товара.

    Returns:
        Optional[int]: ID добавленной записи или None в случае ошибки.
    """
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()

            insert_query = '''
                INSERT INTO catalog (description, link, photo_url, category)
                VALUES (?, ?, ?, ?)
            '''

            cursor.execute(insert_query, (description, link, photo_url, category))

            product_id = cursor.lastrowid
            conn.commit()

            return product_id

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении товара в базу данных: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None

def create_video(
    name: str,
    text: str,
    video_url: str,
    category: str,
    token: str
) -> Optional[int]:
    """
    Создаёт новую видеозапись в таблице video базы данных.

    Args:
        name (str): Название видео (обязательное поле).
        text (str): Описание/текст к видео.
        video_url (str): URL видео (обязательное поле).
        category (str): Категория видео.

    Returns:
        Optional[int]: ID добавленной записи или None в случае ошибки.
    """
    try:
        if not(video_url):
            video_url = ""
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()

            insert_query = '''
                INSERT INTO video (name, text, video_url, category, token)
                VALUES (?, ?, ?, ?, ?)
            '''

            cursor.execute(insert_query, (name, text, video_url, category, token))
            video_id = cursor.lastrowid
            conn.commit()

            print(f"Видео '{name}' успешно добавлено в категорию '{category}' с ID: {video_id}")
            return video_id

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении видео в базу данных: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None



def create_recipe(
    name: str,
    text: str,
    video_url: str,
    category: str
) -> Optional[int]:
    """
    Создаёт новый рецепт в таблице recepts базы данных.

    Args:
        name (str): Название рецепта (обязательное поле).
        text (str): Текст рецепта.
        video_url (str): URL видеорецепта.
        category (str): Категория рецепта.

    Returns:
        Optional[int]: ID добавленной записи или None в случае ошибки.
    """
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()

            insert_query = '''
                INSERT INTO recepts (name, text, video_url, category)
                VALUES (?, ?, ?, ?)
            '''

            cursor.execute(insert_query, (name, text, video_url, category))
            recipe_id = cursor.lastrowid
            conn.commit()

            print(f"Рецепт '{name}' успешно добавлен в категорию '{category}' с ID: {recipe_id}")
            return recipe_id

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении рецепта в базу данных: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None

def get_monthly_daily_participants() -> set:
    """
    Получает всех уникальных участников ежедневных розыгрышей за текущий месяц.

    Args:
        None

    Returns:
        set: множество уникальных ID участников за текущий месяц
    """
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()

    # Получаем текущий год и месяц
    current_year = datetime.now().year
    current_month = datetime.now().month

    try:
        # SQL-запрос: выбираем записи за текущий месяц и год
        query = """
            SELECT user_id
            FROM everyday_raffles
            WHERE strftime('%Y-%m', date) = ?
        """
        date_filter = f"{current_year:04d}-{current_month:02d}"
        cursor.execute(query, (date_filter,))

        all_participants = set()

        for row in cursor.fetchall():
            user_ids_str = row[0]  # строка вида "123,456,789"

            if user_ids_str:  # проверяем, что строка не пустая
                # разбиваем на ID и преобразуем в числа
                participants_list = [
                    int(uid.strip())
                    for uid in user_ids_str.split(',')
            if uid.strip()  # фильтруем пустые строки
                ]
                # добавляем в множество (автоматически убирает дубликаты)
                all_participants.update(participants_list)

        return all_participants

    except sqlite3.Error:
        return set()
    finally:
        conn.close()

def get_weekly_participants() -> list:
    """
    Получает список ID участников за текущую календарную неделю (понедельник–воскресенье).

    Returns:
        list: список целых чисел (ID пользователей) или пустой список, если участников нет
    """
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()

    try:
        # Получаем начало и конец текущей недели (понедельник и воскресенье)
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())  # понедельник
        end_of_week = start_of_week + timedelta(days=6)  # воскресенье

        start_date = start_of_week.strftime('%Y-%m-%d')
        end_date = end_of_week.strftime('%Y-%m-%d')

        # Запрос: выбираем все записи за текущую неделю
        cursor.execute(
            "SELECT user_id FROM everyday_raffles WHERE date BETWEEN ? AND ?",
            (start_date, end_date)
        )
        results = cursor.fetchall()

        all_participants = set()  # используем set для автоматической уникализации ID

        for row in results:
            if row[0]:  # проверяем, что поле user_id не пустое
                participants = [
                    int(uid.strip())
                    for uid in row[0].split(',')
                    if uid.strip()
                ]
                all_participants.update(participants)

        return list(all_participants)  # возвращаем список уникальных ID

    except sqlite3.Error as e:
        print(f"Ошибка при получении участников за неделю: {e}")
        return []
    except ValueError as e:
        print(f"Ошибка преобразования ID в число: {e}")
        return []
    finally:
        conn.close()

def get_weekky_winner():
    participants = get_weekly_participants()
    if participants:
        winner = random.choice(participants)
        return winner
    else:
        return None

def check_strid_exists(strid: str) -> bool:
    """
    Проверяет, существует ли указанный STRID в таблице everyday_raffles.

    Args:
        strid (str): STRID для проверки

    Returns:
        bool: True, если STRID найден в таблице, False — если не найден или произошла ошибка
    """
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT 1 FROM everyday_raffles WHERE strid = ?",
            (strid,)
        )
        result = cursor.fetchone()
        return result is not None

    except sqlite3.Error as e:
        print(f"Ошибка при проверке STRID: {e}")
        return False
    finally:
        conn.close()

def get_monthly_participants() -> list:
    """
    Получает список ID участников за текущий календарный месяц (с 1‑го числа до последнего дня месяца).

    Returns:
        list: список целых чисел (ID пользователей) или пустой список, если участников нет
    """
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()

    try:
        # Получаем начало и конец текущего месяца
        today = date.today()
        start_of_month = today.replace(day=1)  # 1‑е число текущего месяца

        # Вычисляем последний день месяца: берём 1‑е число следующего месяца и отнимаем 1 день
        if today.month == 12:
            end_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            end_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

        start_date = start_of_month.strftime('%Y-%m-%d')
        end_date = end_of_month.strftime('%Y-%m-%d')

        # Запрос: выбираем все записи за текущий месяц
        cursor.execute(
            "SELECT user_id FROM everyday_raffles WHERE date BETWEEN ? AND ?",
            (start_date, end_date)
        )
        results = cursor.fetchall()

        all_participants = set()  # используем set для автоматической уникализации ID

        for row in results:
            if row[0]:  # проверяем, что поле user_id не пустое
                participants = [
                    int(uid.strip())
                    for uid in row[0].split(',')
            if uid.strip()
                ]
                all_participants.update(participants)

        return list(all_participants)  # возвращаем список уникальных ID

    except sqlite3.Error as e:
        print(f"Ошибка при получении участников за месяц: {e}")
        return []
    except ValueError as e:
        print(f"Ошибка преобразования ID в число: {e}")
        return []
    finally:
        conn.close()


def get_monthly_winner() -> int | None:
    """
    Выбирает случайного победителя из участников текущего месяца.

    Returns:
        int | None: ID победителя или None, если участников нет
    """
    participants = get_monthly_participants()
    if participants:
        winner = random.choice(participants)
        return winner
    else:
        return None

def add_user_to_monthly_raffle(user_id: int, current_date, strid) -> bool:
    """
    Добавляет пользователя в розыгрыш, если он ещё не участвовал в текущем месяце.

    Args:
        user_id: ID пользователя
        current_date: объект datetime.date (дата регистрации)
        strid: STRID пользователя

    Returns:
        bool: True если пользователь добавлен или уже был зарегистрирован в этом месяце,
              False при ошибке БД.
    """
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()
    try:
        # Преобразуем date в строку формата YYYY-MM-DD и выделяем год-месяц
        date_str = current_date.isoformat()           # '2025-03-08'
        year_month = current_date.strftime("%Y-%m")   # '2025-03'



        # Добавляем новую запись
        cursor.execute(
            "INSERT INTO everyday_raffles (date, user_id, strid) VALUES (?, ?, ?)",
            (date_str, user_id, strid)
        )
        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"Ошибка БД при добавлении в розыгрыш: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_last_raffle_post(db_path: str = "database/base.db") -> Optional[Dict]:
    """
    Возвращает последний пост из таблицы raffles в виде словаря,
    или None, если таблица пуста.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row  # чтобы обращаться по именам столбцов
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, text, photo, created_at
                FROM raffles
                ORDER BY created_at DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                return dict(row)  # преобразуем в обычный dict
            return None
    except sqlite3.Error as e:
        print(f"Ошибка при получении последнего поста: {e}")
        return None

def add_new_raffle(text: str, photo: str | None = None) -> int | None:
    """
    Добавляет новый розыгрыш в таблицу raffles.

    Args:
        text (str): обязательный текст описания розыгрыша
        photo (str | None, optional): путь к фото или URL изображения (может быть None)

    Returns:
        int | None: ID созданного розыгрыша или None при ошибке
    """
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()

    try:
        # Выполняем вставку новой записи в таблицу raffles
        cursor.execute(
            "INSERT INTO raffles (text, photo) VALUES (?, ?)",
            (text, photo)
        )

        # Получаем ID последней вставленной записи
        raffle_id = cursor.lastrowid

        # Сохраняем изменения в базе данных
        conn.commit()

        return raffle_id

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении нового розыгрыша: {e}")
        return None
    finally:
        conn.close()

def get_products_by_category(category: str) -> List[Dict]:
    """
    Получает все товары заданной категории из базы данных.

    Args:
        category (str): Название категории.

    Returns:
        List[Dict]: Список товаров в категории (может быть пустым).
    """
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            query = '''
                SELECT id, description, link, photo_url
                FROM catalog
                WHERE category = ?
                ORDER BY id ASC
            '''
            cursor.execute(query, (category,))
            rows = cursor.fetchall()

            products = [
                {
                    'id': row[0],
                    'description': row[1],
            'link': row[2],
            'photo_url': row[3]
                }
                for row in rows
            ]
            return products
    except sqlite3.Error as e:
        print(f"Ошибка получения товаров категории '{category}': {e}")
        return []

def get_product_by_index(category: str, index: int) -> Optional[Dict]:
    """
    Получает товар по индексу в категории.

    Args:
        category (str): Название категории.
        index (int): Индекс товара (0-based).

    Returns:
        Optional[Dict]: Товар по индексу или None, если индекс вне диапазона.
    """
    products = get_products_by_category(category)
    if 0 <= index < len(products):
        return products[index]
    return None
def get_categories_from_db() -> List[str]:
    """
    Получает список уникальных категорий товаров из таблицы catalog базы данных.

    Returns:
        List[str]: Отсортированный список названий категорий (пустой список при ошибке или отсутствии данных).
    """
    try:
        with sqlite3.connect('database/base.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # SQL‑запрос для получения уникальных категорий из таблицы catalog
            query = """
                SELECT DISTINCT category
                FROM catalog
                WHERE category IS NOT NULL AND category != ''
                ORDER BY category ASC
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Извлекаем названия категорий из результатов запроса
            categories = [row['category'] for row in rows]

            return categories

    except sqlite3.Error as e:
        return []
    except Exception as e:
        return []

def delete_category_from_db(category_name: str) -> bool:
    """
    Удаляет категорию и все связанные с ней товары из таблицы catalog.

    Args:
        category_name (str): Название категории для удаления.

    Returns:
        bool: True при успешном удалении, False при ошибке.
    """
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            # Удаляем все товары данной категории
            cursor.execute(
                "DELETE FROM catalog WHERE category = ?",
                (category_name,)
            )
            conn.commit()
            print(f"Категория '{category_name}' и все связанные товары успешно удалены")
            return True

    except sqlite3.Error as e:
        print(f"Ошибка при удалении категории '{category_name}': {e}")
        return False

def get_all_video_categories() -> List[str]:
    """Получает все уникальные категории из таблицы video"""
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM video WHERE category IS NOT NULL AND category != ''")
            categories = [row[0] for row in cursor.fetchall()]
            return sorted(categories)  # Сортируем для удобства
    except Exception as e:
        print(f"Ошибка получения категорий: {e}")
        return []

def create_video(name: str, text: str, category: str, token: str = "", video_url :str = "") -> bool:
    """Добавляет новое видео в БД (может создать новую категорию)"""
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO video (name, text, video_url, category, token) VALUES (?, ?, ?, ?, ?)",
                (name, text, video_url, category, token or None)
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка добавления видео: {e}")
        return False



def delete_videos_by_category(category: str) -> bool:
    """Удаляет все видео в указанной категории"""
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM video WHERE category = ?", (category,))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Ошибка удаления видео категории: {e}")
        return False

def get_videos_by_category(category: str) -> List[Dict]:
    """Получает видео по категории"""
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, text, video_url, category, token FROM video WHERE category = ? ORDER BY id",
                (category,)
            )
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка получения видео категории: {e}")
        return []

def get_video_in_category(category: str, n: int) -> Optional[Dict]:
    """
    Получает n‑ное видео в указанной категории (нумерация с 1)
    Возвращает: видео как словарь или None, если не найдено
    """
    try:
         with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, text, video_url, category, token FROM video "
                "WHERE category = ? ORDER BY id LIMIT 1 OFFSET ?",
                (category, n - 1)  # OFFSET n-1 для нумерации с 1
            )
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    except Exception as e:
            print(f"Ошибка получения {n}-го видео категории '{category}': {e}")
            return None

def get_total_videos_in_category(category: str) -> int:
    """Получает общее количество видео в категории"""
    try:
         with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM video WHERE category = ?", (category,))
            return cursor.fetchone()[0]
    except Exception as e:
        print(f"Ошибка подсчёта видео в категории '{category}': {e}")
        return 0





#!!
def get_all_recipes_categories() -> List[str]:
    """Получает все уникальные категории из таблицы recepts"""
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM recepts WHERE category IS NOT NULL AND category != ''")
            categories = [row[0] for row in cursor.fetchall()]
            return sorted(categories)  # Сортируем для удобства
    except Exception as e:
        print(f"Ошибка получения категорий: {e}")
        return []

def create_recipe(name: str, text: str, video_url: str, category: str) -> bool:
    """Добавляет новый рецепт в БД (может создать новую категорию)"""
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO recepts (name, text, video_url, category) VALUES (?, ?, ?, ?)",
                (name, text, video_url, category or None)
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка добавления рецепта: {e}")
        return False

def delete_recipes_by_category(category: str) -> bool:
    """Удаляет все рецепты в указанной категории"""
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recepts WHERE category = ?", (category,))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Ошибка удаления рецептов категории: {e}")
        return False

def get_recipes_by_category(category: str) -> List[Dict]:
    """Получает рецепты по категории"""
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, text, video_url, category FROM recepts WHERE category = ? ORDER BY id",
                (category,)
            )
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка получения рецептов категории: {e}")
        return []

def get_recipe_in_category(category: str, n: int) -> Optional[Dict]:
    """
    Получает n‑ное блюдо в указанной категории (нумерация с 1)
    Возвращает: рецепт как словарь или None, если не найдено
    """
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, text, video_url, category FROM recepts "
                "WHERE category = ? ORDER BY id LIMIT 1 OFFSET ?",
                (category, n - 1)  # OFFSET n-1 для нумерации с 1
            )
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    except Exception as e:
        print(f"Ошибка получения {n}-го рецепта категории '{category}': {e}")
        return None

def get_total_recepe_in_category(category: str) -> int:
    """Получает общее количество рецептов в категории"""
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM recepts WHERE category = ?", (category,))
            return cursor.fetchone()[0]
    except Exception as e:
        print(f"Ошибка подсчёта рецептов в категории '{category}': {e}")
        return 0

def add_user_to_db(user_id: int) -> bool:
    """
    Добавляет пользователя в таблицу users.

    Args:
        user_id (int): ID пользователя Telegram.

    Returns:
        bool: True при успехе, False при ошибке.
    """
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
                (user_id,)
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка добавления пользователя {user_id} в БД: {e}")
        return False
def get_all_users() -> list[int] | None:
    """
    Получает все user_id из таблицы users.

    Returns:
        list[int]: Список user_id или None при ошибке.
    """
    try:
        with sqlite3.connect('database/base.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users")
            users = [row[0] for row in cursor.fetchall()]
            return users
    except Exception as e:
        print(f"Ошибка получения пользователей: {e}")
        return None

def update_video_name(video_id: int, new_name: str) -> bool:
    conn = sqlite3.connect('database/base.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE video SET name = ? WHERE id = ?", (new_name, video_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()

def update_video_desc(video_id: int, new_desc: str | None) -> bool:
    conn = sqlite3.connect('database/base.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE video SET text = ? WHERE id = ?", (new_desc, video_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()

def update_recipe_name(recipe_id: int, new_name: str) -> bool:
    conn = sqlite3.connect('database/base.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE recepts SET name = ? WHERE id = ?", (new_name, recipe_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()

def update_recipe_desc(recipe_id: int, new_desc: str | None) -> bool:
    conn = sqlite3.connect('database/base.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE recepts SET text = ? WHERE id = ?", (new_desc, recipe_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()


#!!
def get_video_item_position(video_id: int) -> tuple[int | None, str | None]:
    """
    Возвращает порядковый номер видео в его категории (начиная с 1) и название категории.
    Если видео не найдено или ошибка, возвращает (None, None).
    """

    if not isinstance(video_id, int):
        video_id = int(video_id)
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()
    try:
        # Получаем категорию видео
        cursor.execute("SELECT category FROM video WHERE id = ?", (video_id,))
        row = cursor.fetchone()
        if not row:
            return None, None
        category = row[0]

        # Получаем все ID видео в этой категории, отсортированные по id
        cursor.execute("SELECT id FROM video WHERE category = ? ORDER BY id", (category,))
        rows = cursor.fetchall()
        video_ids = [r[0] for r in rows]

        # Ищем позицию
        if video_id in video_ids:
            return video_ids.index(video_id) + 1, category
        return None, None
    except sqlite3.Error as e:
        print(f"Ошибка получения позиции видео: {e}")
        return None, None
    finally:
        conn.close()

def get_recipe_item_position(recipe_id: int) -> tuple[int | None, str | None]:
    """
    Возвращает порядковый номер рецепта в его категории (начиная с 1) и название категории.
    Если рецепт не найдено или ошибка, возвращает (None, None).
    """
    if not isinstance(recipe_id, int):
        recipe_id = int(recipe_id)
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()
    try:
        # Получаем категорию рецепта
        cursor.execute("SELECT category FROM recepts WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()
        if not row:
            return None, None
        category = row[0]

        # Получаем все ID рецептов в этой категории, отсортированные по id
        cursor.execute("SELECT id FROM recepts WHERE category = ? ORDER BY id", (category,))
        rows = cursor.fetchall()
        recipe_ids = [r[0] for r in rows]

        # Ищем позицию
        if recipe_id in recipe_ids:
            return recipe_ids.index(recipe_id) + 1, category
        return None, None
    except sqlite3.Error as e:
        print(f"Ошибка получения позиции рецепта: {e}")
        return None, None
    finally:
        conn.close()

def delete_recipe(recipe_id: int) -> bool:
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM recepts WHERE id = ?", (recipe_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Ошибка удаления рецепта {recipe_id}: {e}")
        return False
    finally:
        conn.close()

def delete_video(video_id: int) -> bool:
    """
    Удаляет видео из таблицы video по его ID.
    Возвращает True, если удаление успешно, иначе False.
    """
    conn = sqlite3.connect("database/base.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM video WHERE id = ?", (video_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Ошибка удаления видео {video_id}: {e}")
        return False
    finally:
        conn.close()
