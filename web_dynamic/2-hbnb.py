#!/usr/bin/python3
"""Starts a Flask web application for the HBNB project."""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid

app = Flask(__name__)

# Optional: Configure Jinja2 to trim and strip whitespace in templates
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """Close the SQLAlchemy session after each request."""
    storage.close()


@app.route('/2-hbnb', strict_slashes=False)
def hbnb():
    """Render the HBNB page with sorted states, cities, amenities, and places."""
    states = sorted(storage.all(State).values(), key=lambda k: k.name)
    st_ct = [[state, sorted(state.cities, key=lambda k: k.name)] for state in states]

    amenities = sorted(storage.all(Amenity).values(), key=lambda k: k.name)
    places = sorted(storage.all(Place).values(), key=lambda k: k.name)

    return render_template('2-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places, 
                           cache_id=uuid.uuid4())


if __name__ == "__main__":
    """Run the Flask application on 0.0.0.0:5000."""
    app.run(host='0.0.0.0', port=5000)

