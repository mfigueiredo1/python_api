
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create a Databas


# Create Routes
@app.route('/')
def home():
    
    return 'Hello World'



if __name__ == '__main__':
    app.run(debug=True)