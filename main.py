from dotenv import load_dotenv
load_dotenv()

from os import environ
from app import Bot


bot = Bot(environ['TELEGRAM_TOKEN'])

if __name__ == '__main__':
    bot.start()
