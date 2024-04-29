from db import db
from sqlalchemy import text
import topics

def display_threads(id):
    sql = text("""select threads.thread_name,threads.id as threadid,
            count(messages.id) as messages_count
            from threads left join topics 
            on threads.topic_id = topics.id
            left join messages
            on messages.thread_id = threads.id
            where threads.topic_id =:id
            group by threads.id
            order by messages_count desc""")
    result = db.session.execute(sql, {"id":id} )
    return result.fetchall()