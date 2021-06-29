import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("loandatabase.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS loan (id INTEGER PRIMARY KEY, customer_name TEXT, tenure integer, balance integer, loantype TEXT, interesttype TEXT,interest integer,security TEXT,totalpayment integer,emi integer,instruction TEXT)")
        self.conn.commit()

    def insert(self,cname,tenure,blance,ltype,itype,interest,security,tpay,emi,instr):
        self.cur.execute("INSERT INTO loan VALUES (NULL,?,?,?,?,?,?,?,?,?,?)",(cname,tenure,blance,ltype,itype,interest,security,tpay,emi,instr))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM loan")
        rows = self.cur.fetchall()
        return rows
    
    def viewspecific(self,cname="",instr =""):
        self.cur.execute("SELECT * FROM loan WHERE customer_name = ? or instruction = ?",(cname,instr))
        rows = self.cur.fetchall()
        return rows
    
    def delete(self,id):
        self.cur.execute("DELETE FROM loan WHERE id = ?",(id,))
        self.conn.commit()

    def update(self,instr,cname):
        self.cur.execute("UPDATE loan SET instruction =? WHERE customer_name= ?",(instr,cname))
        self.conn.commit()

    def viewrejec(self,instr =""):
        self.cur.execute("SELECT * FROM loan WHERE instruction = ?",(instr,))
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()

