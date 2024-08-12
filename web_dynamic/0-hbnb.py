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

# Optional: Configure Jinja to trim and strip blocks for cleaner templates
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """Closes the current SQLAlchemy session after each request."""
    storage.close()


@app.route('/0-hbnb/', strict_slashes=False)
def hbnb():
    """Renders the HBNB homepage with dynamic content."""
    # Retrieve and sort states by name
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    
    # Prepare a list of states and their associated sorted cities
    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    # Retrieve and sort amenities by name
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    # Retrieve and sort places by name
    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    # Render the template with the prepared data
    return render_template('100-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places, 
                           cache_id=uuid.uuid4())


if __name__ == "__main__":
    """Runs the Flask application on host 0.0.0.0 and port 5000."""
    app.run(host='0.0.0.0', port=5000)
