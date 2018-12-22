from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler
from telegram.ext.filters import Filters

from .handlers import StartConversationState
from . import handlers


class Bot:
    def __init__(self, token: str) -> None:
        self.updater = Updater(token)
        self.__register_handlers__()

    def __register_handlers__(self) -> None:
        self.updater.dispatcher.add_handler(ConversationHandler(
            [CommandHandler('start', handlers.sc_start)],
            {
                StartConversationState.NAME: [
                    MessageHandler(Filters.text, handlers.sc_set_name, pass_chat_data=True)
                ],
                StartConversationState.USERNAME: [
                    MessageHandler(Filters.text, handlers.sc_set_username, pass_chat_data=True)
                ],
                StartConversationState.CONFIRMATION: [
                    RegexHandler('^Зберегти$', handlers.sc_save_user, pass_chat_data=True),
                    RegexHandler('^Скинути$', handlers.sc_reset_user, pass_chat_data=True),
                ]
            },
            []
        ))
        self.updater.dispatcher.add_handler(CommandHandler('whoami', handlers.whoami))
        self.updater.dispatcher.add_handler(CommandHandler('problem', handlers.create_problem, pass_args=True))

    def start(self) -> None:
        self.updater.start_polling()
        self.updater.idle()
