from db import db
from sqlalchemy import text

def get_list():
    sql = text("""SELECT topics.id as topics_id, topics.status,
                topics.topic_name, 
               count(distinct threads.id) as threads_count,
               count(messages.id) as messages_count
               FROM topics 
               left join threads 
               on topics.id = threads.topic_id 
               left join messages
               on messages.thread_id = threads.id
               group by topics.id
               order by threads_count desc""")
    result = db.session.execute(sql)
    return result.fetchall()