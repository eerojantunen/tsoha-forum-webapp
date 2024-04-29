from db import db
from sqlalchemy import text
import threads

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