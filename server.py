import facebook
import os
import json
import time
from pprint import pprint
from flask import Flask, flash, redirect, request, render_template
from flask_debugtoolbar import DebugToolbarExtension

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

    current_time = int(time.time())
    event_keyword = request.args.get('event-keyword').strip().replace(" ", "%20")
    search_location = request.args.get('city').strip().lower()
    results_dict = {}
    events = graph.request("/search?q=" + event_keyword + "&type=event&limit=100") # &since=" + str(current_time) + "&after=")
    event_list = events['data']
    pprint(events)
    #how do I utilize pagination? or filter for more accurate local results?

    if event_keyword and search_location:
        for individual_events in event_list:
            event_id = individual_events['id']  # ID NEEDED TO ACCESS EVENTS
            check_place = individual_events.get('place', {})
            check_location = check_place.get('location', {})
            check_city = check_location.get('city', '')

            if check_city.lower() == search_location:
                event_data = graph.get_object(id=event_id,
                                              fields='attending_count, \
                category,start_time,end_time,interested_count,is_canceled, \
                is_page_owned,maybe_count,ticket_uri,timezone,type')
                if event_data['attending_count'] <= 75 and \
                    event_data['is_canceled'] is False and \
                        event_data['is_page_owned'] is False:
                    results_dict['url' + ':'] = "https://www.facebook.com/events/" + str(event_id) + "/"
                    results_dict['event_name' + ':'] = individual_events['name']
                    results_dict['event_description' + ':'] = individual_events['description']
                    for pkeys, pvals in individual_events['place'].iteritems():
                        if str(pkeys) == 'location':
                            for lkeys, lvals in pvals.iteritems():
                                results_dict[lkeys + ":"] = lvals
                        else:
                            results_dict[pkeys + ":"] = pvals
                        #else bit prints event owner data, if unpacks location
                    for keys, values in event_data.iteritems():
                        results_dict[keys + ":"] = values
                else:
                    continue
            else:
                continue
    else:
        flash("You have to fill in both fields!")
        return redirect("/event-search")

    if results_dict == {}:
        flash("No results found.")
        return redirect('/event-search')

    json.dump(results_dict, open('event-results.json', 'w'))

    return render_template("/search-results.html", results_dict=results_dict)

#### Helper Functions ####
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
