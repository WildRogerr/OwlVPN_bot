import sqlite3

class database:

    def adduser(self):
        conn = sqlite3.connect('./owldatabase.db')
        cur = conn.cursor()
        userid = self.getuserdata(userid)
        username = self.getuserdata(username)
        firstname = self.getuserdata(firstname)
        lastname = self.getuserdata(lastname)
        pay_day = 0
        days_without_pay = 0
        next_month = False
        cur.execute(f'INSERT INTO botowluserskz(userid,firstname,lastname,username,pay_day,days_without_pay,next_month) VALUES (?, ?, ?, ?, ?, ?, ?)',(userid,firstname,lastname,username,pay_day,days_without_pay,next_month))

    def getuserdata(self):
        userid = 1
        username = 1
        firstname = 1
        lastname = 1
        return userid, username, firstname, lastname