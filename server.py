import requests, json
from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension

# GET /oauth/access_token
#     ?client_id=os.environ['FACEBOOK_APP_ID']
#     &client_secret=os.environ['FACEBOOK_APP_SECRET']
#     &grant_type=client_credentials
#how do I use this?

#https://developers.facebook.com/docs/graph-api/reference/event/

app = Flask(__name__)
app.secret_key = os.environ['FACEBOOK_APP_SECRET']

event_info = graph.get_object(id='event_id',
                              fields='id, start_time, is_canceled, owner, parent_group, attending_count, category, guest_list_enabled, description')

#GET graph.facebook.com/search?q=user_query&type=event

@app.route("/")
def homepage():
    """Renders homepage."""

    return render_template("homepage.html")

@app.route("/event-search")
def render_event_form():
    """Renders event finder form."""

    return render_temploate("event-search.html")

@app.route("/upcoming-events")
def plot_events():
    """Finds and returns upcoming events from Facebook."""

    event = request.args.get("/graph.facebook.com/search?q=party&type=event")

    return event