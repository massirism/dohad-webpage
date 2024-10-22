from flask import Flask

app = Flask(__name__)

@app.route("/home")
def home():
    return "Hello, main page<h1>JUNIOR TU PAPÁ<H1>"

@app.route("/")
def index():
    return "Welcome to the main page!<h1>HELLO<H1>"

if __name__ == "__main__":
    app.run()

