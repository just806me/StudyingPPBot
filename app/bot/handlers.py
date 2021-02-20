from os import environ
from enum import Enum, unique, auto
from telegram.ext import run_async, ConversationHandler, CallbackContext
from telegram import Update

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
def sc_start(update: Update, context: CallbackContext) -> StartConversationState:
    user = User.find(db, update.message.chat_id, True)
    if user is not None:
        update.message.reply_text(resources.SC_START_ERROR_TEXT)
        return ConversationHandler.END
    else:
        update.message.reply_text(resources.SC_START_OK_TEXT)
        return StartConversationState.NAME


@run_async
def sc_set_name(update: Update, context: CallbackContext) -> StartConversationState:
    context.chat_data['name'] = update.message.text.strip()
    update.message.reply_text(resources.SC_SET_NAME_TEXT)
    return StartConversationState.USERNAME


@run_async
def sc_set_username(update: Update, context: CallbackContext) -> StartConversationState:
    context.chat_data['username'] = update.message.text.strip()
    text = resources.SC_SET_USERNAME_TEXT % (context.chat_data['name'], context.chat_data['username'])
    update.message.reply_text(text, reply_markup=resources.SC_SET_USERNAME_MARKUP)
    return StartConversationState.CONFIRMATION


@run_async
def sc_save_user(update: Update, context: CallbackContext) -> StartConversationState:
    User.create(db, update.callback_query.message.chat_id, context.chat_data['name'], context.chat_data['username'])
    context.chat_data.clear()
    update.callback_query.message.edit_text(resources.SC_SAVE_USER_TEXT)
    return ConversationHandler.END


@run_async
def sc_reset_user(update: Update, context: CallbackContext) -> StartConversationState:
    context.chat_data.clear()
    update.callback_query.message.edit_text(resources.SC_RESET_USER_TEXT)
    return StartConversationState.NAME


@run_async
def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(resources.HELP_TEXT)


@run_async
def whoami(update: Update, context: CallbackContext) -> None:
    user = User.find(db, update.message.chat_id, True)
    if user is None:
        update.message.reply_text(resources.WHOAMI_NONE_TEXT)
    else:
        update.message.reply_text(resources.WHOAMI_USER_TEXT % (user.id, user.name, user.username, user.deleted_at))


@run_async
def create_problem(update: Update, context: CallbackContext) -> None:
    pid, pgroup = map(int, context.args)
    if not update.message.chat_id in ADMIN_IDS:
        return
    if Problem.find(db, pid) is not None:
        update.message.reply_text(resources.CREATE_PROBLEM_EXISTS % pid)
    else:
        problem = Problem.create(db, pid, pgroup)
        update.message.reply_text(resources.CREATE_PROBLEM_SUCCESS % (problem.id, problem.group))


@run_async
def create_submission(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text(resources.CREATE_SUBMISSION_ERROR_SYNTAX)
        return
    user = User.find(db, update.message.chat_id)
    if user is None:
        return
    parser = EOlimpParser(int(context.args[0]), user, db)
    parser.execute()
    if parser.errors:
        update.message.reply_text(parser.errors[0])
    else:
        submission = parser.create_submission()
        update.message.reply_text(resources.CREATE_SUBMISSION_SUCCESS %
                                  (submission.id, submission.problem_id, submission.score))


@run_async
def results(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(resources.RESULTS_TEXT)


@run_async
def broadcast(update: Update, context: CallbackContext) -> None:
    if not update.message.chat_id in ADMIN_IDS:
        return
    if len(context.args) == 0:
        update.message.reply_text(resources.BROADCAST_ERROR_SYNTAX)
        return
    text = update.message.text[11:]
    users = User.all(db)
    for user in users:
        context.bot.send_message(user.id, text)
    update.message.reply_text(resources.BROADCAST_SUCCESS % len(users))


@run_async
def unicast(update: Update, context: CallbackContext) -> None:
    if not update.message.chat_id in ADMIN_IDS:
        return
    if len(context.args) < 2:
        update.message.reply_text(resources.UNICAST_ERROR_SYNTAX)
        return
    uid = context.args[0]
    user = User.find(db, uid)
    if user is None:
        update.message.reply_text(resources.UNICAST_ERROR_NOT_FOUND % uid)
        return
    context.bot.send_message(user.id, update.message.text[(len(uid) + 9):])
    update.message.reply_text(resources.UNICAST_SUCCESS % user.username)
