import facebook, json, os
from pprint import pprint
from flask import Flask, flash, redirect, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = "ultra secret ssssh"
user_token = os.environ['FACEBOOK_USER_TOKEN']
gmaps_key = os.environ['GOOGLE_MAPS_TOKEN']
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
def grab_events():
    """Gets from HTML, grabs and returns events from Graph API."""

    event_keyword = request.args.get('event-keyword').strip().replace(" ", "%20")
    search_location = request.args.get('city').strip().lower()

    events = graph.request("/search?q=" + event_keyword + "&type=event&limit=10", post_args={'method': 'get'})
    return jsonify(events), search_location, event_keyword


def paginate(events, event_keyword):
    """Allows next page of results from Graph."""
        #how do I tie pagination in with grab_events?
    check_pagination = events.get('paging', {})
    print check_pagination

    if check_pagination != {}:
        for paging in check_pagination:
            check_cursors = check_pagination.get('cursors', {})
            check_after = check_cursors.get('after', '')
            check_before = check_cursors.get('before', '')
            check_next = check_pagination.get('next', '')
            if check_after != '':
                next_page = graph.request("/search?access_token=" + user_token + "&q=" + event_keyword + "&type=event&limit=1000&after=" + check_after)
            else:
                flash("End of results.")

    return render_template("/search-results.html", next_page=next_page)


def input_checks(event_keyword, search_location, events):
    """Performs checks on nested dicts, var existence/match checks."""

    event_by_city = []

    if event_keyword and search_location:
        for individual_events in events['data']:
            event_id = individual_events['id']
            check_place = individual_events.get('place', {})
            check_location = check_place.get('location', {})
            check_city = check_location.get('city', '')
            if check_city.lower() == search_location:
                event_by_city.append(event_id)
    else:
        flash("You have to fill in both fields!")
        return redirect("/event-search")

    return event_by_city


def event_details(event_by_city):
    """Makes batch request to Graph for event details."""

    event_data = graph.get_object(id=event_by_city,
                                      fields='attending_count, \
        category,start_time,end_time,interested_count,is_canceled, \
        is_page_owned,ticket_uri,timezone,type')
    return event_data


def detail_checks(event_data, events):
    """Checks to make sure attending_count, etc fit parameters. Puts events \
    set to be returned to user."""

    results_dictionary = {}
        #is this impractical? do I only need to run through events['data'] in input_checks()?
    for individual_events in events['data']:
        if event_data['attending_count'] <= 75 and \
            event_data['is_canceled'] is False and \
                event_data['is_page_owned'] is False:
            results_dictionary['url'] = "https://www.facebook.com/events/"# + str(ID OF EVENT) + "/"
            #based on how I've rewritten input_checks(), how do I get individual event ids?
            results_dictionary['event_name'] = individual_events['name']
            results_dictionary['event_description'] = individual_events['description']
            event_set = set()
            event_set.add(individual_events)

    return event_set, results_dictionary


# need to find places for all this:
    #                 for pkeys, pvals in individual_events['place'].iteritems():
    #                     if str(pkeys) == 'location':
    #                         for lkeys, lvals in pvals.iteritems():
    #                             results_dict[lkeys] = lvals
    #                     else:
    #                         results_dict[pkeys] = pvals
    #                     #else bit prints event owner data, if unpacks location
    #                 for keys, values in event_data.iteritems():
    #                     results_dict[keys] = values

def result_return(results_dictionary):
    """Handles edge cases, returns results."""

    if results_dictionary == {}:
        flash("No results found.")
        return redirect('/event-search')

    return render_template("/search-results")


@app.route("/process-json")
def jconvert():
    """Turns JSON to JS obj."""

    processor = open('event-results.json', 'r')
    json_string = processor.read()
    processor.close()
    data = json.loads(json_string)
    return jsonify(data)


### Helper Functions ####
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
