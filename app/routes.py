from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Habit, HabitProgress
from datetime import datetime

@app.route("/")
def index():
    habits = Habit.query.all()
    return render_template("index.html", habits=habits)

@app.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        if name:
            habit = Habit(name=name, description=description)
            db.session.add(habit)
            db.session.commit()
            flash("Habit added successfully!")
            return redirect(url_for("index"))
        else:
            flash("Name is required!")
    return render_template("add_habit.html")

@app.route("/edit/<int:habit_id>", methods=["GET", "POST"])
def edit_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if request.method == "POST":
        habit.name = request.form.get("name")
        habit.description = request.form.get("description")
        db.session.commit()
        flash("Habit updated successfully!")
        return redirect(url_for("index"))
    return render_template("edit_habit.html", habit=habit)

@app.route("/progress/<int:habit_id>")
def progress(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    progress = HabitProgress.query.filter_by(habit_id=habit.id).all()
    return render_template("progress.html", habit=habit, progress=progress)
