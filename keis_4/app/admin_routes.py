from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Survey, Question

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        title = request.form['title']
        survey = Survey(title=title)
        db.session.add(survey)
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))

    surveys = Survey.query.all()
    return render_template('admin.html', surveys=surveys)

@admin.route('/admin/survey/<int:survey_id>/questions', methods=['POST'])
def add_question(survey_id):
    text = request.form['text']
    question_type = request.form['type']
    question = Question(text=text, question_type=question_type, survey_id=survey_id)
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))
