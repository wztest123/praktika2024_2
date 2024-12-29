from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Task

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.tasks'))

@main.route('/tasks', methods=['GET', 'POST'])
@jwt_required()
def tasks():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        task = Task(title=title, description=description, due_date=due_date, user_id=user_id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.tasks'))

    tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template('tasks.html', tasks=tasks)
