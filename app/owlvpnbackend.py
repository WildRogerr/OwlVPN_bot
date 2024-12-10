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
        next_month = 0
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
                cur.execute(f'UPDATE botowluserskz SET userid = ? firstname = ? lastname = ? username = ? pay_day = ? left_days = ? end_day = ? next_month = ? banned = ? WHERE client_id = ?)',
                            (userid,firstname,lastname,username,pay_day,left_days,end_day,next_month,banned,client_check[0]))
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
            cur.execute(f'''INSERT INTO botowluserskz(userid,firstname,lastname,username,promo,pay_day,left_days,end_day,next_month,active,banned)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (userid,firstname,lastname,username,promo,pay_day,left_days,end_day,next_month,active,banned))
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
   
    def addtariff(self,tariff,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'UPDATE botowluserskz SET tariff = ? WHERE userid = ?',(tariff,userid))
        if tariff == 4 or 5:
            cur.execute(f'UPDATE botowluserskz SET promo = 1 WHERE userid = ?',(userid,))
        conn.commit()
        conn.close()

    def gettariff(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT tariff FROM botowluserskz WHERE userid = ?',(userid,))
        number = cur.fetchone()
        try: 
            tariff = number[0]
        except:
            tariff = None
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
    
    def get_client_name(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT client_name FROM botowluserskz WHERE userid = ?',(userid,))
        name = cur.fetchone()
        client_name = name[0]
        conn.close()
        return client_name
    
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
        if code == True:
            cur.execute(f'UPDATE botowluserskz SET active = 1 WHERE userid = ?',(userid,))
        else:
            cur.execute(f'UPDATE botowluserskz SET active = 0 WHERE userid = ?',(userid,))
        conn.commit()
        conn.close()

    def get_active_status(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT active FROM botowluserskz WHERE userid = ?',(userid,))
        client_active_check = cur.fetchone()
        active_status = client_active_check[0]
        conn.close()
        return active_status
    
    def add_pay_day(self,userid):
        today = date.today()
        day_of_mounth = today.day
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        if day_of_mounth == 29 or 30 or 31:
            cur.execute(f'UPDATE botowluserskz SET pay_day = 1 WHERE userid = ?',(userid,))
        else:
            cur.execute(f'UPDATE botowluserskz SET pay_day = ? WHERE userid = ?',(day_of_mounth,userid))
        conn.commit()
        conn.close()

    def get_day_of_mount():
        today = date.today()
        day_of_mounth = today.day
        return day_of_mounth
    
    def get_hour():
        now = datetime.now()
        hour = now.strftime("%H")
        return hour
    
    def three_days_counter():
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



class managebot():

    def manage_server_accounts(self,userid,client_name,tariff):
        databasemanager = database()
        server_account1 = databasemanager.get_server_account1(userid)
        server_account2 = databasemanager.get_server_account2(userid)
        server_account3 = databasemanager.get_server_account3(userid)
        if tariff == 1 and server_account1 == False and server_account2 == False and server_account3 == False:
            self.create_server_account(client_name,value=None)
            self.stop_user(client_name,value=None)
        elif tariff == 2 or 4 and server_account1 == False and server_account2 == False and server_account3 == False:
            self.create_server_account(client_name,value=None)
            self.create_server_account(client_name,value=2)
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
        elif tariff == 3 or 5 and server_account1 == False and server_account2 == False and server_account3 == False:
            self.create_server_account(client_name,value=None)
            self.create_server_account(client_name,value=2)
            self.create_server_account(client_name,value=3)
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
            self.stop_user(client_name,value=3)
        elif tariff == 1 and server_account1 == 1 and server_account2 == False and server_account3 == False:
            return
        elif tariff == 2 or 4 and server_account1 == 1 and server_account2 == False and server_account3 == False:
            self.create_server_account(client_name,value=2)
            self.stop_user(client_name,value=2)
        elif tariff == 3 or 5 and server_account1 == 1 and server_account2 == False and server_account3 == False:
            self.create_server_account(client_name,value=2)
            self.create_server_account(client_name,value=3)
            self.stop_user(client_name,value=2)
            self.stop_user(client_name,value=3)
        elif tariff == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == False:
            self.stop_user(client_name,value=2)
            databasemanager.server_accounts(userid,code=5)
        elif tariff == 2 or 4 and server_account1 == 1 and server_account2 == 1 and server_account3 == False:
            return
        elif tariff == 3 or 5 and server_account1 == 1 and server_account2 == 1 and server_account3 == False:
            self.create_server_account(client_name,value=3)
            self.stop_user(client_name,value=3)
        elif tariff == 1 and server_account1 == 1 and server_account2 == 0 and server_account3 == False:
            return
        elif tariff == 2 or 4 and server_account1 == 1 and server_account2 == 0 and server_account3 == False:
            databasemanager.server_accounts(userid,code=2)
        elif tariff == 3 or 5 and server_account1 == 1 and server_account2 == 0 and server_account3 == False:
            databasemanager.server_accounts(userid,code=2)
            self.create_server_account(client_name,value=3)
            self.stop_user(client_name,value=3)
        elif tariff == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == 1:
            databasemanager.server_accounts(userid,code=5)
            databasemanager.server_accounts(userid,code=6)
        elif tariff == 2 or 4 and server_account1 == 1 and server_account2 == 1 and server_account3 == 1:
            databasemanager.server_accounts(userid,code=6)
        elif tariff == 3 or 5 and server_account1 == 1 and server_account2 == 1 and server_account3 == 1:
            return
        elif tariff == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == 0:
            databasemanager.server_accounts(userid,code=5)
        elif tariff == 2 or 4 and server_account1 == 1 and server_account2 == 1 and server_account3 == 0:
            return
        elif tariff == 3 or 5 and server_account1 == 1 and server_account2 == 1 and server_account3 == 0:
            databasemanager.server_accounts(userid,code=3)
        elif tariff == 1 and server_account1 == 1 and server_account2 == 0 and server_account3 == 0:
            return
        elif tariff == 2 or 4 and server_account1 == 1 and server_account2 == 0 and server_account3 == 0:
            databasemanager.server_accounts(userid,code=2)
        elif tariff == 3 or 5 and server_account1 == 1 and server_account2 == 0 and server_account3 == 0:
            databasemanager.server_accounts(userid,code=2)
            databasemanager.server_accounts(userid,code=3)

    def create_server_account(self,client_name,value):
        command = f'source /home/vpnserver/awgm && generate_config "{client_name}{value}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)
        command = f'source /home/vpnserver/awgm && сopy_config_files "{client_name}{value}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)
    
    def stop_user(self,client_name,value):
        command = f'source /home/vpnserver/awgm && stop_config "{client_name}{value}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)

    def start_user(self,client_name,value):
        command = f'source /home/vpnserver/awgm && start_config "{client_name}{value}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)

    def active_server_switch(self,userid,client_name):
        databasemanager = database()
        server_account1 = databasemanager.get_server_account1(userid)
        server_account2 = databasemanager.get_server_account2(userid)
        server_account3 = databasemanager.get_server_account3(userid)
        activestatus = databasemanager.get_active_status(userid)
        if activestatus == 1 and server_account1 == 1 and server_account2 == False or 0 and server_account3 == False or 0:
            self.start_user(client_name,value=None)
        if activestatus == 0 and server_account1 == 1 and server_account2 == False or 0 and server_account3 == False or 0:
            self.stop_user(client_name,value=None)
        if activestatus == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == False or 0:
            self.start_user(client_name,value=None)
            self.start_user(client_name,value=2)
        if activestatus == 0 and server_account1 == 1 and server_account2 == 1 and server_account3 == False or 0:
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
        if activestatus == 1 and server_account1 == 1 and server_account2 == 1 and server_account3 == 1:
            self.start_user(client_name,value=None)
            self.start_user(client_name,value=2)
            self.start_user(client_name,value=3)
        if activestatus == 0 and server_account1 == 1 and server_account2 == 1 and server_account3 == 1:
            self.stop_user(client_name,value=None)
            self.stop_user(client_name,value=2)
            self.stop_user(client_name,value=3)