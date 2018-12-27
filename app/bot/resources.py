from telegram import InlineKeyboardMarkup, InlineKeyboardButton

SC_START_OK_TEXT = "Привіт! Спершу мені потрібно взнати твої дані. Надішли своє прізвище та ім'я."

SC_START_ERROR_TEXT = ''

SC_SET_NAME_TEXT = "А тепер надішли свій нік на e-olimp. Він повинен бути точно як на сайті, інакше розв'язки не будуть прийматись."

SC_SET_USERNAME_TEXT = '''Добре. Ось дані, які я отримав:
Прізвище та ім'я: %s
Нік: %s

Якщо все вірно - натисни 'Зберегти', щоб продовжити. Якщо виникла помилка - натисни 'Скинути', щоб розпочати знову.'''

SC_SET_USERNAME_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton('Зберегти', callback_data='save'),
    InlineKeyboardButton('Скинути', callback_data='reset'),
]])

SC_SAVE_USER_TEXT = "Інформацію успішно збережено!"

SC_RESET_USER_TEXT = "Надішли своє прізвище та ім'я."

HELP_TEXT = '''Маленький хелп вам від мене. Я знаю три команди:
по команді /whoami я виводжу інформацію про тебе;
команда /submission id змусить мене додати твоє відправлення в список. Тільки не роби з мене дурня, якщо я не знаю такого завдання або ти вирішиш надіслати не своє рішення я на тебе ображуся.
І ще є /help там тебе чекає цей текст

Успіху вам і нехай переможе найсильніший, Мандрівник!'''

WHOAMI_NONE_TEXT = 'Мені про тебе нічого не відомо!'

WHOAMI_USER_TEXT = '''Ось, що мені відомо про тебе:
ID: %s
Прізвище та ім'я: %s
Нік: %s
Deleted at: %s'''

CREATE_PROBLEM_SUCCESS = "Успішно додано задачу з ІД %s та групою %s."

CREATE_PROBLEM_EXISTS = "Задача з ІД %s вже існує."

CREATE_SUBMISSION_SUCCESS = "Успішно додано розв'язок %s для задачі %s з %s балами."

CREATE_SUBMISSION_ERROR_SYNTAX = "Необхідно виконати команду у форматі /submission id, наприклад /submission 4932458"

CREATE_SUBMISSION_ERROR_CANNOT_FETCH = "Не вийшло завантажити дані з e-olimp, спробуй пізніше."

CREATE_SUBMISSION_ERROR_PROBLEM_NOT_FOUND = "Розв'язки для задачі з ІД %s не приймаються."

CREATE_SUBMISSION_ERROR_USERNAME_INVALID = "Твій нік (%s) не співпадає з ніком у розв'зку (%s)."

CREATE_SUBMISSION_ERROR_SUBMISSION_EXISTS = "Розв'язок з ІД %s вже додано."
