from dotenv import load_dotenv
load_dotenv()

from os import environ
from app import Bot, Web

bot = Bot(environ['TELEGRAM_TOKEN'])
web = Web()

if __name__ == '__main__':
    bot.start()
    web.start()
