from telegram import ReplyKeyboardMarkup

SC_START_OK_TEXT = "Привіт! Спершу мені потрібно взнати твої дані. Надішли своє прізвище та ім'я."

SC_START_ERROR_TEXT = ''

SC_SET_NAME_TEXT = "А тепер надішли свій username на e-olimp. Він повинен бути точно як на сайті, інакше розв'язки не будуть прийматись."

SC_SET_USERNAME_TEXT = '''Добре. Ось дані, які я отримав:
Прізвище та ім'я: %s
Username: %s

Якщо все вірно - натисни 'Зберегти', щоб продовжити. Якщо виникла помилка - натисни 'Скинути', щоб розпочати знову.'''

SC_SET_USERNAME_MARKUP = ReplyKeyboardMarkup([['Зберегти', 'Скинути']], one_time_keyboard=True, resize_keyboard=True)

SC_SAVE_USER_TEXT = "Інформацію успішно збережено!"

SC_RESRT_USER_TEXT = "Надішли своє прізвище та ім'я."

WHOAMI_NONE_TEXT = 'Мені про тебе нічого не відомо!'

WHOAMI_USER_TEXT = '''Ось, що мені відомо про тебе:
ID: %s
Прізвище та ім'я: %s
Username: %s
Deleted at: %s'''

CREATE_PROBLEM_SUCCESS = "Успішно додано задачу з ІД %s та групою %s."

CREATE_PROBLEM_EXISTS = "Задача з ІД %s вже існує."

CREATE_SUBMISSION_SUCCESS = "Успішно додано розв'язок з ІД %s, ІД задачі %s та балами %s."

CREATE_SUBMISSION_ERROR_CANNOT_FETCH = "Не вийшло завантажити дані з e-olimp, спробуй пізніше."

CREATE_SUBMISSION_ERROR_PROBLEM_NOT_FOUND = "Розв'язки для задачі за ІД %s не приймаються."

CREATE_SUBMISSION_ERROR_USERNAME_INVALID = "Твій username (%s) не співпадає з username у розв'зку (%s)."

CREATE_SUBMISSION_ERROR_SUBMISSION_EXISTS = "Розв'язок з ІД %s вже додано."
