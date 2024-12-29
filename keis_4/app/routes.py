from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Survey, Question, Answer

main = Blueprint('main', __name__)

@main.route('/survey/<int:survey_id>', methods=['GET', 'POST'])
@jwt_required()
def survey(survey_id):
    if request.method == 'POST':
        user_id = get_jwt_identity()
        data = request.form
        for question_id, answer_text in data.items():
            answer = Answer(question_id=question_id, user_id=user_id, answer=answer_text)
            db.session.add(answer)
        db.session.commit()
        return jsonify({'message': 'Survey submitted successfully'})

    survey = Survey.query.get_or_404(survey_id)
    return render_template('survey.html', survey=survey)
