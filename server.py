import facebook, json, os, time
from pprint import pprint
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
    counter = 0
    events = graph.request("/search?q=" + event_keyword + "&type=event&limit=1000&since=" + str(current_time), post_args={'method': 'get'})
    check_pagination = events.get('paging', {})
    #how do I utilize pagination? 

    if event_keyword and search_location:
        for individual_events in events['data']:
            counter += 1
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
                    results_dict['url'] = "https://www.facebook.com/events/" + str(event_id) + "/"
                    results_dict['event_name'] = individual_events['name']
                    results_dict['event_description'] = individual_events['description']
                    for pkeys, pvals in individual_events['place'].iteritems():
                        if str(pkeys) == 'location':
                            for lkeys, lvals in pvals.iteritems():
                                results_dict[lkeys] = lvals
                        else:
                            results_dict[pkeys] = pvals
                        #else bit prints event owner data, if unpacks location
                    for keys, values in event_data.iteritems():
                        results_dict[keys] = values
                else:
                    continue
            else:
                continue
    else:
        flash("You have to fill in both fields!")
        return redirect("/event-search")

    print counter

    if results_dict == {}:
        flash("No results found.")
        return redirect('/event-search')

    json.dump(results_dict, open('event-results.json', 'w'))
    pprint(results_dict)

    return check_pagination, redirect("/pagination", check_pagination=check_pagination)


@app.route("/process-json")
def jconvert():
    """Turns JSON to JS obj."""

    processor = open('event-results.json', 'r')
    json_string = processor.read()
    processor.close()
    data = json.loads(json_string)
    return jsonify(data)


@app.route('/pagination')
def paginate():
    """Allows next page of results from Graph."""

    for paging in check_pagination:
       # check_cursors = check_pagination.get('cursors', {})
        check_after = check_cursors.get('after', '')
       # check_before = check_cursors.get('before', '')
        check_next = check_pagination.get('next', '')
        if check_after != '':
            next_page = graph.request("/search?access_token=" + user_token + "&since=" + current_time + "&q=" + event_keyword + "&type=event&limit=1000&after=" + check_after)

    return render_template("/search-results.html", )


### Helper Functions ####
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
