from os import environ
from typing import Dict, Any, List
from enum import Enum, unique, auto
from telegram.ext import run_async, ConversationHandler
from telegram import Bot, Update

from ..database import Database
from ..models import User, Problem
from .eolymp_parser import EOlimpParser
from . import resources


ADMIN_IDS = list(map(int, environ['ADMIN_IDS'].split(',')))

db = Database()


@unique
class StartConversationState(Enum):
    NAME = auto()
    USERNAME = auto()
    CONFIRMATION = auto()


@run_async
def sc_start(bot: Bot, update: Update) -> StartConversationState:
    user = User.find(db, update.message.chat_id, True)
    if user is not None:
        update.message.reply_text(resources.SC_START_ERROR_TEXT)
        return ConversationHandler.END
    else:
        update.message.reply_text(resources.SC_START_OK_TEXT)
        return StartConversationState.NAME


@run_async
def sc_set_name(bot: Bot, update: Update, chat_data: Dict[str, str]) -> StartConversationState:
    chat_data['name'] = update.message.text.strip()
    update.message.reply_text(resources.SC_SET_NAME_TEXT)
    return StartConversationState.USERNAME


@run_async
def sc_set_username(bot: Bot, update: Update, chat_data: Dict[str, str]) -> StartConversationState:
    chat_data['username'] = update.message.text.strip()
    update.message.reply_text(resources.SC_SET_USERNAME_TEXT % (chat_data['name'], chat_data['username']),
                              reply_markup=resources.SC_SET_USERNAME_MARKUP)
    return StartConversationState.CONFIRMATION


@run_async
def sc_save_user(bot: Bot, update: Update, chat_data: Dict[str, str]) -> StartConversationState:
    User.create(db, update.callback_query.message.chat_id, chat_data['name'], chat_data['username'])
    chat_data.clear()
    update.callback_query.message.edit_text(resources.SC_SAVE_USER_TEXT)
    return ConversationHandler.END


@run_async
def sc_reset_user(bot: Bot, update: Update, chat_data: Dict[str, str]) -> StartConversationState:
    chat_data.clear()
    update.callback_query.message.edit_text(resources.SC_RESET_USER_TEXT)
    return StartConversationState.NAME


@run_async
def help(bot: Bot, update: Update) -> None:
    update.message.reply_text(resources.HELP_TEXT)


@run_async
def whoami(bot: Bot, update: Update) -> None:
    user = User.find(db, update.message.chat_id, True)
    if user is None:
        update.message.reply_text(resources.WHOAMI_NONE_TEXT)
    else:
        update.message.reply_text(resources.WHOAMI_USER_TEXT % (user.id, user.name, user.username, user.deleted_at))


@run_async
def create_problem(bot: Bot, update: Update, args: List[str]) -> None:
    if not update.message.chat_id in ADMIN_IDS:
        return
    if Problem.find(db, int(args[0])) is not None:
        update.message.reply_text(resources.CREATE_PROBLEM_EXISTS % int(args[0]))
    else:
        problem = Problem.create(db, int(args[0]), int(args[1]))
        update.message.reply_text(resources.CREATE_PROBLEM_SUCCESS % (problem.id, problem.group))


@run_async
def create_submission(bot: Bot, update: Update, args: List[str]) -> None:
    if len(args) != 1:
        update.message.reply_text(resources.CREATE_SUBMISSION_ERROR_SYNTAX)
        return
    user = User.find(db, update.message.chat_id)
    if user is None:
        return
    parser = EOlimpParser(int(args[0]), user, db)
    parser.execute()
    if parser.errors:
        update.message.reply_text(parser.errors[0])
    else:
        submission = parser.create_submission()
        update.message.reply_text(resources.CREATE_SUBMISSION_SUCCESS %
                                  (submission.id, submission.problem_id, submission.score))


@run_async
def results(bot: Bot, update: Update) -> None:
    update.message.reply_text(resources.RESULTS_TEXT)

@run_async
def broadcast(bot: Bot, update: Update, args: List[str]) -> None:
    if not update.message.chat_id in ADMIN_IDS:
        return
    if len(args) == 0:
        update.message.reply_text(resources.BROADCAST_ERROR_SYNTAX)
        return
    text = update.message.text[11:]
    users = User.all(db)
    for user in users:
        bot.send_message(user.id, text)
    update.message.reply_text(resources.BROADCAST_SUCCESS % len(users))
