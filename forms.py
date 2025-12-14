from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, BooleanField, RadioField, TextAreaField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional
from models import User


class RegistrationForm(FlaskForm):
    """User registration form."""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    nickname = StringField('Nickname (optional)', validators=[
        Optional(),
        Length(max=80, message='Nickname must be at most 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    team = SelectField('Choose Your Team', 
        choices=[('red', '🔴 Red Team'), ('blue', '🔵 Blue Team'), ('green', '🟢 Green Team')],
        validators=[DataRequired()]
    )
    show_leaderboard = BooleanField('I am competitive and want to see the leaderboard on my dashboard', default=True)
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username already exists."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email already exists."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    """User login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class WeeklyPlanForm(FlaskForm):
    """Weekly plan creation form."""
    book_id = SelectField('Book', coerce=int, validators=[DataRequired()])
    plan_mode = RadioField('Plan Mode', 
                          choices=[('chapterwise', 'Chapterwise (Complete one chapter per week)'),
                                 ('subchapterwise', 'Subchapterwise (Complete specific sections per week)'),
                                 ('own_pace', 'Own Pace (Custom exercises each week)')],
                          default='chapterwise',
                          validators=[DataRequired()])
    start_chapter = SelectField('Starting Chapter', coerce=int, validators=[Optional()])
    deadline_day = SelectField('Deadline Day',
                              choices=[
                                  ('monday', 'Monday'),
                                  ('tuesday', 'Tuesday'),
                                  ('wednesday', 'Wednesday'),
                                  ('thursday', 'Thursday'),
                                  ('friday', 'Friday'),
                                  ('saturday', 'Saturday'),
                                  ('sunday', 'Sunday')
                              ],
                              default='sunday',
                              validators=[DataRequired()])
    deadline_hour = SelectField('Hour',
                               choices=[(str(i), f"{i:02d}") for i in range(0, 24)],
                               default='12',
                               validators=[DataRequired()])
    deadline_minute = SelectField('Minute',
                                 choices=[(str(i), f"{i:02d}") for i in range(0, 60, 5)],
                                 default='0',
                                 validators=[DataRequired()])
    custom_exercises = TextAreaField('Custom Exercises for This Week',
                                    render_kw={"placeholder": "e.g., chap. 1 exercises 2,4,5,7,8 or Chapter 2: ex 1-10",
                                             "rows": 3},
                                    validators=[Optional()])
    submit = SubmitField('Create Plan')
