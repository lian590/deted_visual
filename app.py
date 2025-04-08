from flask import Flask, render_template

app = Flask("__name__")

@app.route("/")
def home():
    return render_template("display.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/cadastro.html")
def cadastro():
    return render_template("cadastro.html")

@app.route("/pos_login.html")
def pos():
    return render_template("pos_login.html")


if __name__ == "__main__":
    app.run(debug=True)