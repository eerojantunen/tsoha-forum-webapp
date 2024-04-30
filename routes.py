from app import app
from flask import render_template, request, redirect, url_for
import topics, threads, messages, users

@app.route("/")
def index():
    topics_list = topics.get_list()        
    return render_template("index.html",topics_list=topics_list)

@app.route("/topic/<int:id>")
def topic(id):
    threads_data = threads.display_threads(id)
    return render_template("topic.html",threads_data=threads_data)

@app.route("/thread/<int:thread_id>")
def thread(thread_id):
    messages_data = messages.get_list(thread_id)
    return render_template("messages.html",messages_data=messages_data, thread_id=thread_id)

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