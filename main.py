# main.py

from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

# Create a Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/rtsp"
mongo = PyMongo(app)

# Function to save text to MongoDB
def save_text_to_mongodb(text):
    mongo.db.text.insert_one({
        'text': text,
    })

# Function to get the latest text from MongoDB
def get_latest_text_from_mongodb():
    saved_text = mongo.db.text.find_one(sort=[('_id', -1)])
    return saved_text.get('text') if saved_text else None

# Landing page route
@app.route('/', methods=['GET'])
def landing_page():
    user_text = get_latest_text_from_mongodb()
    return render_template('index.html', user_text=user_text)

# Form submission route
@app.route('/submit', methods=['POST'])
def submit_text():
    user_text = request.form.get('text')
    save_text_to_mongodb(user_text)
    return jsonify({'user_text': user_text})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
