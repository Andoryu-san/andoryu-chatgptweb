from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from flask import render_template
from pytube import YouTube

app = Flask(__name__)
app.config['SECRET_KEY'] = 'x'  # Replace with a strong, secret key
app.config['MONGO_URI'] = 'x'  # Replace with your MongoDB URI
app.config['STATIC_FOLDER'] = 'static' # Detect the css file

mongo = PyMongo(app)

login_manager = LoginManager(app)

# Mock user data (replace with MongoDB integration later)
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

# Example users
users = {'user1': User('andoryu'), 'user2': User('andoryuro')}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/forum')
def forum():
    return render_template('forum_page.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me_page.html')

@app.route('/blog')
def blog():
    return render_template('blog_page.html')

@app.route('/tools')
def tools():
    return render_template('tools_page.html')

@app.route('/features')
def features():
    return render_template('features_page.html')

@app.route('/youtube_downloader', methods=['GET', 'POST'])
@login_required
def youtube_downloader():
    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            # Download video
            yt = YouTube(video_url)
            video = yt.streams.filter(file_extension='mp4', resolution='720p').first()
            video.download('static/videos')  # Save videos in the 'static/videos' folder

            # Save download information in MongoDB
            download_info = {
                'user_id': current_user.id,
                'video_title': yt.title,
                'video_url': video_url,
            }
            mongo.db.downloads.insert_one(download_info)

            return redirect(url_for('youtube_downloader'))
        except Exception as e:
            error_message = f'Error: {str(e)}'
            return render_template('youtube_downloader.html', error_message=error_message)

    return render_template('youtube_downloader.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot_page.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message']
    chatgpt_api_url = 'x'  # Replace with the actual ChatGPT API endpoint

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'user_id': current_user.id,
        'user_message': user_message,
    }

    response = request.post(chatgpt_api_url, headers=headers, json=data)

    if response.status_code == 200:
        chatbot_response = response.json().get('chatbot_response')
        return render_template('chatbot_page.html', user_message=user_message, chatbot_response=chatbot_response)

    return 'Error getting response from ChatGPT API'

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
