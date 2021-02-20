from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler
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
                    MessageHandler(Filters.text, handlers.sc_set_name)
                ],
                StartConversationState.USERNAME: [
                    MessageHandler(Filters.text, handlers.sc_set_username)
                ],
                StartConversationState.CONFIRMATION: [
                    CallbackQueryHandler(handlers.sc_save_user, pattern='^save$'),
                    CallbackQueryHandler(handlers.sc_reset_user, pattern='^reset$'),
                ],
            },
            [],
        ))
        self.updater.dispatcher.add_handler(CommandHandler('whoami', handlers.whoami))
        self.updater.dispatcher.add_handler(CommandHandler('problem', handlers.create_problem))
        self.updater.dispatcher.add_handler(CommandHandler('submission', handlers.create_submission))
        self.updater.dispatcher.add_handler(CommandHandler('help', handlers.help))
        self.updater.dispatcher.add_handler(CommandHandler('results', handlers.results))
        self.updater.dispatcher.add_handler(CommandHandler('broadcast', handlers.broadcast))
        self.updater.dispatcher.add_handler(CommandHandler('unicast', handlers.unicast))

    def start(self) -> None:
        self.updater.start_polling()
