from app import app
from flask import render_template, request, redirect, url_for
import topics, threads, messages, users

@app.route("/")
def index():
    topics_list = topics.get_list()     
    is_admin = users.is_admin()
    print(is_admin)
    return render_template("index.html",topics_list=topics_list, is_admin=is_admin)

@app.route("/topic/<int:id>")
def topic(id):
    threads_data = threads.display_threads(id)
    topic_name = topics.topic_name(id)[0]
    return render_template("topic.html",threads_data=threads_data, topic_id=id, topic_name=topic_name)

@app.route("/thread/<int:thread_id>")
def thread(thread_id):
    messages_data = messages.get_list(thread_id)
    threadname = threads.get_name(thread_id)
    topic_id = topics.thread_to_topic(thread_id)
    return render_template("messages.html",messages_data=messages_data, thread_id=thread_id, threadname=threadname, topic_id=topic_id)

@app.route("/login", methods=["GET","POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username,password):
        return redirect("/")
    else:
        return render_template("error.html",message="Wrong username or password")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 == password2:
            if users.signup(username,password1):
                return redirect("/")
            else:
                return render_template("error.html",message = "Username taken")
        else:
            return render_template("error.html", message="Passwords don't match")

@app.route("/logout")     
def logout():
       users.logout()
       return redirect("/")

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form["message"]
    thread_id = request.form["thread_id"]
    if messages.send_new(message,thread_id):
        return redirect(url_for("thread", thread_id=thread_id))
    else:
        return render_template("error.html", message="ERROR")
    
@app.route("/new_thread", methods=["POST"])
def new_thread():
    topic_id = request.form["topic_id"]
    return render_template("new_thread.html",topic_id=topic_id)

@app.route("/create_thread", methods=["POST"])
def create_thread():
    thread_name = request.form["thread_name"]
    message = request.form["thread_message"]
    topic_id = request.form["topic_id"]
    user_id = users.get_id()
    threads.insert_thread(thread_name,message,user_id,topic_id)
    return redirect(url_for("topic",id=topic_id))

@app.route("/tools")
def tools():
    user_id = users.get_id()
    user_threads = threads.user_threads(user_id)
    user_messsages = messages.user_messages(user_id)
    return render_template("tools.html", user_id=user_id, user_threads=user_threads, user_messages=user_messsages)

@app.route("/thread_rename", methods=["POST"])
def thread_rename():
    thread_id = int(request.form["thread_id"])
    new_name = str(request.form["new_name"])
    threads.rename(thread_id,new_name)
    return redirect("/tools")

@app.route("/edit_message", methods=["POST"])
def edit_message():
    message_id = request.form["message_id"]
    message= request.form["new_message"]
    new_message = message + " (edited)"
    messages.edit(message_id,new_message)
    return redirect("/tools")

@app.route("/delete_message", methods=["POST"])
def delete_message():
    message_id = request.form["message_id"]
    messages.delete(message_id)
    return redirect("/tools")

@app.route("/delete_thread", methods=["POST"])
def delete_thread():
    thread_id = request.form["thread_id"]
    threads.delete(thread_id)
    return redirect("/tools")

@app.route("/return_to", methods=["POST"])
def return_to():
    topic_id = request.form["topic_id"]
    return redirect(url_for("topic", id=topic_id))

@app.route("/new_topic")
def new_topic():
    return render_template("create_topic.html")

@app.route("/create_topic", methods=["POST"])
def create_topic():
    topic_name = request.form["topic"]
    private_value = request.form.get("private_value")
    if private_value == None:
        topics.create_topic(topic_name,1)
    else:
        topics.create_topic(topic_name,0)

    return redirect("/")