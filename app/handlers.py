from os import environ
from typing import Dict, Any
from enum import Enum, unique, auto
from telegram.ext import run_async, ConversationHandler
from telegram import Bot, Update

from . import resources
from .database import Database
from .models import User


db = Database(environ['DATABASE'])


@unique
class StartConversationState(Enum):
    NAME = auto()
    USERNAME = auto()
    CONFIRMATION = auto()


@run_async
def sc_start(bot: Bot, update: Update) -> StartConversationState:
    user = User.find(db, update.message.chat.id, True)
    if user is not None:
        update.message.reply_markdown(resources.SC_START_ERROR_TEXT)
        return ConversationHandler.END
    else:
        update.message.reply_markdown(resources.SC_START_OK_TEXT)
        return StartConversationState.NAME


@run_async
def sc_set_name(bot: Bot, update: Update, chat_data: Dict[str, Any]) -> StartConversationState:
    chat_data['name'] = update.message.text.strip()
    update.message.reply_markdown(resources.SC_SET_NAME_TEXT)
    return StartConversationState.USERNAME


@run_async
def sc_set_username(bot: Bot, update: Update, chat_data: Dict[str, str]) -> StartConversationState:
    chat_data['username'] = update.message.text.strip()
    update.message.reply_markdown(resources.SC_SET_USERNAME_TEXT % (chat_data['name'], chat_data['username']),
                                  reply_markup=resources.SC_SET_USERNAME_MARKUP)
    return StartConversationState.CONFIRMATION


@run_async
def sc_save_user(bot: Bot, update: Update, chat_data: Dict[str, str]) -> StartConversationState:
    User.create(db, update.message.chat.id, chat_data['name'], chat_data['username'])
    chat_data.clear()
    update.message.reply_markdown(resources.SC_SAVE_USER_TEXT)
    return ConversationHandler.END


@run_async
def sc_reset_user(bot: Bot, update: Update, chat_data: Dict[str, str]) -> StartConversationState:
    chat_data.clear()
    update.message.reply_markdown(resources.SC_RESRT_USER_TEXT)
    return StartConversationState.NAME


@run_async
def whoami(bot: Bot, update: Update) -> None:
    user = User.find(db, update.message.chat.id, True)
    if user is None:
        update.message.reply_markdown(resources.WHOAMI_NONE_TEXT)
    else:
        update.message.reply_markdown(resources.WHOAMI_USER_TEXT % (user.id, user.name, user.username, user.deleted_at))
