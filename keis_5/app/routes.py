from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User, Transaction
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import csv

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Неправильное имя пользователя или пароль!')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    income = sum(t.amount for t in transactions if t.type == 'income')
    expenses = sum(t.amount for t in transactions if t.type == 'expense')
    return render_template('dashboard.html', transactions=transactions, income=income, expenses=expenses)

@app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    category = request.form['category']
    t_type = request.form['type']
    amount = float(request.form['amount'])
    date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    new_transaction = Transaction(
        user_id=current_user.id, category=category, type=t_type, amount=amount, date=date
    )
    db.session.add(new_transaction)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/export')
@login_required
def export():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    with open('transactions.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Category', 'Type', 'Amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for t in transactions:
            writer.writerow({'Date': t.date, 'Category': t.category, 'Type': t.type, 'Amount': t.amount})
    flash('Данные экспортированы в файл transactions.csv')
    return redirect(url_for('dashboard'))
