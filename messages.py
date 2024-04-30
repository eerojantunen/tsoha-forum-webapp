from db import db
from sqlalchemy import text
import threads, users

def get_list(id):
    sql = text("""
                select messages.message,
               messages.created_at,
               users.username
               from threads left join messages on
               messages.thread_id = threads.id
               left join users on
               messages.user_id = users.id
               group by messages.created_at,
               messages.message,
               users.username
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

