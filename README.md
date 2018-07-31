# crasher

This is my final project for Hackbright. It searches by keyword for parties, then filters said parties by location, then plots the parties on a map (complete with links to the events and onsite detail pages).

<b>Retrospective</b>: A lot of my time on this project got absorbed into trying to tweak the Facebook Graph API. I was expecting it to return more results than it did, because Graph doesn't return the type/quantity of events I expected (for example, you'll never find any house parties to crash using this, because Graph will never return them to you when you make requests API-side). I'd be better off trying to utilize any of the libraries that allow you to discover any events that are public <i>and</i> happening at places with their own Facebook pages. For demo purposes, this will pull from your events, but I have around 30 keywords in the file you can uncomment and check out. It's just a lot of API requests to make.

<b>Features</b>:
* Uses keyword(s) to find events by the city you submit, using the Facebook Graph API
* Filters those events out by the city you entered
* Filters those events further to find smallish events that haven't been canceled and aren't owned by Facebook pages
* Plots those events using coordinates onto a Google Map using the Google Maps API
* Links to the FB event pages themselves and provides detail page for each event
__________

<b>Tech stack</b>: Python, JavaScript, HTML, CSS, Flask, JQuery, Jinja, Bootstrap<br>
Utilizes Facebook Graph API and Google Maps API

__________

<img src="https://i.imgur.com/mUJxGwa.png"></img>
