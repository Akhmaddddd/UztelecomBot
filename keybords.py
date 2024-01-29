from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database import *



def inl_but_for_user():
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(
        InlineKeyboardButton(text='Наш Сайт', url='https://uztelecom.uz/')


    )
    markup.row(

        InlineKeyboardButton(text='Связаться с оператором', callback_data='connect_with')

    )
    markup.row(

        InlineKeyboardButton(text='Тарифы', callback_data='tarif')


    )
    markup.row(

        InlineKeyboardButton(text='Другое', callback_data='other')

    )
    return markup





def buttons_for_admin():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='Оператор')],
        [KeyboardButton(text='Пользователи')]
    ], resize_keyboard=True)



def inl_users():
    users = get_all_users()


    markup = InlineKeyboardMarkup(row_width=1)

    if users:

        buttons = []

        for user in users:
            print(user)
            btn = InlineKeyboardButton(text=f'Username: {user[1]} Имя: {user[2]}',
                                       callback_data=f'user_{user[0]}_{user[1]}')
            buttons.append(btn)

        markup.add(*buttons)

        row_buttons = [InlineKeyboardButton(text='Назад', callback_data='tgd')]


        row_buttons.append(InlineKeyboardButton("→", callback_data=f"forward"))

        markup.row(*row_buttons)

    else:
        markup.row(

            InlineKeyboardButton(text='Нет пользователей',callback_data='dd')

        )
        markup.row(
            InlineKeyboardButton(text='Назад', callback_data='tgd')
        )
    return markup







def inl_operators():
    operators = get_all_operators()

    markup = InlineKeyboardMarkup(row_width=1)
    if operators:
        buttons = []

        for operator in operators:
            btn = InlineKeyboardButton(text=f'Username: {operator[1]} Имя: {operator[2]}', callback_data=f'operator_{operator[0]}_{operator[1]}')
            buttons.append(btn)

        markup.add(*buttons)
        markup.row(

            InlineKeyboardButton(text='Назад', callback_data='qwer'),
            InlineKeyboardButton("→", callback_data=f"sled_")
        )
    else:
        markup.row(
            InlineKeyboardButton(text='Нет операторов', callback_data='dфыфd')
        )
        markup.row(
            InlineKeyboardButton(text='Назад', callback_data='qwer')
        )
    return markup

