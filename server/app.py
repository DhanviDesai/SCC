from flask import Flask, jsonify

app = Flask(__name__)

# Define a route for the root URL '/'
@app.route("/")
def index():
    """
    This view function handles requests to the root URL.
    """
    return "<h1>Welcome to the Flask Backend Service!</h1>"

# Define a simple API endpoint
@app.route("/api/hello")
def hello_api():
    """
    This view function returns a simple JSON response.
    """
    return jsonify({"message": "Hello from the Flask API!"})

if __name__ == '__main__':
    # This block allows running the app directly for development
    # python app.py
    app.run(debug=True)