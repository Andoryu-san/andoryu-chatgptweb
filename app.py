from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong, secret key

login_manager = LoginManager(app)

# Mock user data (replace with MongoDB integration later)
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# Example users
users = {'user1': User('user1'), 'user2': User('user2')}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
def home():
    return 'Hello, World!'

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            user = users[username]
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')  # Create a login.html template later

# Dashboard route (protected)
@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.id}! This is your dashboard.'

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You have been logged out.'

if __name__ == '__main__':
    app.run(debug=True)
