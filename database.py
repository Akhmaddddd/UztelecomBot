import psycopg2


def create_users_table():
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()

    cursor.execute('''
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    CREATE TABLE IF NOT EXISTS users(
        user_id uuid DEFAULT uuid_generate_v4()  PRIMARY KEY ,
        telegram_username VARCHAR(100),
        telegram_id BIGINT NOT NULL UNIQUE,        
        full_name VARCHAR(200),
        status TEXT DEFAULT 'user',
        user_page Text,
        operator_page Text,
        created_at timestamp DEFAULT now(),
        operator_connect_id BIGINT,
        user_connect_id BIGINT,
        busy_status Text default 'free',
        time_of_free_oper timestamp DEFAULT now(),
        in_support text default 'no',
        end_session text default 'no',
        first_message text default 'no'
        
    );
    ''')
    database.commit()
    database.close()


create_users_table()

def insert_to_user(chat_id, telegram_username, full_name):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()

    # Fetch the current count of users to determine the page number
    # cursor.execute('''SELECT COUNT(*) FROM users where status != 'admin' and status != 'operator' ''')
    # user_count = cursor.fetchone()[0]

    # Calculate the page number based on the user count
    # page_number = (user_count // 5) + 1

    cursor.execute('''
        INSERT INTO users (telegram_username, telegram_id, full_name)
        VALUES (%s, %s, %s)
    ''', (telegram_username, chat_id, full_name))

    database.commit()
    database.close()


def first_select(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()

    cursor.execute('''
    SELECT * FROM users WHERE telegram_id = %s;
    ''', (chat_id,))
    user = cursor.fetchone()
    database.commit()
    database.close()
    return user


def check_admin(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )
    try:
        cursor = database.cursor()
        cursor.execute('''
        SELECT status FROM users WHERE telegram_id = %s
        ''', (chat_id,))

        admin = cursor.fetchone()
        database.commit()
        database.close()
        return admin[0]
    except:
        pass


def get_all_users():
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    num = 5

    cursor = database.cursor()
    cursor.execute('''
        update users set user_page ='0' where status = 'admin'
        ''')

    cursor.execute('''
        SELECT * FROM  users where status = 'admin'
        ''')
    admin = cursor.fetchone()[5]
    print(admin)

    cursor.execute('''
        SELECT user_id,telegram_username,full_name,user_page FROM users
        WHERE status = 'user'
        ORDER BY created_at desc
        limit 5 offset %s

        ''', (int(admin) * 5,))
    users = cursor.fetchall()

    # cursor.execute('''
    # update users set page = %s where status = 'admin'
    # ''', (str(int(admin) + 1)))

    database.commit()
    database.close()
    return users


def get_next_users():
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
            SELECT * FROM  users where status = 'admin'
            ''')
    admin = cursor.fetchone()[5]
    cursor.execute('''
                update users set user_page = %s where status = 'admin'
                ''', (str(int(admin) + 1),))
    cursor.execute('''
                SELECT * FROM  users where status = 'admin'
                ''')
    admin2 = cursor.fetchone()[5]
    print(admin2)

    cursor.execute('''
            SELECT user_id,telegram_username,full_name FROM users
            WHERE status = 'user'
            ORDER BY created_at desc
            limit 5 offset %s

            ''', (int(admin2) * 5,))

    users = cursor.fetchall()


    database.commit()
    database.close()
    return users

def get_previous_users():
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
        SELECT * FROM  users where status = 'admin'
        ''')
    admin = cursor.fetchone()[5]
    cursor.execute('''
            update users set user_page = %s where status = 'admin'
            ''', (str(int(admin) - 1)))
    cursor.execute('''
            SELECT * FROM  users where status = 'admin'
            ''')
    admin2 = cursor.fetchone()[5]

    cursor.execute('''
        SELECT user_id,telegram_username,full_name FROM users
        WHERE status = 'user'
        ORDER BY created_at desc
        limit 5 offset %s

        ''', (int(admin2) * 5,))
    users = cursor.fetchall()


    database.commit()
    database.close()
    return users




