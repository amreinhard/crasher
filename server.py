import facebook, json, os, time
from flask import Flask, flash, redirect, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = "ultra secret ssssh"
user_token = os.environ['FACEBOOK_USER_TOKEN']
graph = facebook.GraphAPI(access_token=user_token, version=2.10)


@app.route("/")
def homepage():
    """Renders homepage."""

    return render_template("homepage.html")


@app.route("/search-results", methods=["GET"])
def grab_events():
    """Gets from HTML, grabs and returns events from Graph API."""

    event_keywords = ["!"]  # ,'party', 'goodbye', 'housewarming', 'this', 'beach', 'celebration', 'promotion',
                      #'halloween', 'birthday', 'brunch', 'food', 'meetup', 'bash',
                      #'dinner', 'dance', 'BBQ', 'karaoke', 'adventure', 'celebrate',
                      #'heist', 'picnic', 'housewarming', 'bday', 'social', 'banquet',
                      #'anniversary', 'potluck', 'pregame', 'networking', 'holiday',
                      #'ceremony', 'gala', 'revelry', 'cookout', 'barbecue']
    search_location = request.args.get('city').strip().lower()
    returned_events = []
    current_time = int(time.time())  # so it's not a float

    for event_keyword in event_keywords:
        #keeps me from pulling expired events
        events = graph.request("/search?q=" + event_keyword + "&type=event&limit=1000&since=" + str(current_time), post_args={'method': 'get'})
        print len(events['data']), 'event length'  # to make sure we're getting events
        event_list = input_checks(search_location, events)  # calling helper functions
        event_list = event_details(event_list)
        checker = detail_checks(event_list)
        returned_events.extend(checker)
        #events = paginate(events, event_keyword)  # optional
        if returned_events != {}:
            json.dump(returned_events, open('event-results.json', 'w'), indent=2)  # write events to JSON file
        else:
            flash("No results found, try another city.")
            return redirect("/")

    return render_template("search-results.html", returned_events=returned_events)


@app.route("/search-results/<event_id>")
def show_details(event_id):
    """Grabs event details and shows them to user."""

    processor = open('event-results.json', 'r')
    json_string = processor.read()
    processor.close()
    data = json.loads(json_string)

    for details in data:
        if details['id'] == event_id:
            results = details  # reads specific JSON dicts for details

    return render_template("event-details.html", results=results)


###Helper functions###
def input_checks(search_location, events):
    """Performs checks on nested dicts, var existence/match checks. \
    Checks city, if city matches, appends id to list."""

    event_by_city = []

    if search_location:
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

    event_data = {}

    if event_by_city != []:
        event_data = graph.get_objects(ids=event_by_city,
                                       fields='attending_count, \
        description,start_time,end_time,interested_count,is_canceled, \
        is_page_owned,name,place,ticket_uri')

    return event_data


def detail_checks(event_data):
    """Checks to make sure attending_count, etc fit parameters. Creates event \
    list."""

    event_list = []

    if event_data != {}:
        for k, data in event_data.iteritems():
            if data['attending_count'] <= 75 and \
                data['is_canceled'] is False and \
                    data['is_page_owned'] is False:  # check if small, private event
                results_dictionary = {}
                results_dictionary['url'] = "https://www.facebook.com/events/" + data['id']
                for ikey in data:
                    # unpacks place and locations dictionaries
                    if str(ikey) == 'place':
                        for pkey in data[ikey]:
                            if str(pkey) == 'location':
                                for lkey in data[ikey]['location']:
                                    results_dictionary[lkey] = data[ikey]['location'][lkey]
                    else:
                        results_dictionary[ikey] = data[ikey]  # else bit assigns basic event info
                event_list.append(results_dictionary)
                    
    return event_list


# def paginate(events, event_keyword):
#     """Allows next page of results from Graph."""

#     check_pagination = events.get('paging', {})
#     next_page = None

#     if check_pagination:
#         for paging in check_pagination:
#             check_cursors = check_pagination.get('cursors', {})
#             check_after = check_cursors.get('after', '')
#             if check_after != '':
#                 next_page = graph.request("/search?access_token=" + user_token + "&q=" + event_keyword + "&type=event&limit=1000&after=" + check_after, post_args={'method': 'get'})

#     return next_page
# This works, but Facebook doesn't return enough results for pagination to be necessary.


@app.route("/process-json")
def jconvert():
    """Turns JSON to JS obj for Google Maps to read."""

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
