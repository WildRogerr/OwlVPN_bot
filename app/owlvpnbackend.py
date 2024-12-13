import sqlite3
import subprocess
from datetime import date, datetime, timedelta

class database():

    def adduser(self, userdata):
        userid = userdata[0]
        firstname = userdata[1]
        lastname = userdata[2]
        username = userdata[3]
        promo = 0
        pay_day = 0
        left_days = 0
        end_day = 0
        active = 0
        banned = 0

        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()

        cur.execute(f'SELECT client_id FROM botowluserskz WHERE userid = ? OR username = ?',
                    (userid,username))
        client_check = cur.fetchone()
        if client_check:
            cur.execute(f'SELECT active FROM botowluserskz WHERE username = ? OR userid = ?',(username,userid))
            client_active_check = cur.fetchone()

            cur.execute(f'SELECT userid FROM botowluserskz WHERE username = ? OR userid = ?',(username,userid))
            client_userid_check = cur.fetchone()      

            cur.execute(f'SELECT tariff FROM botowluserskz WHERE username = ? OR userid = ?',(username,userid))
            client_tariff_check = cur.fetchone() 

            if client_active_check[0] == 1 and not client_userid_check:
                cur.execute(f'UPDATE botowluserskz SET userid = ?, firstname = ?, lastname = ?, username = ?, pay_day = ?, left_days = ?, end_day = ?, banned = ? WHERE client_id = ?)',
                            (userid,firstname,lastname,username,pay_day,left_days,end_day,banned,client_check[0]))
                conn.commit()
                conn.close()
                return 1
            
            elif client_active_check[0] == 1 and client_userid_check:
                cur.execute(f'UPDATE botowluserskz SET username = ? WHERE userid = ?',(username,client_userid_check[0]))
                conn.commit()
                conn.close()
                return 2
            
            elif client_active_check[0] == 0 and client_tariff_check:
                cur.execute(f'UPDATE botowluserskz SET username = ? WHERE userid = ?',(username,client_userid_check[0]))
                conn.commit()
                conn.close()
                return 3 
            
            elif client_active_check == 0 and not client_tariff_check:
                cur.execute(f'UPDATE botowluserskz SET username = ? WHERE userid = ?',(username,client_userid_check[0]))
                conn.commit()
                conn.close()
                return 4            
            
        else:
            cur.execute(f'''INSERT INTO botowluserskz(userid,firstname,lastname,username,promo,pay_day,left_days,end_day,active,banned)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (userid,firstname,lastname,username,promo,pay_day,left_days,end_day,active,banned))
            conn.commit()
            cur.execute(f'SELECT client_id FROM botowluserskz WHERE username = ?',(username,))
            client_id = cur.fetchone()
            client_name = f'client_owl_{client_id[0]}.{username}'
            cur.execute(f'UPDATE botowluserskz SET client_name = ? WHERE client_id = ?', (client_name,client_id[0]))
            conn.commit()
            conn.close()
            return 0        

    def getusers(self):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT userid FROM botowluserskz')
        user_ids = []
        row = cur.fetchone()
        if row:
            for id in row:
                user_ids.append(id)
        conn.close()
        return user_ids   
    
    def get_client_name(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT client_name FROM botowluserskz WHERE userid = ?',(userid,))
        name = cur.fetchone()
        client_name = name[0] if name else None
        conn.close()
        return client_name
    
    def get_first_last_name(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT firstname FROM botowluserskz WHERE userid = ?',(userid,))
        fname = cur.fetchone()
        firstname = fname[0] if fname else None
        cur.execute(f'SELECT lastname FROM botowluserskz WHERE userid = ?',(userid,))
        lname = cur.fetchone()
        lastname = lname[0] if lname else None
        conn.close()
        return f'{firstname} {lastname}'
    
    def get_username(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT username FROM botowluserskz WHERE userid = ?',(userid,))
        uname = cur.fetchone()
        username = uname[0] if uname else None
        conn.close()
        return username
   
    def addtariff(self,tariff,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'UPDATE botowluserskz SET tariff = ? WHERE userid = ?',(tariff,userid))
        if tariff == 4 or tariff == 5:
            cur.execute(f'UPDATE botowluserskz SET promo = 1 WHERE userid = ?',(userid,))
        conn.commit()
        conn.close()

    def gettariff(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT tariff FROM botowluserskz WHERE userid = ?',(userid,))
        number = cur.fetchone()
        tariff = number[0] if number else None
        conn.close()
        return tariff
    
    def getpromo(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT promo FROM botowluserskz WHERE userid = ?',(userid,))
        number = cur.fetchone()
        promo = number[0]
        conn.close()
        return promo
    
    def server_accounts(self,userid,code):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        if code == 1:
            cur.execute(f'UPDATE botowluserskz SET server_account1 = 1 WHERE userid = ?',(userid,))
        elif code == 2:
            cur.execute(f'UPDATE botowluserskz SET server_account2 = 1 WHERE userid = ?',(userid,))
        elif code == 3:
            cur.execute(f'UPDATE botowluserskz SET server_account3 = 1 WHERE userid = ?',(userid,))
        elif code == 4:
            cur.execute(f'UPDATE botowluserskz SET server_account1 = 0 WHERE userid = ?',(userid,))
        elif code == 5:
            cur.execute(f'UPDATE botowluserskz SET server_account2 = 0 WHERE userid = ?',(userid,))
        elif code == 6:
            cur.execute(f'UPDATE botowluserskz SET server_account3 = 0 WHERE userid = ?',(userid,))
        elif code == 7:
            cur.execute(f'UPDATE botowluserskz SET server_account1 = 2 WHERE userid = ?',(userid,))
        elif code == 8:
            cur.execute(f'UPDATE botowluserskz SET server_account2 = 2 WHERE userid = ?',(userid,))
        elif code == 9:
            cur.execute(f'UPDATE botowluserskz SET server_account2 = 2 WHERE userid = ?',(userid,))
        conn.commit()
        conn.close()

    def get_server_account1(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT server_account1 FROM botowluserskz WHERE userid = ?',(userid,))
        value = cur.fetchone()
        try: server_account1 = value[0]
        except:
            server_account1 = False
        conn.close()
        return server_account1

    def get_server_account2(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT server_account2 FROM botowluserskz WHERE userid = ?',(userid,))
        value = cur.fetchone()
        try: server_account2 = value[0]
        except:
            server_account2 = False
        conn.close()
        return server_account2

    def get_server_account3(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT server_account3 FROM botowluserskz WHERE userid = ?',(userid,))
        value = cur.fetchone()
        try: server_account3 = value[0]
        except:
            server_account3 = False
        conn.close()
        return server_account3
    
    def active_status(self,userid,code):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        status = self.get_active_status(userid)
        if code == True:
            if status == 0:
                cur.execute(f'UPDATE botowluserskz SET active = 1 WHERE userid = ?',(userid,))
            else:
                pass
        else:
            cur.execute(f'UPDATE botowluserskz SET active = 0 WHERE userid = ?',(userid,))
        conn.commit()
        conn.close()

    def get_active_status(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT active FROM botowluserskz WHERE userid = ?',(userid,))
        client_active_check = cur.fetchone()
        active_status = client_active_check[0] if client_active_check else None
        conn.close()
        return active_status
    
    def add_pay_day(self,userid):
        today = date.today()
        day_of_month = today.day + 1
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        if day_of_month == 29 or day_of_month == 30 or day_of_month == 31:
            cur.execute(f'UPDATE botowluserskz SET pay_day = 1 WHERE userid = ?',(userid,))
        else:
            cur.execute(f'UPDATE botowluserskz SET pay_day = ? WHERE userid = ?',(day_of_month,userid))
        conn.commit()
        conn.close()

    def get_day_of_month(self):
        today = date.today()
        day_of_month = today.day
        return day_of_month
    
    def get_hour(self):
        now = datetime.now()
        hour = now.strftime("%H")
        return hour
    
    def three_days_counter(self):
        start_time = date.today()
        end_time = start_time + timedelta(days=3)
        end_day = end_time.day
        return end_day
    
    def get_pay_day(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT pay_day FROM botowluserskz WHERE userid = ?',(userid,))
        day = cur.fetchone()
        pay_day = day[0]
        conn.close()
        return pay_day
    
    def set_left_days(self,userid,code):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        if code == 1:
            cur.execute(f'UPDATE botowluserskz SET left_days = 1 WHERE userid = ?',(userid,))
        elif code == 0:
            cur.execute(f'UPDATE botowluserskz SET left_days = 0 WHERE userid = ?',(userid,))
        conn.commit()
        conn.close()

    def get_left_days(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT left_days FROM botowluserskz WHERE userid = ?',(userid,))
        days = cur.fetchone()
        left_days = days[0]
        conn.close()
        return left_days
    
    def set_end_day(self,userid,end_day):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'UPDATE botowluserskz SET end_day = ? WHERE userid = ?',(end_day,userid))
        conn.commit()
        conn.close()

    def get_end_day(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT end_day FROM botowluserskz WHERE userid = ?',(userid,))
        day = cur.fetchone()
        end_day = day[0]
        conn.close()
        return end_day
                
    def set_next_month_0(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'UPDATE botowluserskz SET next_month = 0 WHERE userid = ?',(userid,))
        conn.commit()
        conn.close()
    
    def get_next_month(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT next_month FROM botowluserskz WHERE userid = ?',(userid,))
        value = cur.fetchone()
        next_month_value = value[0] if value else None
        conn.close()
        return next_month_value
    
    def next_month(self,userid):
        next_month_value = self.get_next_month(userid)
        left_days = self.get_left_days(userid)
        active_status = self.get_active_status(userid)
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        if next_month_value == 0 and left_days == 0 and active_status == 1:
            cur.execute(f'UPDATE botowluserskz SET next_month = 1 WHERE userid = ?',(userid,))
            code = 2
        else:
            code = 1
        conn.commit()
        conn.close()
        return code
    
    def set_ban(self,userid,code):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'UPDATE botowluserskz SET banned = ? WHERE userid = ?',(code,userid))
        conn.commit()
        conn.close()

    def get_ban(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT banned FROM botowluserskz WHERE userid = ?',(userid,))
        value = cur.fetchone()
        ban = value[0] if value else None
        conn.close()
        return ban



class managebot():

    def manage_server_accounts(self,userid,client_name,tariff):
        databasemanager = database()
        server_account1 = databasemanager.get_server_account1(userid)
        server_account2 = databasemanager.get_server_account2(userid)
        server_account3 = databasemanager.get_server_account3(userid)
        if tariff == 1 and server_account1 == False and server_account2 == False and server_account3 == False:
            self.create_server_account(client_name,value=None)
            self.stop_user(client_name,value=None)
        elif (tariff == 2 or tariff == 4) and server_account1 == False and server_account2 == False and server_account3 == False:
            self.create_server_account(client_name,value=None)
            self.create_server_account(client_name,value=2)
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
        elif (tariff == 3 or tariff == 5) and server_account1 == False and server_account2 == False and server_account3 == False:
            self.create_server_account(client_name,value=None)
            self.create_server_account(client_name,value=2)
            self.create_server_account(client_name,value=3)
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
            self.stop_user(client_name,value=3)
        elif tariff == 1 and server_account1 == 1 and server_account2 == False and server_account3 == False:
            return
        elif (tariff == 2 or tariff == 4) and server_account1 == 1 and server_account2 == False and server_account3 == False:
            self.create_server_account(client_name,value=2)
            self.stop_user(client_name,value=2)
        elif (tariff == 3 or tariff == 5) and server_account1 == 1 and server_account2 == False and server_account3 == False:
            self.create_server_account(client_name,value=2)
            self.create_server_account(client_name,value=3)
            self.stop_user(client_name,value=2)
            self.stop_user(client_name,value=3)
        elif tariff == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == False:
            self.stop_user(client_name,value=2)
            databasemanager.server_accounts(userid,code=5)
        elif (tariff == 2 or tariff == 4) and server_account1 == 1 and server_account2 == 1 and server_account3 == False:
            return
        elif (tariff == 3 or tariff == 5) and server_account1 == 1 and server_account2 == 1 and server_account3 == False:
            self.create_server_account(client_name,value=3)
            self.stop_user(client_name,value=3)
        elif tariff == 1 and server_account1 == 1 and server_account2 == 0 and server_account3 == False:
            return
        elif (tariff == 2 or tariff == 4) and server_account1 == 1 and server_account2 == 0 and server_account3 == False:
            databasemanager.server_accounts(userid,code=2)
        elif (tariff == 3 or tariff == 5) and server_account1 == 1 and server_account2 == 0 and server_account3 == False:
            databasemanager.server_accounts(userid,code=2)
            self.create_server_account(client_name,value=3)
            self.stop_user(client_name,value=3)
        elif (tariff == 1 and server_account1 == 1) and server_account2 == 1 and server_account3 == 1:
            databasemanager.server_accounts(userid,code=5)
            databasemanager.server_accounts(userid,code=6)
        elif (tariff == 2 or tariff == 4) and server_account1 == 1 and server_account2 == 1 and server_account3 == 1:
            databasemanager.server_accounts(userid,code=6)
        elif (tariff == 3 or tariff == 5) and server_account1 == 1 and server_account2 == 1 and server_account3 == 1:
            return
        elif tariff == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == 0:
            databasemanager.server_accounts(userid,code=5)
        elif (tariff == 2 or tariff == 4) and server_account1 == 1 and server_account2 == 1 and server_account3 == 0:
            return
        elif (tariff == 3 or tariff == 5) and server_account1 == 1 and server_account2 == 1 and server_account3 == 0:
            databasemanager.server_accounts(userid,code=3)
        elif tariff == 1 and server_account1 == 1 and server_account2 == 0 and server_account3 == 0:
            return
        elif (tariff == 2 or tariff == 4) and server_account1 == 1 and server_account2 == 0 and server_account3 == 0:
            databasemanager.server_accounts(userid,code=2)
        elif (tariff == 3 or tariff == 5) and server_account1 == 1 and server_account2 == 0 and server_account3 == 0:
            databasemanager.server_accounts(userid,code=2)
            databasemanager.server_accounts(userid,code=3)

    def create_server_account(self,client_name,value):
        command = f'source /home/vpnserver/awgm && generate_config "{client_name}{value}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)
        command = f'source /home/vpnserver/awgm && copy_config_files "{client_name}{value}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)
    
    def stop_user(self,client_name,value):
        command = f'source /home/vpnserver/awgm && stop_config "{client_name}{value}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)

    def start_user(self,client_name,value):
        command = f'source /home/vpnserver/awgm && start_config "{client_name}{value}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)

    def active_server_switch(self,userid,client_name,old_active_status):
        databasemanager = database()
        server_account1 = databasemanager.get_server_account1(userid)
        server_account2 = databasemanager.get_server_account2(userid)
        server_account3 = databasemanager.get_server_account3(userid)
        activestatus = databasemanager.get_active_status(userid)
        if activestatus == 1 and server_account1 == 1 and (server_account2 == False or server_account2 == 2) and (server_account3 == False or server_account3 == 2)  and old_active_status == 0:
            self.start_user(client_name,value=None)
        elif activestatus == 1 and server_account1 == 1 and (server_account2 == False or server_account2 == 2) and (server_account3 == False or server_account3 == 2) and old_active_status == 1:
            pass
        elif activestatus == 1 and server_account1 == 1 and server_account2 == 0 and (server_account3 == False or server_account3 == 2)  and old_active_status == 0:
            self.start_user(client_name,value=None)
            self.stop_user(client_name,value=2)
            databasemanager.server_accounts(userid,code=8)
        elif activestatus == 1 and server_account1 == 1 and server_account2 == 0 and (server_account3 == False or server_account3 == 2)  and old_active_status == 1:
            self.stop_user(client_name,value=2)
            databasemanager.server_accounts(userid,code=8)
        elif activestatus == 1 and server_account1 == 1 and server_account2 == 0 and server_account3 == 0 and old_active_status == 0:
            self.start_user(client_name,value=None)
            self.stop_user(client_name,value=2)
            self.stop_user(client_name,value=3)
            databasemanager.server_accounts(userid,code=8)
            databasemanager.server_accounts(userid,code=9)
        elif activestatus == 1 and server_account1 == 1 and server_account2 == 0 and server_account3 == 0 and old_active_status == 1:
            self.stop_user(client_name,value=2)
            self.stop_user(client_name,value=3)
            databasemanager.server_accounts(userid,code=8)
            databasemanager.server_accounts(userid,code=9)
        elif activestatus == 1 and server_account1 == 1 and server_account2 == 1 and (server_account3 == False or server_account3 == 2) and old_active_status == 0:
            self.start_user(client_name,value=None)
            self.start_user(client_name,value=2)
        elif activestatus == 1 and server_account1 == 1 and server_account2 == 1 and (server_account3 == False or server_account3 == 2) and old_active_status == 1:
            pass
        elif activestatus == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == 0 and old_active_status == 0:
            self.start_user(client_name,value=None)
            self.start_user(client_name,value=2)
            self.stop_user(client_name,value=3)
            databasemanager.server_accounts(userid,code=9)
        elif activestatus == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == 0 and old_active_status == 1:
            self.stop_user(client_name,value=3)
            databasemanager.server_accounts(userid,code=9)
        elif activestatus == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == 1 and old_active_status == 0:
            self.start_user(client_name,value=None)
            self.start_user(client_name,value=2)
            self.start_user(client_name,value=3)
        elif activestatus == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == 1 and old_active_status == 1:
            pass
        elif activestatus == 0 and server_account1 == 1 and (server_account2 == False or server_account2 == 2) and (server_account3 == False or server_account3 == 2) and old_active_status == 1:
            self.stop_user(client_name,value=None)
        elif activestatus == 0 and server_account1 == 1 and server_account2 == 0 and (server_account3 == False or server_account3 == 2) and old_active_status == 1:
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
            databasemanager.server_accounts(userid,code=8)
        elif activestatus == 0 and server_account1 == 1 and server_account2 == 0 and server_account3 == 0 and old_active_status == 1:
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
            self.stop_user(client_name,value=3)
            databasemanager.server_accounts(userid,code=8)
            databasemanager.server_accounts(userid,code=9)
        elif activestatus == 0 and server_account1 == 1 and server_account2 == 1 and (server_account3 == False or server_account3 == 2) and old_active_status == 1:
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
        elif activestatus == 0 and server_account1 == 1 and server_account2 == 1 and server_account3 == 0 and old_active_status == 1:
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
            self.stop_user(client_name,value=3)
            databasemanager.server_accounts(userid,code=9)
        elif activestatus == 0 and server_account1 == 1 and server_account2 == 1 and server_account3 == 1 and old_active_status == 1:
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
            self.stop_user(client_name,value=3)
        
    
    
    class Logger:

        def log(self, data):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not isinstance(data, str):
                data = str(data)
            try:
                with open('./log.txt', 'a', encoding="utf-8") as file:
                    file.write(f'{now}: {data}\n')
            except Exception as e:
                print(f"Ошибка записи лога: {e}")