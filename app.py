import os
import csv
import io
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, Response
from models import db, User, Question, Vote
from config import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Routes
    @app.route('/')
    def index():
        if 'user_id' in session:
            return redirect(url_for('survey'))
        return render_template('index.html')

    @app.route('/login', methods=['POST'])
    def login():
        email = request.form.get('email', '').strip().lower()
        if not email or '@' not in email:
            return render_template('index.html', error='Please enter a valid email address.')

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()

        session['user_id'] = user.id
        session['email'] = user.email
        return redirect(url_for('survey'))

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    @app.route('/survey')
    def survey():
        if 'user_id' not in session:
            return redirect(url_for('index'))

        user_id = session['user_id']

        # Get questions grouped by category
        categories = {
            'marketing': Question.query.filter_by(category='marketing').order_by(Question.question_id).all(),
            'loans': Question.query.filter_by(category='loans').order_by(Question.question_id).all(),
            'live_transactions': Question.query.filter_by(category='live_transactions').order_by(Question.question_id).all(),
            'user_suggested': Question.query.filter_by(is_user_suggested=True).order_by(Question.created_at.desc()).all(),
        }

        # Get user's votes
        user_votes = {}
        votes = Vote.query.filter_by(user_id=user_id).all()
        for vote in votes:
            user_votes[vote.question_id] = vote.vote_type

        return render_template('survey.html',
                             categories=categories,
                             user_votes=user_votes,
                             email=session.get('email'))

    @app.route('/vote', methods=['POST'])
    def vote():
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401

        data = request.get_json()
        question_id = data.get('question_id')
        vote_type = data.get('vote_type')  # 'upvote', 'downvote', or 'remove'

        if not question_id:
            return jsonify({'error': 'Missing question_id'}), 400

        question = Question.query.get(question_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404

        user_id = session['user_id']
        existing_vote = Vote.query.filter_by(user_id=user_id, question_id=question_id).first()

        if vote_type == 'remove':
            if existing_vote:
                db.session.delete(existing_vote)
                db.session.commit()
        elif vote_type in ['upvote', 'downvote']:
            if existing_vote:
                if existing_vote.vote_type == vote_type:
                    # Same vote type - remove the vote (toggle off)
                    db.session.delete(existing_vote)
                else:
                    # Different vote type - change the vote
                    existing_vote.vote_type = vote_type
            else:
                # New vote
                new_vote = Vote(user_id=user_id, question_id=question_id, vote_type=vote_type)
                db.session.add(new_vote)
            db.session.commit()
        else:
            return jsonify({'error': 'Invalid vote_type'}), 400

        # Return updated counts
        return jsonify({
            'upvotes': question.upvote_count,
            'downvotes': question.downvote_count,
            'net_score': question.net_score,
            'user_vote': question.get_user_vote(user_id)
        })

    @app.route('/suggest', methods=['GET', 'POST'])
    def suggest():
        if 'user_id' not in session:
            return redirect(url_for('index'))

        if request.method == 'POST':
            question_text = request.form.get('question_text', '').strip()
            category = request.form.get('category', 'general').strip()
            follow_up = request.form.get('follow_up_example', '').strip()
            use_case = request.form.get('use_case', '').strip()

            if not question_text:
                return render_template('suggest.html', error='Question text is required.',
                                     email=session.get('email'))

            # Generate unique question ID
            count = Question.query.filter_by(is_user_suggested=True).count()
            question_id = f'user_{count + 1:03d}'

            question = Question(
                question_id=question_id,
                category='user_suggested',
                question_text=question_text,
                follow_up_example=follow_up if follow_up else None,
                use_case=use_case if use_case else category,
                is_user_suggested=True,
                suggested_by_user_id=session['user_id']
            )
            db.session.add(question)
            db.session.commit()

            return redirect(url_for('survey'))

        return render_template('suggest.html', email=session.get('email'))

    @app.route('/results')
    def results():
        # Get all questions sorted by net score
        questions = Question.query.all()

        # Calculate scores and sort
        scored_questions = []
        for q in questions:
            scored_questions.append({
                'question': q,
                'upvotes': q.upvote_count,
                'downvotes': q.downvote_count,
                'net_score': q.net_score
            })

        scored_questions.sort(key=lambda x: x['net_score'], reverse=True)

        # Group by category for filtering
        categories = ['marketing', 'loans', 'live_transactions', 'user_suggested']
        category_filter = request.args.get('category', 'all')

        if category_filter != 'all':
            scored_questions = [q for q in scored_questions if q['question'].category == category_filter]

        return render_template('results.html',
                             questions=scored_questions,
                             categories=categories,
                             current_filter=category_filter,
                             email=session.get('email'))

    @app.route('/export')
    def export():
        questions = Question.query.all()

        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(['Question ID', 'Category', 'Question', 'Follow-up Example',
                        'Use Case', 'Upvotes', 'Downvotes', 'Net Score', 'User Suggested'])

        for q in sorted(questions, key=lambda x: x.net_score, reverse=True):
            writer.writerow([
                q.question_id,
                q.category,
                q.question_text,
                q.follow_up_example or '',
                q.use_case or '',
                q.upvote_count,
                q.downvote_count,
                q.net_score,
                'Yes' if q.is_user_suggested else 'No'
            ])

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=survey_results.csv'}
        )

    return app


# For local development
if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, port=5000)
