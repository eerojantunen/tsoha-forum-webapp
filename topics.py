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

def create_topic(topic_name, access_type):
    sql = text(""" insert into topics
                (topic_name, access_type, status)
               values (:topic_name, :access_type, 1)
""")
    db.session.execute(sql,{"topic_name":topic_name,"access_type":access_type})
    db.session.commit()

def thread_to_topic(id):
    sql = text(""" select topics.id from topics 
               left join threads on threads.topic_id = topics.id
               where threads.id =:id
""")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def topic_access(id):
    sql = text(""" select topics.access_type from topics 
               where topics.id =:id
""")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def add_to_topic(topic_id, user_id):
    sql = text(""" insert into private_topics
                (user_id, topic_id)
               values (:user_id, :topic_id)
""")
    db.session.execute(sql,{"user_id":user_id,"topic_id":topic_id})
    db.session.commit()

def delete_topic(id):
    sql = text(""" update topics 
               set status = 0
               where id=:id
""")
    db.session.execute(sql,{"id":id})
    db.session.commit()

def topic_rename(new_name,id):
    sql = text(""" update topics 
               set topic_name =:new_name
               where id=:id
""")
    db.session.execute(sql,{"new_name":new_name,"id":id})
    db.session.commit()