import sqlite3

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS messages (
                                        id integer PRIMARY KEY,
                                        date date NOT NULL,
                                        sender text NOT NULL,
                                        content text NOT NULL,
                                        reply integer NOT NULL
                                    ); """



def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(db_file)
    return conn
    

def create_table(conn,sql_statement):
    c = conn.cursor()
    c.execute(sql_statement)


if __name__ == "__main__":
    db_nm = "msg_db.db"
    conn = create_connection(db_nm)
    create_table(conn, sql_create_projects_table)