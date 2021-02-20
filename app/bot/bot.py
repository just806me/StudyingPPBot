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
            [CommandHandler('start', handlers.sc_start, run_async=True)],
            {
                StartConversationState.NAME: [
                    MessageHandler(Filters.text, handlers.sc_set_name, run_async=True)
                ],
                StartConversationState.USERNAME: [
                    MessageHandler(Filters.text, handlers.sc_set_username, run_async=True)
                ],
                StartConversationState.CONFIRMATION: [
                    CallbackQueryHandler(handlers.sc_save_user, pattern='^save$', run_async=True),
                    CallbackQueryHandler(handlers.sc_reset_user, pattern='^reset$', run_async=True),
                ],
            },
            [],
        ))
        self.updater.dispatcher.add_handler(CommandHandler('whoami', handlers.whoami, run_async=True))
        self.updater.dispatcher.add_handler(CommandHandler('problem', handlers.create_problem, run_async=True))
        self.updater.dispatcher.add_handler(CommandHandler('submission', handlers.create_submission, run_async=True))
        self.updater.dispatcher.add_handler(CommandHandler('help', handlers.help, run_async=True))
        self.updater.dispatcher.add_handler(CommandHandler('results', handlers.results, run_async=True))
        self.updater.dispatcher.add_handler(CommandHandler('broadcast', handlers.broadcast, run_async=True))
        self.updater.dispatcher.add_handler(CommandHandler('unicast', handlers.unicast, run_async=True))

    def start(self) -> None:
        self.updater.start_polling()
