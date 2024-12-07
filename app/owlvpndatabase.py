import sqlite3

class database:

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

            if client_active_check == 1 and not client_userid_check:
                cur.execute(f'UPDATE botowluserskz SET userid = ? firstname = ? lastname = ? username = ? pay_day = ? days_without_pay = ? next_month = ? WHERE client_id = ?)',
                            (userid,firstname,lastname,username,pay_day,days_without_pay,next_month,client_check))
                conn.commit()
                conn.close()
                return 1
            
            elif client_active_check == 1 and client_userid_check:
                cur.execute(f'UPDATE botowluserskz SET username = ? WHERE userid = ?',(username,client_userid_check))
                conn.commit()
                conn.close()
                return 2
            
            elif client_active_check == 0 and client_tariff_check:
                cur.execute(f'UPDATE botowluserskz SET username = ? WHERE userid = ?',(username,client_userid_check))
                conn.commit()
                conn.close()
                return 3 
            
            elif client_active_check == 0 and not client_tariff_check:
                cur.execute(f'UPDATE botowluserskz SET username = ? WHERE userid = ?',(username,client_userid_check))
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