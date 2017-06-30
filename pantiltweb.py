#!/usr/bin/env python
from sys import exit

try:
    import pantilthat
except ImportError:
    exit("This script requires the pantilthat module\nInstall with: sudo pip install pantilthat')

try:
    from flask import Flask, render_template
    from flask_assets import Environment, Bundle
except ImportError:
    exit("This script requires the flask module and flask_assets\nInstall with: sudo pip install flask and sudo pip install flask-assets")

app = Flask(__name__)
assets = Environment(app)

js = Bundle(
    'assets/jquery-3.2.1.js',
    filters='jsmin',
    output='gen/packed.js'
)
assets.register('js_all', js)

css = Bundle(
    'assets/bootstrap.min.css',
    'assets/bootstrap-theme.min.css',
    filters='cssmin',
    output='css/min.css'
)
assets.register('css_all', css)


@app.route('/')
def home():
    return render_template('webcam.html')

@app.route('/api/<direction>/<int:angle>')
def api(direction, angle):
    if angle < 0 or angle > 180:
        return "{'error':'out of range'}"

    angle -= 90

    if direction == 'pan':
        pantilthat.pan(angle)
        return '{{"direction": "pan", "angle":{}}}'.format(angle)

    elif direction == 'tilt':
        pantilthat.tilt(angle)
        return '{{"direction": "tilt", "angle":{}}}'.format(angle)

    return "{'error':'invalid direction'}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9595, debug=True)

