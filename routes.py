from app import app
from flask import render_template
import topics, threads, messages

@app.route("/")
def index():
    topics_list = topics.get_list()        
    return render_template("index.html",topics_list=topics_list)

@app.route("/topic/<int:id>")
def topic(id):
    threads_data = threads.display_threads(id)
    return render_template("topic.html",threads_data=threads_data)

@app.route("/thread/<int:id>")
def thread(id):
    messages_data = messages.get_list(id)
    return render_template("messages.html",messages_data=messages_data)