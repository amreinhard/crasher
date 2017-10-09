import facebook, json, os, time
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
    #fixed

    event_keyword = request.args.get('event-keyword').strip().replace(" ", "%20")
    search_location = request.args.get('city').strip().lower()

    events = graph.request("/search?q=" + event_keyword + "&type=event&limit=10000", post_args={'method': 'get'}) 
    return events, search_location

def paginate():
    """Allows next page of results from Graph."""
        #how do I tie pagination in with grab_events?

    for paging in check_pagination:
       # # check_cursors = check_pagination.get('cursors', {})
       #  check_after = check_cursors.get('after', '')
       # # check_before = check_cursors.get('before', '')
       #  check_next = check_pagination.get('next', '')
        if check_after != '':
            next_page = graph.request("/search?access_token=" + user_token + "&since=" + current_time + "&q=" + event_keyword + "&type=event&limit=1000&after=" + check_after)
            #probably need to rewrite this at some point^
    return render_template("/search-results.html", )


def input_checks(event_keyword, search_location, events):
    """Performs checks on nested dicts, var existence/match checks."""

    event_by_city = set()

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


def detail_checks(event_data):
    """Checks to make sure attending_count, etc fit parameters."""

    results_dict = {}
        #do I need to move/declare this individual_events-relevant stuff in 
        #input_checks()? or is there another way?
    if event_data['attending_count'] <= 75 and \
        event_data['is_canceled'] is False and \
            event_data['is_page_owned'] is False:
        results_dict['url'] = "https://www.facebook.com/events/" + str(#ID OF EVENT) + "/"
        #based on how I've rewritten input_checks(), how do I get event_id?
        results_dict['event_name'] = individual_events['name']
        results_dict['event_description'] = individual_events['description'] #syntax error on this line? why?
        event_set = set()
        event_set.add(events)

    return event_set


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

    # json.dump(check_pagination, open('pagination.json', 'w'))
    # pprint(results_dict)

def result_return():
    """Handles edge cases, returns results."""

    if results_dict == {}:
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