def get_all_operators():
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    num = 5

    cursor = database.cursor()
    cursor.execute('''
    update users set operator_page ='0' where status = 'admin'
    ''')

    cursor.execute('''
    SELECT * FROM  users where status = 'admin'
    ''')
    admin = cursor.fetchone()[6]




    cursor.execute('''
    SELECT user_id,telegram_username,full_name,operator_page FROM users
    WHERE status = 'operator'
    ORDER BY created_at desc
    limit 5 offset %s

    ''',(int(admin) * 5,))
    operators = cursor.fetchall()

    # cursor.execute('''
    # update users set page = %s where status = 'admin'
    # ''', (str(int(admin) + 1)))


    database.commit()
    database.close()
    return operators

def get_next_operators():
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
        SELECT * FROM  users where status = 'admin'
        ''')
    admin = cursor.fetchone()[6]
    cursor.execute('''
            update users set operator_page = %s where status = 'admin'
            ''', (str(int(admin) + 1)))
    cursor.execute('''
            SELECT * FROM  users where status = 'admin'
            ''')
    admin2 = cursor.fetchone()[6]
    print(admin2)
    cursor.execute('''
        SELECT user_id,telegram_username,full_name FROM users
        WHERE status = 'operator'
        ORDER BY created_at desc
        limit 5 offset %s

        ''', (int(admin2) * 5,))
    print(int(admin2) * 5)
    operators = cursor.fetchall()

    print(operators)
    database.commit()
    database.close()
    return operators


def get_previous_operators():
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )



    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM  users where status = 'admin'
    ''')
    admin = cursor.fetchone()[6]
    cursor.execute('''
        update users set operator_page = %s where status = 'admin'
        ''', (str(int(admin) - 1)))
    cursor.execute('''
        SELECT * FROM  users where status = 'admin'
        ''')
    admin2 = cursor.fetchone()[6]



    cursor.execute('''
    SELECT user_id,telegram_username,full_name,operator_page FROM users
    WHERE status = 'operator'
    ORDER BY created_at desc
    limit 5 offset %s

    ''',(int(admin2) * 5,))
    operators = cursor.fetchall()



    print(operators)
    database.commit()
    database.close()
    return operators

def user_info(username):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE telegram_username = %s
    ''', (username,))
    users = cursor.fetchone()
    database.commit()
    database.close()
    return users



def function_of_delete(user_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
            DELETE FROM users WHERE user_id = %s and status = 'user'
            ''', (user_id,))
    database.commit()
    database.close()
    return True



def function_update_to_operator(user_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()


    cursor.execute('''
    UPDATE users SET status='operator' WHERE user_id = %s and status = 'user'
    ''', (user_id,))
    database.commit()
    database.close()
    return True


def function_of_delete_operator(user_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
        DELETE FROM users WHERE user_id = %s and status = 'operator'
        ''', (user_id,))
    database.commit()
    database.close()
    return True


def function_reduce_to_user(user_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()



    cursor.execute('''
        UPDATE users SET status='user'  WHERE user_id = %s and status = 'operator'
        ''', (user_id,))
    database.commit()
    database.close()
    return True





def page_op():
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    select operator_page from users where status = 'admin'
    ''')
    page = cursor.fetchone()[0]

    database.commit()
    database.close()
    return page





def back_button_op(op_page):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
            SELECT user_id,telegram_username,full_name,operator_page FROM users
            WHERE status = 'operator'
            ORDER BY created_at desc
            limit 5 offset %s

            ''', (int(op_page) * 5,))
    operators = cursor.fetchall()
    database.commit()
    database.close()
    return operators


def page_user():
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    select user_page from users where status = 'admin'
    ''')
    page = cursor.fetchone()[0]

    database.commit()
    database.close()
    return page


def back_button_user(user_page):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
                SELECT user_id,telegram_username,full_name,operator_page FROM users
                WHERE status = 'user'
                ORDER BY created_at desc
                limit 5 offset %s

                ''', (int(user_page) * 5,))
    users = cursor.fetchall()
    database.commit()
    database.close()
    return users


def support_id_operator():
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    select telegram_id from users  where status = 'operator' and busy_status = 'free' ORDER BY time_of_free_oper
    ''')

    op=cursor.fetchall()
    suport_ids.clear()
    for i in op:
        suport_ids.append(i[0])
    database.commit()
    database.close()
    return op



suport_ids = []
for i in support_id_operator():

    suport_ids.append(i[0])


