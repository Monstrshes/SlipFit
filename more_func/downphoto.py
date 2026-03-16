import aiohttp
import uuid
from pathlib import Path
import aiofiles

async def download_photo_bytes(photo_url: str) -> bytes | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(photo_url) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    return None
    except Exception as e:
        return None

async def download_video_bytes(video_url: str, filename: str = "video.mp4"):
    """
    Преобразует URL видео в объект InputMediaBuffer.

    Args:
        video_url (str): Ссылка на видео.
        filename (str): Имя файла для медиа (по умолчанию 'video.mp4').

    Returns:
        InputMediaBuffer: Готовый объект для отправки.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status != 200:
                raise Exception(f"Ошибка загрузки видео: HTTP {response.status}")

            # Читаем данные как байты
            video_bytes = await response.read()

    # Создаём буфер из байтов
    return bytearray(video_bytes)


async def save_video_to_disk(video_url: str) -> str | None:
    """
    Скачивает видео по ссылке и сохраняет его в папку videos/.
    Возвращает путь к сохранённому файлу или None.
    """
    try:
        # Скачиваем видео в байты (используем вашу существующую функцию)
        video_bytes = await download_video_bytes(video_url)

        # Генерируем уникальное имя файла
        filename = f"{uuid.uuid4()}.mp4"
        # Папка для хранения видео (создастся, если её нет)
        save_dir = Path("videos")
        save_dir.mkdir(exist_ok=True)
        file_path = save_dir / filename

        # Асинхронно записываем байты в файл
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(video_bytes)

        return str(file_path)
    except Exception as e:
        print(f"Ошибка сохранения видео: {e}")
        return None
