from dotenv import load_dotenv
import os


class Config():
    def __init__(self, ):
        load_dotenv()
        self.token = os.getenv("TOKEN")
        self.admins = list(map(int, os.getenv("ADMINS_ID").split(",")))
