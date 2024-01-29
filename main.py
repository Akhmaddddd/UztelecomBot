import random
import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentTypes,ParseMode
from database import *

from keybords import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware



TOKEN = '6723195739:AAGl2XXX6anuSmkZUZ03QTfPwGlOOR0Uyow'

bot = Bot(TOKEN)

dp = Dispatcher(bot)
dp.storage = MemoryStorage()




class UserStates(StatesGroup):
    entering_name = State()


class YourState(StatesGroup):
    waiting_for_message = State()


@dp.message_handler(commands=['start'])
async def command_start(message: Message, state: FSMContext):
    await message.answer(f'Здравствуйте {message.from_user.full_name}.\nВас приветствует UztelecomBot')
    chat_id = message.chat.id
    user = first_select(chat_id)

    if user:
        await operator_or_user(message)
    else:
        await message.answer('Введите фамилию и имя')

        await UserStates.entering_name.set()


@dp.message_handler(lambda message: message.text and not message.text.startswith('/'), state=UserStates.entering_name)
async def handle_name_input(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user = first_select(chat_id)

    if user:
        pass
    else:
        fullname = message.text
        username = message.from_user.username
        insert_to_user(chat_id, username, fullname)
        await operator_or_user(message)

        await state.finish()


async def operator_or_user(message: Message):
    await message.answer('Спасибо за  ваш отклик \n Выберите направление ', reply_markup=inl_but_for_user())


@dp.message_handler(commands=['admin'])
async def admin_page(message: Message):
    chat_id = message.chat.id
    admin = check_admin(chat_id)
    if admin == 'admin':
        await message.answer('Здравствуйте админ', reply_markup=buttons_for_admin())
    else:
        pass


@dp.message_handler(lambda message: 'Пользователи' in message.text)
async def user_admin_page(message: Message):
    chat_id = message.chat.id

    await message.answer('Список пользователей', reply_markup=inl_users())

    sent_message = await message.answer(text=message.text, reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=chat_id, message_id=sent_message.message_id)


@dp.message_handler(lambda message: 'Оператор' in message.text)
async def operator_admin_page(message: Message):
    chat_id = message.chat.id

    await message.answer('Список операторов', reply_markup=inl_operators())

    sent_message = await message.answer(text=message.text, reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=chat_id, message_id=sent_message.message_id)


@dp.callback_query_handler(lambda call: 'user' in call.data)
async def user_detail_for_admin(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, user_id, *username_parts = call.data.split('_')
    username = '_'.join(username_parts)
    user_id = user_id


    message_id = call.message.message_id
    info_user = user_info(username)

    details = f'''
User_id: {info_user[0]}
Username: {info_user[1]}
Telegram_id: {info_user[2]}
Full_name: {info_user[3]}
Status: {info_user[4]}
    '''

    await bot.edit_message_text(details, chat_id, message_id, reply_markup=user_detail__button(user_id))


@dp.callback_query_handler(lambda call: 'delete' in call.data)
async def delete_user_for_admin(call: CallbackQuery):
    message = call.message.message_id
    chat_id = call.message.chat.id
    _, user_id, user_page = call.data.split('_')
    if function_of_delete(user_id):
        await bot.answer_callback_query(call.id, 'Юзер удален')

        await bot.edit_message_text('Список пользователей ',chat_id=chat_id,  message_id=message,reply_markup=inl_users_nazad(user_page))


    else:
        await bot.answer_callback_query(call.id, 'Юзер not удален')


@dp.callback_query_handler(lambda call: 'makeoperator_' in call.data)
async def update_user_for_admin(call: CallbackQuery):
    message = call.message.message_id
    chat_id = call.message.chat.id
    _, user_id, user_page = call.data.split('_')
    if function_update_to_operator(user_id):
        await bot.answer_callback_query(call.id, 'Юзер повышен')
        await bot.edit_message_text('Список пользователей ', chat_id=chat_id, message_id=message,
                                    reply_markup=inl_users_nazad(user_page))

    else:
        await bot.answer_callback_query(call.id, 'Юзер not updated')


@dp.callback_query_handler(lambda call: 'back' in call.data)
async def return_to_category_user(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, user_page = call.data.split('_')


    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, 'Список пользователей ', reply_markup=inl_users_nazad(user_page))


@dp.callback_query_handler(lambda call: 'operator' in call.data)
async def operator_detail_for_admin(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, user_id, *username_parts = call.data.split('_')
    username = '_'.join(username_parts)
    user_id = user_id

    message_id = call.message.message_id
    info_user = user_info(username)

    details = f'''
User_id: {info_user[0]}
Username: {info_user[1]}
Telegram_id: {info_user[2]}
Full_name: {info_user[3]}
Status: {info_user[4]}
    '''

    await bot.edit_message_text(details, chat_id, message_id, reply_markup=operator_detail__button(user_id))


@dp.callback_query_handler(lambda call: 'nazad' in call.data)
async def return_to_category_operator(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _,op_page= call.data.split('_')


    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, 'Список операторов ', reply_markup=inl_operators_nazad(op_page))


@dp.callback_query_handler(lambda call: 'opedel' in call.data)
async def delete_operator_for_admin(call: CallbackQuery):
    message = call.message.message_id
    chat_id = call.message.chat.id
    _, user_id, op_page = call.data.split('_')
    if function_of_delete_operator(user_id):
        await bot.answer_callback_query(call.id, 'Оператор  удален')

        await bot.edit_message_text('Список операторов ', chat_id=chat_id, message_id=message,
                                    reply_markup=inl_operators_nazad(op_page))


    else:
        await bot.answer_callback_query(call.id, 'Оператор not удален')


@dp.callback_query_handler(lambda call: 'reduceoper' in call.data)
async def reduce_operator_for_admin(call: CallbackQuery):
    message = call.message.message_id
    chat_id = call.message.chat.id
    _, user_id, op_page = call.data.split('_')
    if function_reduce_to_user(user_id):
        await bot.answer_callback_query(call.id, 'Оператор понижен')
        await bot.edit_message_text('Список операторов ', chat_id=chat_id, message_id=message,
                                    reply_markup=inl_operators_nazad(op_page))
    else:
        await bot.answer_callback_query(call.id, 'Оператор not понижен')


@dp.callback_query_handler(lambda call: 'qwer' in call.data)
async def return_to_main_admin(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, 'Нажмите на кнопку для информации ', reply_markup=buttons_for_admin())


@dp.callback_query_handler(lambda call: 'tgd' in call.data)
async def return_to_main_user(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, 'Нажмите на кнопку для информации ', reply_markup=buttons_for_admin())


@dp.callback_query_handler(lambda call: 'forward' in call.data or 'prevpage' in call.data )
async def paginate_users(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id




    if 'forward' in call.data:
        await bot.edit_message_text('Список пользователей', chat_id, message_id, reply_markup=inl_users_2())
    elif 'prevpage' in call.data:
        try:
            await bot.edit_message_text('Список пользователей', chat_id, message_id, reply_markup=inl_users_back())
        except:
            await bot.answer_callback_query(call.id, 'Это самая первая страница')






@dp.callback_query_handler(lambda call: 'sled' in call.data or 'pered' in call.data )
async def paginate_operators(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id




    if 'sled' in call.data:
        await bot.edit_message_text('Список операторов', chat_id, message_id, reply_markup=inl_operators_2())
    elif 'pered' in call.data:
        try:
            await bot.edit_message_text('Список операторов', chat_id, message_id, reply_markup=inl_operators_back())
        except:
            await bot.answer_callback_query(call.id, 'Это самая первая страница')





#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#---------------------------------------------------------reverse response--------------to_operator



class MyState(StatesGroup):
    waiting_for_message = State()

class OperState(StatesGroup):
    waiting_for_message_from_user = State()

class UserState(StatesGroup):
    waiting_for_message_from_operator = State()

@dp.callback_query_handler(lambda call: 'other' in call.data)
async def button_other(call: CallbackQuery):
    chat_id = call.message.chat.id
    await bot.send_message(chat_id, 'Нажмите на кнопку для дальнейших действий', reply_markup=inl_btn_to_connect())

@dp.callback_query_handler(lambda call: 'connect' in call.data)
async def connect_op(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    support_id_operator()
    await bot.delete_message(chat_id=chat_id,message_id=message_id)
    # Edit the message to prompt the user to write a message
    try:
        oper_ids = suport_ids

        operator_id = oper_ids[0]
        await bot.send_message(chat_id,'Напишите текст оператору',  reply_markup=btn_from_coonect_tomain())
        endses_on = endsession_on(chat_id)
        # Set the user's state to wait for a message
        insup_on(chat_id)
        await MyState.waiting_for_message.set()
        await state.update_data(original_message_id=message_id)
    except:
        await bot.send_message(chat_id,'Нет свободных операторов',reply_markup=btn_from_coonect_tomain())



@dp.message_handler(state=MyState.waiting_for_message, content_types=ContentTypes.TEXT)
async def obtain_message(message: Message, state: FSMContext):

    # Get the original message ID from the state
    chat_id = message.chat.id
    check_session = get_endses(chat_id)
    if message.text == 'На главную':
        await state.finish()
        await tomain(message)
        off_sup = suppro__off(chat_id)

    data = await state.get_data()
    original_message_id = data.get("original_message_id")
    oper_ids = suport_ids
    get_in_sup = obtain_insup(chat_id)
    operator_id = oper_ids[0]
    msg = firts_msg(operator_id)
    # Do something with the obtained message
    obtained_message_text = message.text
    if check_session =='no':
        if obtained_message_text and obtained_message_text != 'На главную':

            set_busy_status = busy_oper(operator_id)

            # Проверяем, первое ли это сообщение
            if msg=='no':
                insup_on(operator_id)
                # Если это первое сообщение, добавляем кнопку
                await bot.send_message(
                    operator_id,
                    f'Новое сообщение от {message.from_user.username}\n'
                    f'Сообщение : {obtained_message_text}',
                    reply_markup=inl_operator_btn_user(chat_id, message.from_user.username)
                )

                upfate_msg(operator_id)
            elif msg=='yes':
                # Если это не первое сообщение, отправляем без кнопки
                get_insup_oper = obtain_insup_status(operator_id)
                if get_insup_oper == 'no':
                    await bot.send_message(
                        operator_id,
                        f'Новое сообщение от {message.from_user.username}\n'
                        f'Сообщение : {obtained_message_text}',
                        reply_markup=inl_operator_btn_user(chat_id, message.from_user.username)
                    )
                else:
                    await bot.send_message(
                        operator_id,
                        f'Новое сообщение от {message.from_user.username}\n'
                        f'Сообщение : {obtained_message_text}'
                    )
        else:
            # Здесь может быть дополнительная обработка, если сообщение - 'На главную'
            pass
    else:
        pass


@dp.callback_query_handler(lambda call: 'vmenu' in call.data)
async def connect_op(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text('Выберите направление', chat_id, message_id,reply_markup=inl_but_for_user())


@dp.callback_query_handler(lambda call: 'responsefromoper_' in call.data)
async def response_to_user(call: CallbackQuery, state: FSMContext):
    _, user_id, *username_parts = call.data.split('_')
    username = '_'.join(username_parts)
    chat_id = call.message.chat.id
    conec= connect_bet(chat_id,user_id)

    # Set the user's state to wait for a message
    await OperState.waiting_for_message_from_user.set()

    # Update data in FSMContext
    await state.update_data(original_message_id=user_id)

    await bot.send_message(chat_id, f'Вы находитесь в состоянии обратной связи с пользователем ,для завершения связи с пользователем нажмите на кнопку\n'
                                    f'Напишите ответ для пользователя {username}',reply_markup=ses_offff())


@dp.message_handler(state=OperState.waiting_for_message_from_user, content_types=ContentTypes.TEXT)
async def obtain_message_from_user(message: Message, state: FSMContext):
    # Get the original user ID from the state
    if message.text == 'Завершить сессию':
        await state.finish()
        await end_ses(message)
    data = await state.get_data()
    original_user_id = data.get("original_message_id")


    # Do something with the obtained message from the user
    obtained_message_text = message.text
    if obtained_message_text != 'Завершить сессию':
        chat_id = message.chat.id
        try:
            get_ids = get_connect_id(chat_id)

            get_in_sup = obtain_insup(get_ids[1])

            if get_in_sup == 'no':
                await bot.send_message(get_ids[1],f'Вам сообщение от оператора:\n{obtained_message_text}',reply_markup=inl_con_user(chat_id))
            elif get_in_sup == 'yes':
                await bot.send_message(get_ids[1],f'Вам сообщение от оператора:\n{obtained_message_text}')

        except:
            pass
    else:
        pass
    # Reset the state


@dp.callback_query_handler(lambda call: 'answerto_' in call.data)
async def response_to_user(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    support__on = insup_on(chat_id)


    _, operator_id = call.data.split('_')
    await UserState.waiting_for_message_from_operator.set()

    #Update data in FSMContext



    await bot.send_message(chat_id, f'Напишите ответ оператору',reply_markup=btn_from_coonect_tomain())


@dp.message_handler(state=UserState.waiting_for_message_from_operator, content_types=ContentTypes.TEXT)
async def obtain_message_from_user(message: Message, state: FSMContext):
    chat_id = message.chat.id
    check_session = get_endses(chat_id)
    # Get the original user ID from the state

    if message.text == 'На главную':
        off_sup = suppro__off(chat_id)
        await state.finish()
        await tomain(message)
    data = await state.get_data()
    original_user_id = data.get("original_message_id")


    # Do something with the obtained message from the user
    obtained_message_text = message.text

    if check_session == 'no':

        if obtained_message_text != 'На главную':



            iduoper = get_con_id_user(chat_id)
            await bot.send_message(iduoper, obtained_message_text)



            # Reset the state
        else:
            pass
    else:
        pass



@dp.message_handler(lambda message: 'На главную' in message.text)
async def tomain(message: Message):
    chat_id = message.chat.id
    message_id = message.message_id
    ses_stat = stat_end_stat(chat_id)
    await bot.delete_message(chat_id=chat_id,message_id=message_id)
    if ses_stat == 'yes':
        await message.answer('Благодарим за использование нашего сервиса',reply_markup=ReplyKeyboardRemove())
    if ses_stat == 'no':
        await message.answer('В скором времени с вами свяжеться наш оператор',reply_markup=ReplyKeyboardRemove())
    await message.answer('Выберите направление', reply_markup=inl_but_for_user())

@dp.message_handler(lambda message: 'Завершить сессию' in message.text)
async def end_ses(message: Message):
    chat_id = message.chat.id
    message_id = message.message_id
    await bot.send_message(chat_id, 'Сессия закончено', parse_mode=ParseMode.MARKDOWN,reply_markup=ReplyKeyboardRemove())

    update__busy_status = from_busy_to_free(chat_id)
    user_id = get_user_conid(chat_id)
    await bot.send_message(user_id,'Оператор завершил с вами связь ,для обратного подключение с оператором перейдите в главное меню')
    close_ses = close_session(user_id)
    clear = clear_user_conid(user_id)
    update_insup = oper_update(chat_id)
    off_firstmsg(chat_id)



#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------





dp.middleware.setup(LoggingMiddleware())




executor.start_polling(dispatcher=dp)
