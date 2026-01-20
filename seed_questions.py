"""
Seed script to populate the database with the 30 pre-generated questions from
GitHub Issue #84: https://github.com/CUInterface/Vyrdia_Financial_AI/issues/84
"""

from app import create_app
from models import db, Question

# Marketing Questions (10)
MARKETING_QUESTIONS = [
    {
        'question_id': 'mkt_001',
        'question_text': "What's our member growth rate this year?",
        'follow_up_example': 'compared to last year',
        'use_case': 'Acquisition tracking'
    },
    {
        'question_id': 'mkt_002',
        'question_text': 'Show me members by age group',
        'follow_up_example': 'who have auto loans',
        'use_case': 'Demographic segmentation'
    },
    {
        'question_id': 'mkt_003',
        'question_text': 'Which members have only one product with us?',
        'follow_up_example': 'checking account only',
        'use_case': 'Cross-sell opportunity'
    },
    {
        'question_id': 'mkt_004',
        'question_text': 'How many members joined from each channel?',
        'follow_up_example': 'online vs branch vs referral',
        'use_case': 'Channel attribution'
    },
    {
        'question_id': 'mkt_005',
        'question_text': "Show members who haven't logged in recently",
        'follow_up_example': 'over 90 days',
        'use_case': 'Engagement/retention'
    },
    {
        'question_id': 'mkt_006',
        'question_text': 'Which zip codes have the most members?',
        'follow_up_example': 'with high loan balances',
        'use_case': 'Geographic targeting'
    },
    {
        'question_id': 'mkt_007',
        'question_text': 'Members approaching loan payoff',
        'follow_up_example': 'within 6 months',
        'use_case': 'Refinance campaigns'
    },
    {
        'question_id': 'mkt_008',
        'question_text': 'Show members with high share balances but no loans',
        'follow_up_example': 'over $50k in deposits',
        'use_case': 'Loan cross-sell'
    },
    {
        'question_id': 'mkt_009',
        'question_text': 'What\'s the average member tenure?',
        'follow_up_example': 'by product type',
        'use_case': 'Retention analysis'
    },
    {
        'question_id': 'mkt_010',
        'question_text': 'New members this month by branch',
        'follow_up_example': 'with their first products',
        'use_case': 'Onboarding tracking'
    },
]

# Loans Questions (10)
LOANS_QUESTIONS = [
    {
        'question_id': 'loan_001',
        'question_text': 'What loans are maturing next month?',
        'follow_up_example': 'auto loans only',
        'use_case': 'Retention/refinance'
    },
    {
        'question_id': 'loan_002',
        'question_text': 'Show my pipeline as a loan officer',
        'follow_up_example': '(by officer ID)',
        'use_case': 'Pipeline management'
    },
    {
        'question_id': 'loan_003',
        'question_text': 'Average time to fund a loan',
        'follow_up_example': 'by loan type',
        'use_case': 'Process efficiency'
    },
    {
        'question_id': 'loan_004',
        'question_text': 'Loans originated this quarter',
        'follow_up_example': 'by dollar volume',
        'use_case': 'Production tracking'
    },
    {
        'question_id': 'loan_005',
        'question_text': 'Which loans have rate adjustments coming up?',
        'follow_up_example': 'ARMs in next 90 days',
        'use_case': 'Rate monitoring'
    },
    {
        'question_id': 'loan_006',
        'question_text': 'Show loans with high DTI ratios',
        'follow_up_example': 'over 40%',
        'use_case': 'Risk assessment'
    },
    {
        'question_id': 'loan_007',
        'question_text': 'Members with loan payoff quotes',
        'follow_up_example': 'requested this week',
        'use_case': 'Payoff tracking'
    },
    {
        'question_id': 'loan_008',
        'question_text': 'Compare our rates to origination volume',
        'follow_up_example': 'are competitive rates driving volume?',
        'use_case': 'Pricing analysis'
    },
    {
        'question_id': 'loan_009',
        'question_text': 'Loans with multiple co-borrowers',
        'follow_up_example': 'show guarantors',
        'use_case': 'Relationship mapping'
    },
    {
        'question_id': 'loan_010',
        'question_text': 'Which loan products have highest approval rates?',
        'follow_up_example': 'by credit tier',
        'use_case': 'Product performance'
    },
]

