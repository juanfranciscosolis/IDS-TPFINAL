from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='template')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about-us')
def about():
    return render_template('about-us.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route ('/contact')
def contact():
    return render_template('contact.html')

@app.route('/elements')
def elements():
    return render_template('elements.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/services')
def services():
    return render_template('services.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)

