from db import db
from sqlalchemy import text

def get_list():
    sql = text("""SELECT topics.id as topics_id, topics.status,
                topics.topic_name, 
               count(distinct threads.id) as threads_count,
               count(messages.id) as messages_count
               FROM topics 
               left join threads 
               on topics.id = threads.topic_id and threads.status=1
               left join messages
               on messages.thread_id = threads.id and messages.status = 1
               group by topics.id
               order by threads_count desc""")
    result = db.session.execute(sql)
    return result.fetchall()

def topic_name(id):
    sql = text(""" select topic_name
               from topics
               where topics.id =:id
               limit 1
""")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()