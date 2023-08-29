
import sqlite3 as lite

from random import randint
import datetime


class DatabaseManagerBank(object):
    """Класс описывающий методы взаимодействия с Базой данных"""
    

    def __init__(self,  path): #-> object:
        #self.dbname = dbname
        self.conn = lite.connect(path, check_same_thread=False)
        self.conn.execute("CREATE TABLE IF NOT EXISTS users(`id` INTEGER UNIQUE, `role` TEXT, `name` TEXT, 'phone' INT, 'balance' INT, 'comment' TEXT)")
        self.conn.commit()

    def new_user(self, id):
        try:
            stmt = f'INSERT OR IGNORE INTO users(id) VALUES ({id})'
            self.conn.execute(stmt)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE new_user", e)
            self.conn.close()
        else:
            self.conn.commit()


    def get_user(self, id):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT * FROM users WHERE id = {id}'
            cur.execute(stmt)
            return cur.fetchall()[0]
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE new_user", e)
            self.conn.close()
            

    def get_name_holders(self,t):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT DISTINCT holder_name, user_id FROM wallets WHERE type = {t}'
            cur.execute(stmt)
            
            return cur.fetchall()
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get name hold", e)
            self.conn.close()


    def get_walets(self,id,t):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT * FROM wallets WHERE type = {t} AND user_id= {id}'
            cur.execute(stmt)
            
            return cur.fetchall()
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_walets", e)
            self.conn.close()


    def get_lk_wallet(self, id):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT * FROM wallets WHERE id= {id}'
            cur.execute(stmt) 
            return cur.fetchall()[0]
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_lk_wallet", e)
            self.conn.close()


    def get_lk_wallet_HB(self, id, bank):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT * FROM wallets WHERE user_id= {id} AND bank_id = {bank}'
            cur.execute(stmt) 
            return cur.fetchall()[0]
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_lk_wallet", e)
            self.conn.close()


    def get_wallets_from_bank(self, bank):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT * FROM wallets WHERE bank_id = {bank}'
            cur.execute(stmt) 
            return cur.fetchall()
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_lk_wallet", e)
            self.conn.close()

    def get_clients_list(self,):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT name, id FROM clients'
            cur.execute(stmt) 
            return cur.fetchall()
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_clients_list", e)
            self.conn.close()


    def get_client_info(self, id):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT * FROM clients WHERE id= {id}'
            cur.execute(stmt) 
            return cur.fetchall()
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_client_info", e)
            self.conn.close()

    def get_banks_list(self, t):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT name, id FROM banks WHERE type= {t}'
            cur.execute(stmt) 
            return cur.fetchall()
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_banks_list", e)
            self.conn.close()


    def get_pp_list(self):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT * FROM orders'
            cur.execute(stmt) 
            return cur.fetchall()
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_banks_list", e)
            self.conn.close()


    def get_pp_info_id(self,id):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT * FROM orders WHERE id = {id}'
            cur.execute(stmt) 
            return cur.fetchall()[0]
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_banks_list", e)
            self.conn.close()
    
    def get_full_pp_info(self, client_id, bank_id, holder_id):
        try:
            cur = self.conn.cursor()
            stmt = f'SELECT * FROM clients WHERE id= {client_id}'
            cur.execute(stmt) 
            client = cur.fetchall()[0]
        
            stmt = f'SELECT bank, holder_name, id, balance FROM wallets WHERE bank_id= {bank_id} AND user_id= {holder_id}'
            cur.execute(stmt) 
            wallet = cur.fetchall()[0]

            return list(client), list(wallet)

        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_banks_list", e)
            self.conn.close()


    def add_new_order(self, o, sum_client, sum_holder, type):
        try:
            date = datetime.date.today()
            date_string = date.strftime("%d.%m.%y")
            cur = self.conn.cursor()
            stmt = f'''INSERT OR IGNORE INTO orders
            (date, number, client_name, holder_name, bank_name,sum,tariff, add_tariff, tax, total, close_sum, close_date,client_id, holder_id, bank_id, wallet_id) 
            VALUES ("{o[1]}", "{o[2]}", "{o[3]}", "{o[4]}", "{o[5]}", "{o[6]}", "{o[7]}", "{o[8]}", "{o[9]}", "{o[10]}", "{o[11]}", "{o[12]}", "{o[13]}", "{o[14]}", "{o[15]}", "{o[16]}" )'''
            self.conn.execute(stmt )
            if type == "order":
                stmt2 = f"UPDATE clients SET balance = balance - {sum_client} WHERE id = {o[13]}"
                cur.execute(stmt2)
                stmt5 = f"UPDATE wallets SET share = share - {o[9]} WHERE id = {o[16]}"
                cur.execute(stmt5)
                stmt6 = f'INSERT INTO transactions(date, type, sender, sum_out, sum_in, recipient ) VALUES ("{date_string}", "share", "{o[2]}", 0, "{o[9]}","{o[14]}")'
                self.conn.execute(stmt6)
            elif type == "transit":
                stmt2 = f"UPDATE wallets SET balance = balance - {sum_client} WHERE id = {o[13]}"
                cur.execute(stmt2)

            stmt3 = f"UPDATE wallets SET balance = balance + {sum_holder} WHERE id = {o[16]}"
            cur.execute(stmt3)
            stmt4 = f'INSERT INTO transactions(date, type, sender, sum_out, sum_in, recipient ) VALUES ("{date_string}", "{type}", "{o[13]}", "{sum_client}", "{sum_holder}","{o[16]}")'
            self.conn.execute(stmt4)

            
            #stmt6 = f"UPDATE wallets SET balance = balance + {sum_holder - sum_client} WHERE id = {o[16]}"
            #cur.execute(stmt6)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE new_order", e)
            self.conn.close()
            return 0
        else:
            self.conn.commit()
            return 1


    def add_new_transfer(self, from_id, to_id, sum, type):
        try:
            date = datetime.date.today()
            date_string = date.strftime("%d.%m.%y")
            cur = self.conn.cursor()
            stmt2 = f"UPDATE wallets SET balance = balance - {sum} WHERE id = {from_id}"
            cur.execute(stmt2)
            stmt3 = f"UPDATE wallets SET balance = balance + {sum} WHERE id = {to_id}"
            cur.execute(stmt3)
            stmt4 = f'INSERT INTO transactions(date, type, sender, sum_out, sum_in, recipient) VALUES ("{date_string}", "{type}", "{from_id}", "{sum}", "{sum}","{to_id}")'
            self.conn.execute(stmt4)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE add_transfer", e)
            self.conn.close()
        else:
            self.conn.commit()


    """def add_new_transferfis(self, from_id, to_id, sum):
        try:
            date = datetime.date.today()
            date_string = date.strftime("%d.%m.%y")
            cur = self.conn.cursor()
            stmt2 = f"UPDATE wallets SET balance = balance - {sum} WHERE id = {from_id}"
            cur.execute(stmt2)
            stmt3 = f"UPDATE wallets SET balance = balance + {sum} WHERE id = {to_id}"
            cur.execute(stmt3)
            stmt4 = f'INSERT INTO transactions(date, type, sender, sum_out, sum_in, recipient) VALUES ("{date_string}", "transfer", "{from_id}", "{sum}", "{sum}","{to_id}")'
            self.conn.execute(stmt4)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE add_transfer", e)
            self.conn.close()
        else:
            self.conn.commit()"""


    def add_new_cash_task(self, date, type, holder_name, bank_name, sum, wallet_id, bank_id):
        try:
            stmt4 = f'INSERT INTO withdrawings (date, type, holder_name, bank_name, sum, wallet_id, bank_id) VALUES ("{date}", "{type}", "{holder_name}", "{bank_name}", "{sum}","{wallet_id}", "{bank_id}")'
            self.conn.execute(stmt4)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE add_transfer", e)
            self.conn.close()
        else:
            self.conn.commit()



    def add_new_pushchases(self, sum, id):
        try:
            date = datetime.date.today()
            date_string = date.strftime("%d.%m.%y")
            cur = self.conn.cursor()
            stmt2 = f"UPDATE wallets SET balance = balance - {sum} WHERE id = {id}"
            cur.execute(stmt2)
            stmt4 = f'INSERT INTO pushchases (date, wallet_id, sum) VALUES ("{date_string}", "{id}", "{sum}")'
            self.conn.execute(stmt4)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE add_transfer", e)
            self.conn.close()
        else:
            self.conn.commit()


    def add_new_payment(self, client_name, holder_name, bank_name, sum, client_id, wallet_id, type ):
        try:
            date = datetime.date.today()
            date_string = date.strftime("%d.%m.%y")
            cur = self.conn.cursor()
            stmt = f"UPDATE clients SET balance = balance + {sum} WHERE id = {client_id}"
            cur.execute(stmt)
            stmt2 = f"UPDATE wallets SET balance = balance - {sum} WHERE id = {wallet_id}"
            cur.execute(stmt2)
            stmt4 = f'INSERT INTO payments (date,client_name, holder_name, bank_name, sum, client_id, wallet_id) VALUES ("{date_string}", "{client_name}","{holder_name}","{bank_name}", "{sum}","{client_id}","{wallet_id}")'
            self.conn.execute(stmt4)
            stmt5 = f'INSERT INTO transactions(date, type, sender, sum_out, sum_in, recipient) VALUES ("{date_string}", "{type}", "{wallet_id}", "{sum}", "{sum}","{client_id}")'
            self.conn.execute(stmt5)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE add_payment", e)
            self.conn.close()
        else:
            self.conn.commit()


    def get_ip_holders(self,):
        try:
                cur = self.conn.cursor()
                stmt = f'SELECT * FROM users WHERE id = {id}'
                cur.execute(stmt)
                return cur.fetchall()[0]
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE new_user", e)
            self.conn.close()

    def update_order_status(self,id,status):
        try:
            cur = self.conn.cursor()
            stmt2 = f"UPDATE orders SET status = '{status}' WHERE id = {id}"
            cur.execute(stmt2)
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE update_order_status", e)
            self.conn.close()
        else:
            self.conn.commit()


    def get_cash_list(self, status):
        try:
            cur = self.conn.cursor()
            stmt = f"SELECT * FROM withdrawings WHERE status = 'task' "
            cur.execute(stmt) 
            return cur.fetchall()
        except (lite.OperationalError, lite.ProgrammingError) as e:
            print("ERROR DATABASE get_banks_list", e)
            self.conn.close()

"""


    def new_wallet(self, id, number, token):
        try:
            stmt = f'SELECT * FROM users WHERE id = {id}'
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
        

    def get_number(self,id):
        stmt = f'SELECT number FROM user WHERE id = {id}'
        cur = self.conn.cursor()
        cur.execute(stmt)
        return cur.fetchone()[0]

    def get_token(self, id, number):
        stmt = f'SELECT token FROM "{id}" WHERE number = {number}'
        cur = self.conn.cursor()
        cur.execute(stmt)
        return cur.fetchone()[0]

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
