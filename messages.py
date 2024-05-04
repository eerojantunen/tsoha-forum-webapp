from db import db
from sqlalchemy import text
import threads, users

def get_list(id):
    sql = text("""
                select messages.message,
               messages.created_at,
               users.username,
               threads.topic_id as topic_id,
               threads.thread_name as thread_name
               from threads left join messages on
               messages.thread_id = threads.id
               left join users on
               messages.user_id = users.id
               where messages.status = 1 and messages.thread_id =:id
               group by messages.created_at,
               messages.message,
               users.username,
               threads.topic_id,
               threads.thread_name
               order by messages.created_at desc
""")
    result = db.session.execute(sql, {"id":id} )
    return result.fetchall()

def send_new(message, thread_id):
    user_id = users.get_id()
    if user_id == 0:
        return False
    
    sql = text("""INSERT INTO messages (message, 
               thread_id, user_id, status,
                created_at)
               values (:message, :thread_id, :user_id,
               1, NOW()
               )""")
    db.session.execute(sql, {"message":message,"thread_id":thread_id,"user_id":user_id,})
    db.session.commit()
    return True

def get_name(id):

    sql = text("""
                    select threads.thread_name from threads where threads.id =:id
               
    """)
    result = db.session.execute(sql, {"id":id} )
    return result.fetchone()[0]

def user_messages(user_id):
    sql = text("""select messages.id, messages.message, messages.created_at
               from messages
               where messages.user_id =:user_id and messages.status = 1
               order by messages.created_at desc
""")
    results = db.session.execute(sql,{"user_id":user_id})
    return results.fetchall()

def edit(message_id,new_message):
    print(message_id)
    print(new_message)
    sql = text(""" update messages
               set message =:new_message
               where id =:message_id
""")
    db.session.execute(sql,{"new_message":new_message,"message_id":message_id})
    db.session.commit()

def delete_message(message_id):
    sql = text(""" update messages
               set status = 0
               where id =:message_id
""")
    db.session.execute(sql,{"message_id":message_id})
    db.session.commit()

def delete(id):
    sql = text(""" update messages
               set status = 0
               where messages.id =:id
""")
    db.session.execute(sql, {"id":id})
    db.session.commit()

def search(message):
    search_edited = f'%{message}%'
    sql = text("""
                select messages.message,
               messages.created_at,
               users.username,
               threads.topic_id as topic_id,
               threads.thread_name as thread_name
               from threads left join messages on
               messages.thread_id = threads.id
               left join users on
               messages.user_id = users.id
               where messages.status = 1 and messages.message like :message
               group by messages.created_at,
               messages.message,
               users.username,
               threads.topic_id,
               threads.thread_name
               order by messages.created_at desc
""")

    result = db.session.execute(sql, {"message":search_edited})
    return result.fetchall()
