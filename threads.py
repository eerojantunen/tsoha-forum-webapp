from db import db
from sqlalchemy import text
import topics, messages

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

def insert_thread(name,message,creator_id,topic_id):
    sql = text("""insert into threads (topic_id,
               access_type,
               status,thread_name,
               creator_id)
               values(:topic_id,1,1,:name,:creator_id               
               )
               returning id
               """)
    result = db.session.execute(sql, {"topic_id":topic_id,"name":name,"creator_id":creator_id})
    thread_id = result.fetchone()[0]

    db.session.commit()
    print(thread_id)
    messages.send_new(message,thread_id)
    return True