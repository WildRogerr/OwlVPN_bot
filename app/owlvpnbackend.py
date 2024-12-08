import sqlite3
import subprocess

class database():

    def adduser(self, userdata):
        userid = userdata[0]
        firstname = userdata[1]
        lastname = userdata[2]
        username = userdata[3]
        promo = 0
        pay_day = 0
        days_without_pay = 0
        next_month = 0
        active = 0
        server_account1 = 0
        server_account2 = 0
        server_account3 = 0

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
                cur.execute(f'UPDATE botowluserskz SET userid = ? firstname = ? lastname = ? username = ? pay_day = ? days_without_pay = ? next_month = ? WHERE client_id = ?)',
                            (userid,firstname,lastname,username,pay_day,days_without_pay,next_month,client_check[0]))
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
            cur.execute(f'''INSERT INTO botowluserskz(userid,firstname,lastname,username,promo,pay_day,days_without_pay,next_month,active)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (userid,firstname,lastname,username,promo,pay_day,days_without_pay,next_month,active))
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
        tariff = number[0]
        conn.commit()
        conn.close()
        return tariff
    
    def getpromo(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT promo FROM botowluserskz WHERE userid = ?',(userid,))
        number = cur.fetchone()
        promo = number[0]
        conn.commit()
        conn.close()
        return promo
    
    def get_client_name(self,userid):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        cur.execute(f'SELECT client_name FROM botowluserskz WHERE userid = ?',(userid,))
        name = cur.fetchone()
        client_name = name[0]
        conn.commit()
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

class managebot():

    def connect_user(self,client_name,tariff):
        command = f'source /home/vpnserver/awgm.sh && generate_config "{client_name}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)
        command = f'source /home/vpnserver/awgm.sh && сopy_config_files "{client_name}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)

    def stop_user(self,client_name):
        command = f'source /home/vpnserver/awgm.sh && stop_config "{client_name}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)

    def start_user(self,client_name):
        command = f'source /home/vpnserver/awgm.sh && start_config "{client_name}"'
        subprocess.run(command, shell=True, capture_output=True, text=True)

    # Написать:
    # Функция отключения аккаунтов после смены тарифа в меньшую или включения после смены в большую или добавление нового
    # Функция остановки серверного аккаунта после истечения таймера и функция отправок сообщений по истечении таймера
    # Функция активации и деактивации аккаунта в базе данных
    # Функция включения аккаунта после оплаты
    # Функция выполнения проверки активных серверных аккаунтов и их наличие