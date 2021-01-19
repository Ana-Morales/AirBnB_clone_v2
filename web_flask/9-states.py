#!/usr/bin/python3
"""Starts a Flask web application"""

from models import storage
from models.state import State
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Call storage.close()"""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def city_state(id=None):
    """Displays list States or list of Cities by State"""
    states = storage.all(State)
    if id:
        key = "State." + id
    else:
        key = None
    return render_template('9-states.html', states=states, key=key)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