def connect_bet(chat_id,user_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    UPDATE users SET  operator_connect_id = %s, user_connect_id = %s where telegram_id = %s
    ''',(chat_id,user_id,chat_id))

    cursor.execute('''
        UPDATE users SET  operator_connect_id = %s where telegram_id = %s
        ''', (chat_id, user_id))

    database.commit()
    database.close()

def busy_oper(operator_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    update users set busy_status = 'busy' where telegram_id = %s
    ''',(operator_id,))
    database.commit()
    database.close()



def get_connect_id(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    select operator_connect_id , user_connect_id from users  where telegram_id = %s and status = 'operator'
    ''',(chat_id,))
    ids= cursor.fetchone()

    database.commit()
    database.close()
    return ids


def get_con_id_user(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
        select operator_connect_id   from users  where telegram_id = %s
        ''', (chat_id,))
    ids = cursor.fetchone()[0]
    database.commit()
    database.close()
    return ids


def from_busy_to_free(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    UPDATE users SET busy_status = 'free', time_of_free_oper = DEFAULT WHERE telegram_id = %s
    ''',(chat_id,))

    cursor.execute('''
        select telegram_id from users  where status = 'operator' and busy_status = 'free' ORDER BY time_of_free_oper
        ''')
    op = cursor.fetchall()

    suport_ids.clear()
    for i in op:
        suport_ids.append(i[0])

    database.commit()
    database.close()


def suppro__off(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    update users set in_support = 'no' where telegram_id = %s
    ''',(chat_id,))
    database.commit()
    database.close()


def insup_on(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
        update users set in_support = 'yes' where telegram_id = %s
        ''', (chat_id,))
    database.commit()
    database.close()



def obtain_insup(id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    select in_support from users where telegram_id = %s
    ''',(id,))
    ind=cursor.fetchone()
    database.commit()
    database.close()
    return ind[0]



def get_user_conid(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    select user_connect_id from users where telegram_id = %s
    ''',(chat_id,))
    ids = cursor.fetchone()
    database.commit()
    database.close()
    return ids[0]


def clear_user_conid(user_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    UPDATE users
SET operator_connect_id = NULL
WHERE telegram_id = %s;
    ''',(user_id,))
    database.commit()
    database.close()

def close_session(user_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    update users set end_session = 'yes' where telegram_id = %s
    ''',(user_id,))
    database.commit()
    database.close()

def get_endses(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    select end_session from users where telegram_id = %s
    ''',(chat_id,))
    ses = cursor.fetchone()
    database.commit()
    database.close()
    return ses[0]

def endsession_on(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    update users set end_session = 'no' where telegram_id = %s
    ''',(chat_id,))
    database.commit()
    database.close()


def oper_update(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    update users set in_support = 'no' where telegram_id = %s
    ''',(chat_id,))
    database.commit()
    database.close()


def obtain_insup_status(operator_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    select in_support from users where telegram_id = %s
    ''',(operator_id,))
    status = cursor.fetchone()
    database.commit()
    database.close()
    return status[0]


def set_def(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    update users set operator_connect_id = default ,user_connect_id = default , busy_status = default , in_support = default , end_session = default
    where telegram_id = %s
    ''',(chat_id,))
    database.commit()
    database.close()

def firts_msg(operator_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    select first_message from users where telegram_id = %s
    ''',(operator_id,))
    msg=cursor.fetchone()
    database.commit()
    database.close()
    return msg[0]


def upfate_msg(operator_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    update users set first_message = 'yes' where telegram_id = %s
    ''',(operator_id,))
    database.commit()
    database.close()

def off_firstmsg(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
        update users set first_message = 'no' where telegram_id = %s
        ''', (chat_id,))
    database.commit()
    database.close()
 # DB_HOST =  tiny.db.elephantsql.com            # your database Host
# DB_PORT =  5432              # your database Port
# DB_PASSWORD= RWERgH6IlhGEPMFolGnNADwRjNYfSId- # your database Password
# DB_USERNAME=  uqmpygjx          # your database UserName
# DATABASE=  uqmpygjx
def stat_end_stat(chat_id):
    database = psycopg2.connect(
        dbname='uqmpygjx',
        host='tiny.db.elephantsql.com',
        port='5432',
        user='uqmpygjx',
        password='RWERgH6IlhGEPMFolGnNADwRjNYfSId-'
    )

    cursor = database.cursor()
    cursor.execute('''
    select end_session from users where telegram_id = %s
    ''',(chat_id,))
    ses = cursor.fetchone()
    database.commit()
    database.close()
    return ses[0]