def user_detail__button(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    user_page = page_user()


    markup.row(
        InlineKeyboardButton(text='Удалить пользователя', callback_data=f'delete_{user_id}_{user_page}'),
        InlineKeyboardButton(text='Сделать оператором', callback_data=f'makeoperator_{user_id}_{user_page}')

    )
    markup.row(

        InlineKeyboardButton(text='Назад',callback_data=f'back_{user_page}'),

    )




    return markup




def operator_detail__button(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    operator_page = page_op()


    markup.row(
        InlineKeyboardButton(text='Удалить оператора', callback_data=f'opedel_{user_id}_{operator_page}'),
        InlineKeyboardButton(text='Понизить  оператором', callback_data=f'reduceoper_{user_id}_{operator_page}')

    )
    markup.row(
        InlineKeyboardButton(text='Назад', callback_data=f'nazad_{operator_page}')
    )

    return markup




def inl_users_2():
    users = get_next_users()


    markup = InlineKeyboardMarkup(row_width=1)

    if users:
        buttons = []

        for user in users:
            btn = InlineKeyboardButton(text=f'Username: {user[1]} Имя: {user[2]}',
                                       callback_data=f'user_{user[0]}_{user[1]}')
            buttons.append(btn)

        markup.add(*buttons)

        markup.row(
            InlineKeyboardButton("←", callback_data=f"prevpage"),
            InlineKeyboardButton(text='Назад', callback_data='tgd'),
            InlineKeyboardButton("→", callback_data=f"forward")
        )


    else:
        markup.row(

            InlineKeyboardButton(text='Нет пользователей', callback_data='dd')

        )
        markup.row(
            InlineKeyboardButton(text='Назад', callback_data='tgd')
        )
        markup.row(
            InlineKeyboardButton("←", callback_data=f"prevpage")
        )
    return markup

def inl_users_back():
    users = get_previous_users()

    markup = InlineKeyboardMarkup(row_width=1)
    if users:
        buttons = []

        for user in users:
            btn = InlineKeyboardButton(text=f'Username: {user[1]} Имя: {user[2]}',
                                       callback_data=f'user_{user[0]}_{user[1]}')
            buttons.append(btn)

        markup.add(*buttons)
        markup.row(
            InlineKeyboardButton("←", callback_data=f"prevpage"),
            InlineKeyboardButton(text='Назад', callback_data='tgd'),
            InlineKeyboardButton("→", callback_data=f"forward")
        )
    else:
        markup.row(
            InlineKeyboardButton(text='Нет операторов', callback_data='dфыфd')
        )
        markup.row(
            InlineKeyboardButton(text='Назад', callback_data='tgd'),

        )
        markup.row(
            InlineKeyboardButton("→", callback_data=f"forward")
        )

    return markup


def inl_operators_2():
    operators = get_next_operators()

    markup = InlineKeyboardMarkup(row_width=1)
    if operators:
        buttons = []

        for operator in operators:
            btn = InlineKeyboardButton(text=f'Username: {operator[1]} Имя: {operator[2]}',
                                       callback_data=f'operator_{operator[0]}_{operator[1]}')
            buttons.append(btn)

        markup.add(*buttons)
        markup.row(
            InlineKeyboardButton("←", callback_data=f"pered"),
            InlineKeyboardButton(text='Назад', callback_data='qwer'),
            InlineKeyboardButton("→", callback_data=f"sled_")
        )
    else:
        markup.row(
            InlineKeyboardButton(text='Нет операторов', callback_data='dфыфd')
        )
        markup.row(
            InlineKeyboardButton(text='Назад', callback_data='qwer')
        )
        markup.row(
            InlineKeyboardButton("←", callback_data=f"pered")
        )
    return markup


def inl_operators_back():
    operators = get_previous_operators()

    markup = InlineKeyboardMarkup(row_width=1)
    if operators:
        buttons = []

        for operator in operators:
            btn = InlineKeyboardButton(text=f'Username: {operator[1]} Имя: {operator[2]}',
                                       callback_data=f'operator_{operator[0]}_{operator[1]}')
            buttons.append(btn)

        markup.add(*buttons)
        markup.row(
            InlineKeyboardButton("←", callback_data=f"pered"),
            InlineKeyboardButton(text='Назад', callback_data='qwer'),
            InlineKeyboardButton("→", callback_data=f"sled_")
        )
    else:
        markup.row(
            InlineKeyboardButton(text='Нет операторов', callback_data='dфыфd')
        )
        markup.row(
            InlineKeyboardButton(text='Назад', callback_data='qwer'),

        )
        markup.row(
            InlineKeyboardButton("→", callback_data=f"sled_")
        )

    return markup



def inl_operators_nazad(op_page):
    operators = back_button_op(op_page)

    markup = InlineKeyboardMarkup(row_width=1)
    if operators:
        buttons = []

        for operator in operators:
            btn = InlineKeyboardButton(text=f'Username: {operator[1]} Имя: {operator[2]}',
                                       callback_data=f'operator_{operator[0]}_{operator[1]}')
            buttons.append(btn)

        markup.add(*buttons)
        markup.row(
            InlineKeyboardButton("←", callback_data=f"pered"),
            InlineKeyboardButton(text='Назад', callback_data='qwer'),
            InlineKeyboardButton("→", callback_data=f"sled_")
        )
    else:
        markup.row(
            InlineKeyboardButton(text='Нет операторов', callback_data='dфыфd')
        )
        markup.row(
            InlineKeyboardButton(text='Назад', callback_data='qwer'),

        )
        markup.row(
            InlineKeyboardButton("→", callback_data=f"sled_")
        )

    return markup



def inl_users_nazad(user_page):
    users = back_button_user(user_page)

    markup = InlineKeyboardMarkup(row_width=1)
    if users:
        buttons = []

        for user in users:
            btn = InlineKeyboardButton(text=f'Username: {user[1]} Имя: {user[2]}',
                                       callback_data=f'user_{user[0]}_{user[1]}')
            buttons.append(btn)

        markup.add(*buttons)
        markup.row(
            InlineKeyboardButton("←", callback_data=f"prevpage"),
            InlineKeyboardButton(text='Назад', callback_data='tgd'),
            InlineKeyboardButton("→", callback_data=f"forward")
        )
    else:
        markup.row(
            InlineKeyboardButton(text='Нет операторов', callback_data='dфыфd')
        )
        markup.row(
            InlineKeyboardButton(text='Назад', callback_data='tgd'),

        )
        markup.row(
            InlineKeyboardButton("→", callback_data=f"forward")
        )

    return markup



def inl_btn_to_connect():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(text='Связаться с оператором',callback_data='connect'),
        InlineKeyboardButton(text='Назад',callback_data='vmenu')

    )


    return markup


def inl_operator_btn_user(chat_id, username):
    inline_markup = InlineKeyboardMarkup(row_width=1)
    inline_markup.row(
        InlineKeyboardButton(text='Ответить пользователю', callback_data=f'responsefromoper_{chat_id}_{username}'),
    )



    return inline_markup



def inl_con_user(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(text='Отвеетить оператору', callback_data=f'answerto_{chat_id}')
    )
    return markup

def btn_from_coonect_tomain():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='На главную')]

    ], resize_keyboard=True)


def ses_offff():
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(
        KeyboardButton(text='Завершить сессию')
    )
    return reply_markup
