
import sqlite3 as lite

from random import randint
from time import time


class DatabaseManagerBank(object):
    """Класс описывающий методы взаимодействия с Базой данных"""

    def __init__(self,  dbname: object = ".data/storage/banking_db.db") -> object:
        self.dbname = dbname
        self.conn = lite.connect(dbname, check_same_thread=False)
        self.conn.execute("CREATE TABLE IF NOT EXISTS user(`id` INTEGER UNIQUE, `number` TEXT, `recipient` TEXT, 'card' TEXT)")
        self.conn.commit()

    def new_user(self, id):
        try:
            stmt = f'CREATE TABLE IF NOT EXISTS "{id}"(`number` INTEGER, `token` TEXT)'
            self.conn.execute(stmt)
            stmt = f'INSERT OR IGNORE INTO user(id) VALUES ({id})'
            self.conn.execute(stmt)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE new_user", e)
            self.conn.close()
        else:
            self.conn.commit()

    def new_wallet(self, id, number, token):
        try:
            stmt = f'INSERT INTO "{id}"(number, token)VALUES(?,?)'
            args = (number, token)
            self.conn.execute(stmt, args)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE new_user", e)
            self.conn.close()
        else:
            self.conn.commit()

    def update_number(self, id, number):
        try:
            stmt = f'UPDATE user SET number = {number} where id = {id}'
            self.conn.execute(stmt)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE new_user", e)
            self.conn.close()
        else:
            self.conn.commit()

    """def get_number(self,id):
        stmt = f'SELECT number FROM user WHERE id = {id}'
        cur = self.conn.cursor()
        cur.execute(stmt)
        return cur.fetchone()[0]

    def get_token(self, id, number):
        stmt = f'SELECT token FROM "{id}" WHERE number = {number}'
        cur = self.conn.cursor()
        cur.execute(stmt)
        return cur.fetchone()[0]"""

    def get_wallet(self,id):
        cur = self.conn.cursor()
        cur.execute(f'SELECT number FROM user WHERE id = {id}')
        number = cur.fetchone()[0]
        cur.execute(f'SELECT token FROM "{id}" WHERE number = {number}')
        token = cur.fetchone()[0]
        return number, token

    def get_wallets(self, id):
        stmt = f'SELECT * FROM "{id}"'
        cur = self.conn.cursor()
        cur.execute(stmt)
        return cur.fetchall()

    def get_card(self,id):
        cur = self.conn.cursor()
        cur.execute(f'SELECT card FROM user WHERE id = {id}')
        return cur.fetchone()[0]
"""
class DatabaseManager(object):

    def __init__(self, path):
        self.conn = lite.connect(path)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.query('CREATE TABLE IF NOT EXISTS products (idx text, title text, body text, photo blob, price int, tag text)')
        self.query('CREATE TABLE IF NOT EXISTS orders (cid int, usr_name text, usr_address text, products text)')
        self.query('CREATE TABLE IF NOT EXISTS cart (cid int, idx text, quantity int)')
        self.query('CREATE TABLE IF NOT EXISTS categories (idx text, title text)')
        self.query('CREATE TABLE IF NOT EXISTS wallet (cid int, balance real)')
        self.query('CREATE TABLE IF NOT EXISTS questions (cid int, question text)')
        
    def query(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        self.conn.commit()

    def fetchone(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchone()

    def fetchall(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()

    try:
        conn = lite.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}", "@{message.from_user.username}")')
        conn.commit()
    except Exception as e:
        print(e)
        conn = lite.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}")')
        conn.commit()
        """
'''

products: idx text, title text, body text, photo blob, price int, tag text

orders: cid int, usr_name text, usr_address text, products text

cart: cid int, idx text, quantity int ==> product_idx

categories: idx text, title text

wallet: cid int, balance real

questions: cid int, question text


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет, я эхо-бот, напиши мне что-нибудь!')
    try:
        conn = lite.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}", "@{message.from_user.username}")')
        conn.commit()
    except Exception as e:
        print(e)
        conn = lite.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}")')
        conn.commit()

@dp.message_handler(commands=['profile'])
async def get_profile(msg: types.Message):
    conn = lite.connect('data.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users WHERE user_id = "{msg.from_user.id}"')
    result = cur.fetchall()
    print(result)
    await bot.send_message(msg.from_user.id, f'ID = {list(result[0])[0]}\nUserName = {[list(result[0])[1]][0]}')


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)
'''
