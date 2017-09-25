import requests
import urllib3
import facebook
import os
from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension

#https://developers.facebook.com/docs/graph-api/reference/event/
#https://medium.com/towards-data-science/how-to-use-facebook-graph-api-and-extract-data-using-python-1839e19d6999

app = Flask(__name__)

api = facebook.Api(
    app_id=os.environ['FACEBOOK_APP_ID'],
    secret_key=os.environ['FACEBOOK_APP_SECRET'],
    user_token=os.environ['FACEBOOK_USER_TOKEN']
)

graph = facebook.GraphAPI(access_token=user_token, version=2.7)


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

    events = graph.request("/search?q=party&type=event&limit=100")
    eventList = events['data']
    eventid = eventList[1]['id']

    event1 = graph.get_object(id=eventid, fields='fields=’attending_count,can_guests_invite,category,cover,declined_count,description,end_time,guest_list_enabled,interested_count,is_canceled,is_page_owned,is_viewer_admin,maybe_count,noreply_count,owner,parent_group,place,ticket_uri,timezone,type,updated_time')
    attenderscount = event1['attending_count']

    return event1, attenderscount