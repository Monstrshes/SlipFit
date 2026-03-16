
import pandas as pd
from io import BytesIO


def get_users_buffer(words):
    df = pd.DataFrame(words, columns=['user_id'])
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    return excel_buffer.getvalue()  # возвращаем байты