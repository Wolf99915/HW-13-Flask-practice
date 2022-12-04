from app import app, db
from flask import render_template, request, redirect
from models.models import Employee, Plant

@app.route("/save-employee", methods=["POST"])
def save_employee():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    plant_id = request.form.get("plant_id")
    employee = Employee(first_name=first_name, last_name=last_name, email=email, plant_id=plant_id)
    db.session.add(employee)
    db.session.commit()
    return redirect("/")

@app.route("/delete-employee/<int:id>")
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")

@app.route("/employees")
def employee():
    employees = Employee.query.all()
    return render_template("employees-list.html", employees=employees)

@app.route("/add-employee", methods=["POST", "GET"])
def add_employee():
    if request.method == "POST":
        data = request.form
        try:
            employee = Employee(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                plant_id=int(data.get("plant_id"))
            )
            db.session.add(employee)
            db.session.commit()
        except:
            return "This email alredy exist!"
        return redirect("/employees")
    else:
        plants = Plant.query.all()
        return render_template("add_employee.html", plants=plants)

@app.route("/about-employee/<int:id>")
def about_employee(id):
    employee = Employee.query.get(id)
    return render_template("/about_employee.html", employee=employee)

@app.route("/edit-employee/<int:id>")
def edit_employee(id):
    employee = Employee.query.get(id)
    return render_template("/add_employee.html", employee=employee)

@app.route("/update-employee/<int:id>", methods=["POST"])
def update_employee(id):
    employee = Employee.query.get(id)
    employee.first_name = request.form.get("first_name")
    employee.last_name = request.form.get("last_name")
    employee.email = request.form.get("email")
    db.session.add(employee)
    db.session.commit()
    return redirect("/")

