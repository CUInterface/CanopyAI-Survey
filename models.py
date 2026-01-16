from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    votes = db.relationship('Vote', backref='user', lazy='dynamic')
    suggested_questions = db.relationship('Question', backref='suggested_by', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    follow_up_example = db.Column(db.String(255))
    use_case = db.Column(db.String(100))
    is_user_suggested = db.Column(db.Boolean, default=False)
    suggested_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    votes = db.relationship('Vote', backref='question', lazy='dynamic')

    @property
    def upvote_count(self):
        return self.votes.filter_by(vote_type='upvote').count()

    @property
    def downvote_count(self):
        return self.votes.filter_by(vote_type='downvote').count()

    @property
    def net_score(self):
        return self.upvote_count - self.downvote_count

    def get_user_vote(self, user_id):
        """Return the user's vote type for this question, or None if not voted."""
        vote = self.votes.filter_by(user_id=user_id).first()
        return vote.vote_type if vote else None

    def __repr__(self):
        return f'<Question {self.question_id}>'


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'question_id', name='unique_user_question_vote'),
        db.CheckConstraint(vote_type.in_(['upvote', 'downvote']), name='valid_vote_type'),
    )

    def __repr__(self):
        return f'<Vote {self.user_id} -> {self.question_id}: {self.vote_type}>'
