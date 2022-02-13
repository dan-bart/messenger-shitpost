import sqlite3
# Create database connection to the sqlite main database

class sql_crawler():
    def __init__(self,db_name):
        self.connectionObject    = sqlite3.connect(db_name, check_same_thread=False)
        self.c  = self.connectionObject.cursor()

    def question_content(self,name = None):
        if name != None:
            name_reg="%"+name+"%"
            statement = """select sender,content from messages where content like "%?%" and content not like "%http%" and sender like (?) order by random() limit 1;"""
            q = self.c.execute(statement,[name_reg])
        else:
            statement = """select sender,content from messages where content like "%?%" and content not like "%http%" order by random() limit 1;"""
            q = self.c.execute(statement)

        ret = q.fetchall()
        return ret

    def reply_content(self,name = None, q_name = None):
        if name != None:
            name_reg="%"+name+"%"
            statement = f"""select sender,content from messages where content like "%?%" and content not like "%http%" AND sender like (?) and sender != (?) order by random() limit 1;"""
            q = self.c.execute(statement,[name_reg,q_name])
        else:
            statement = """select sender,content from messages where reply = 1 and content not like "%http%" and sender != (?) order by random() limit 1;"""
            q = self.c.execute(statement,[q_name])

        ret = q.fetchall()
        return ret

