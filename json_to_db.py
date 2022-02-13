import json
import sqlite3
from datetime import datetime
import os

json_files=[]
for file in os.listdir("./convo"):
        json_file = os.path.join("convo", file)
        json_files.append(json_file)

conn = sqlite3.connect("msg_db.db")

statement = """INSERT INTO
messages (date,sender,content,reply)
VALUES (?,?,?,?)
"""

def json_to_db(json_file):
    with open(json_file) as f:
        z = json.load(f)
        msgs = z["messages"]

        for msg in msgs:
            if "content" in msg:
                sender = msg["sender_name"]
                sender = sender.encode('latin1').decode('utf8')
                content = msg["content"]
                content = content.encode('latin1').decode('utf8')
                ts = int(msg["timestamp_ms"])
                msg_datetime = datetime.fromtimestamp(ts/1000.0).date()
                reply = 0
                if "reactions" in msg:
                    reply = 1
                record = (msg_datetime,sender,content,reply)
                conn.execute(statement,record)
        conn.commit()
    f.close()

for i in json_files:
     json_to_db(i)