# Live Transactions Questions (10)
LIVE_TRANSACTIONS_QUESTIONS = [
    {
        'question_id': 'live_001',
        'question_text': "What's happening right now?",
        'follow_up_example': 'last 15 minutes',
        'use_case': 'Real-time monitoring'
    },
    {
        'question_id': 'live_002',
        'question_text': 'Show large transactions today',
        'follow_up_example': 'over $10,000',
        'use_case': 'Unusual activity'
    },
    {
        'question_id': 'live_003',
        'question_text': 'Any declined transactions in the last hour?',
        'follow_up_example': 'show reason codes',
        'use_case': 'Issue triage'
    },
    {
        'question_id': 'live_004',
        'question_text': 'Current pending ACH batches',
        'follow_up_example': 'by dollar amount',
        'use_case': 'Settlement tracking'
    },
    {
        'question_id': 'live_005',
        'question_text': 'Card swipes happening now',
        'follow_up_example': 'by merchant type',
        'use_case': 'Real-time card activity'
    },
    {
        'question_id': 'live_006',
        'question_text': 'Show wire transfers today',
        'follow_up_example': 'outgoing only',
        'use_case': 'Wire monitoring'
    },
    {
        'question_id': 'live_007',
        'question_text': 'Any unusual account activity?',
        'follow_up_example': 'multiple transactions same account',
        'use_case': 'Fraud detection'
    },
    {
        'question_id': 'live_008',
        'question_text': "What's our transaction volume today vs yesterday?",
        'follow_up_example': 'same time period',
        'use_case': 'Volume comparison'
    },
    {
        'question_id': 'live_009',
        'question_text': 'Show mobile deposit activity',
        'follow_up_example': 'pending review',
        'use_case': 'Remote deposit capture'
    },
    {
        'question_id': 'live_010',
        'question_text': 'Current ATM network status',
        'follow_up_example': 'any offline machines',
        'use_case': 'Operations monitoring'
    },
]


def seed_questions():
    """Seed all 30 pre-generated questions into the database."""
    import os
    env = os.environ.get('FLASK_ENV', 'development')
    # Use production config if DATABASE_URL is set
    if os.environ.get('DATABASE_URL'):
        env = 'production'
    app = create_app(env)

    with app.app_context():
        # Check if questions already exist
        existing = Question.query.count()
        if existing > 0:
            print(f'Database already has {existing} questions. Skipping seed.')
            return

        # Add Marketing questions
        for q in MARKETING_QUESTIONS:
            question = Question(
                question_id=q['question_id'],
                category='marketing',
                question_text=q['question_text'],
                follow_up_example=q['follow_up_example'],
                use_case=q['use_case'],
                is_user_suggested=False
            )
            db.session.add(question)

        # Add Loans questions
        for q in LOANS_QUESTIONS:
            question = Question(
                question_id=q['question_id'],
                category='loans',
                question_text=q['question_text'],
                follow_up_example=q['follow_up_example'],
                use_case=q['use_case'],
                is_user_suggested=False
            )
            db.session.add(question)

        # Add Live Transactions questions
        for q in LIVE_TRANSACTIONS_QUESTIONS:
            question = Question(
                question_id=q['question_id'],
                category='live_transactions',
                question_text=q['question_text'],
                follow_up_example=q['follow_up_example'],
                use_case=q['use_case'],
                is_user_suggested=False
            )
            db.session.add(question)

        db.session.commit()
        print('Successfully seeded 30 questions!')


if __name__ == '__main__':
    seed_questions()
