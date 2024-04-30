from app import app
from flask import render_template, request, redirect
import topics, threads, messages, users

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
