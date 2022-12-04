from app import app, db
from flask import render_template, request, session, redirect
from models.models import Plant, Employee, User
from sqlalchemy import or_
import hashlib
import re
from sqlalchemy.exc import IntegrityError


@app.route("/")
def main():
    plants = Plant.query.order_by(Plant.title.asc()).all()
    user = None
    if session.get("user", False):
        user = User.query.get(session.get("user"))
    return render_template("index.html", plants=plants, user=user)

@app.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        data = request.form
        try:
            user = User(
                username=data.get("username"),
                email=data.get("email"),
                password=hashlib.md5(data.get("password").encode()).hexdigest(),
                first_name=data.get("first_name"),
                last_name=data.get("last_name")
            )
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            return render_template("sign_up.html", error="This email or username already exists")
        session["user"] = user.id
        return redirect("/")
    else:
        return render_template("sign_up.html")

@app.route("/sign-in", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        user = User.query.filter(or_(User.email == request.form.get("email"), User.username == request.form.get("email"))).first()
        if user is not None:
            if user.password == hashlib.md5(request.form.get("password").encode()).hexdigest():
                session["user"] = user.id
        return redirect("/")
    else:
        return render_template("sign_in.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

