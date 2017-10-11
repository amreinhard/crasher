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
    events = graph.request("/search?q=" + event_keyword + "&type=event&limit=1000", post_args={'method': 'get'})
    returned_events = []

    while events:
        event_list = input_checks(event_keyword, search_location, events)
        event_list = event_details(event_list)
        checker = detail_checks(event_list, events)
        returned_events.extend(checker)
        events = paginate(events, event_keyword)
        if not events['data']:
            #check for paging token instead
            flash("No more results.")
            break

    #pprint(returned_events)
    for single_events in returned_events:
        json.dump(single_events, open('event-results.json', 'w'))
    return render_template("/search-results.html")


def paginate(events, event_keyword):
    """Allows next page of results from Graph."""

    check_pagination = events.get('paging', {})
    next_page = None

    if check_pagination:
        for paging in check_pagination:
            check_cursors = check_pagination.get('cursors', {})
            check_after = check_cursors.get('after', '')
            #check_before = check_cursors.get('before', '')
            #check_next = check_pagination.get('next', '')
            if check_after != '':
                next_page = graph.request("/search?access_token=" + user_token + "&q=" + event_keyword + "&type=event&limit=1000&after=" + check_after)

    return next_page


def input_checks(event_keyword, search_location, events):
    """Performs checks on nested dicts, var existence/match checks. \
    Checks city, if city matches, appends id to list."""

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

    event_data = graph.get_objects(ids=event_by_city,
                                   fields='attending_count, \
        category,description,start_time,end_time,interested_count,is_canceled, \
        is_page_owned,name,place,ticket_uri,timezone,type')
    return event_data


def detail_checks(event_data, events):
    """Checks to make sure attending_count, etc fit parameters. Creates event \
    list."""

    results_dictionary = {}
    event_list = []

    for individual_event in event_data.values():
        if individual_event['attending_count'] <= 75 and \
            individual_event['is_canceled'] is False and \
                individual_event['is_page_owned'] is False:
            for ikeys, ivals in individual_event.iteritems():
                if str(ikeys) == 'place':
                    for pkeys, pvals in ivals.iteritems():
                        if str(pkeys) == 'location':
                            for lkeys, lvals in pvals.iteritems():
                                results_dictionary[lkeys] = lvals
                else:
                    results_dictionary[ikeys] = ivals
                #else bit assigns basic event info, ifs unpack place + location
            results_dictionary['url'] = "https://www.facebook.com/events/" + individual_event['id']
            event_list.append(results_dictionary)

    if event_list == []:
        flash("No results found.")
        return redirect('/event-search')

    return event_list


@app.route("/process-json")
def jconvert():
    """Turns JSON to JS obj."""

    processor = open('event-results.json', 'r')
    json_string = processor.read()
    processor.close()
    data = json.loads(json_string)
    return jsonify(data)

### Debugger ####
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
