import facebook
import os
from flask import Flask, redirect, request, render_template
from flask_debugtoolbar import DebugToolbarExtension

#https://developers.facebook.com/docs/graph-api/reference/event/
#https://medium.com/towards-data-science/how-to-use-facebook-graph-api-and-extract-data-using-python-1839e19d6999

app = Flask(__name__)
app.secret_key = "ultra secret ssssh"
user_token = os.environ['FACEBOOK_USER_TOKEN']
graph = facebook.GraphAPI(access_token=user_token, version=2.10)


@app.route("/")
def homepage():
    """Renders homepage."""

    return render_template("homepage.html")


@app.route("/event-search")
def render_event_form():
    """Renders event finder form."""

    return render_template("event-search.html")


@app.route("/upcoming-events", methods=["GET"])
def plot_events():
    """Finds and returns upcoming events from Facebook."""

    event_keyword = request.args.get('event-keyword').strip().replace(" ", "%20")

    events = graph.request("/search?q=" + event_keyword + "&type=event&limit=5")
    eventList = events['data']
    #eventid = eventList[1]['id']

    for i, individual_events in enumerate(eventList):
        print individual_events['name'] + "\n" + individual_events['description']
        for i, x in individual_events['place'].iteritems():
            if str(i) == 'location':
                for j, y in x.iteritems():
                    print str(j) + ": " + str(y)
            else:
                print i + ": " + x

        #print locale['id']
        #print locale['location']['city']
        print "//////////////////"

    #event1 = graph.get_object(id=eventid, fields='attending_count,can_guests_invite,category,cover,declined_count,description,end_time,guest_list_enabled,interested_count,is_canceled,is_page_owned,is_viewer_admin,maybe_count,noreply_count,owner,parent_group,place,ticket_uri,timezone,type,updated_time')
    #attenderscount = event1['attending_count']

    #print event_info
    #print attenderscount

    #return render_template("/search-results.html")

#### Helper Functions ####
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)