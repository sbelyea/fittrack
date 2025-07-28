from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost/fittrack')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Workout model
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    classification = db.Column(db.String(100), nullable=False)  # e.g., 'weightlifting', 'cardio', 'flexibility'
    workout_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationship to exercises
    exercises = db.relationship('Exercise', backref='workout', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Workout {self.classification} on {self.workout_date}>'

# Exercise model (individual exercises within a workout)
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    exercise_name = db.Column(db.String(100), nullable=False)  # e.g., 'squats', 'bench press'
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)  # weight in pounds or kg
    weight_unit = db.Column(db.String(10), default='lbs')  # 'lbs' or 'kg'
    rest_time = db.Column(db.Integer)  # rest time in seconds
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Exercise {self.exercise_name}: {self.sets}x{self.reps} @ {self.weight}{self.weight_unit}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables function (used by init_db.py and for manual setup)
def create_tables():
    """Create database tables if they don't exist"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

# For Docker, tables are created by the db_init service
# For manual setup, tables are created by database_setup.py or when running directly

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html', user=current_user)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get recent workouts for the dashboard
    recent_workouts = Workout.query.filter_by(user_id=current_user.id)\
                            .order_by(Workout.workout_date.desc())\
                            .limit(5).all()
    
    # Get workout stats
    total_workouts = Workout.query.filter_by(user_id=current_user.id).count()
    
    return render_template('dashboard.html', 
                         user=current_user, 
                         recent_workouts=recent_workouts,
                         total_workouts=total_workouts)

# Workout routes
@app.route('/workouts')
@login_required
def workout_list():
    """Display all workouts for the current user"""
    workouts = Workout.query.filter_by(user_id=current_user.id)\
                           .order_by(Workout.workout_date.desc())\
                           .all()
    return render_template('workouts/list.html', workouts=workouts)

@app.route('/workouts/new', methods=['GET', 'POST'])
@login_required
def new_workout():
    """Create a new workout"""
    if request.method == 'POST':
        # Create new workout
        workout = Workout(
            user_id=current_user.id,
            classification=request.form['classification'],
            workout_date=request.form['workout_date'],
            notes=request.form.get('notes', '')
        )
        db.session.add(workout)
        db.session.flush()  # Get the workout ID
        
        # Add exercises
        exercise_count = 0
        while f'exercise_name_{exercise_count}' in request.form:
            if request.form[f'exercise_name_{exercise_count}'].strip():
                exercise = Exercise(
                    workout_id=workout.id,
                    exercise_name=request.form[f'exercise_name_{exercise_count}'],
                    sets=int(request.form[f'sets_{exercise_count}']),
                    reps=int(request.form[f'reps_{exercise_count}']),
                    weight=float(request.form[f'weight_{exercise_count}']) if request.form[f'weight_{exercise_count}'] else None,
                    weight_unit=request.form[f'weight_unit_{exercise_count}'],
                    notes=request.form.get(f'exercise_notes_{exercise_count}', '')
                )
                db.session.add(exercise)
            exercise_count += 1
        
        db.session.commit()
        flash('Workout logged successfully!')
        return redirect(url_for('workout_list'))
    
    return render_template('workouts/new.html')

@app.route('/workouts/<int:workout_id>')
@login_required
def view_workout(workout_id):
    """View a specific workout"""
    workout = Workout.query.filter_by(id=workout_id, user_id=current_user.id).first_or_404()
    return render_template('workouts/view.html', workout=workout)

@app.route('/workouts/<int:workout_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_workout(workout_id):
    """Edit an existing workout"""
    workout = Workout.query.filter_by(id=workout_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        # Update workout
        workout.classification = request.form['classification']
        workout.workout_date = request.form['workout_date']
        workout.notes = request.form.get('notes', '')
        
        # Delete existing exercises
        for exercise in workout.exercises:
            db.session.delete(exercise)
        
        # Add updated exercises
        exercise_count = 0
        while f'exercise_name_{exercise_count}' in request.form:
            if request.form[f'exercise_name_{exercise_count}'].strip():
                exercise = Exercise(
                    workout_id=workout.id,
                    exercise_name=request.form[f'exercise_name_{exercise_count}'],
                    sets=int(request.form[f'sets_{exercise_count}']),
                    reps=int(request.form[f'reps_{exercise_count}']),
                    weight=float(request.form[f'weight_{exercise_count}']) if request.form[f'weight_{exercise_count}'] else None,
                    weight_unit=request.form[f'weight_unit_{exercise_count}'],
                    notes=request.form.get(f'exercise_notes_{exercise_count}', '')
                )
                db.session.add(exercise)
            exercise_count += 1
        
        db.session.commit()
        flash('Workout updated successfully!')
        return redirect(url_for('view_workout', workout_id=workout.id))
    
    return render_template('workouts/edit.html', workout=workout)

@app.route('/workouts/<int:workout_id>/delete', methods=['POST'])
@login_required
def delete_workout(workout_id):
    """Delete a workout"""
    workout = Workout.query.filter_by(id=workout_id, user_id=current_user.id).first_or_404()
    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted successfully!')
    return redirect(url_for('workout_list'))

# API endpoints
@app.route('/api/user')
@login_required
def api_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)