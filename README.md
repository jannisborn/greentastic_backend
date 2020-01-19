<img align="right" width="100" height="100" src="https://github.com/jannisborn/clean_commuter/blob/ios_app/CleanConmute/AppIcon.appiconset/cleancommute_icon-76%402x.png">

# Greentastic 
### A project created @Hack Zurich 2019

<img align="right" src="https://github.com/jannisborn/greentastic/blob/master/assets/demo.jpeg" alt="demo" width="400"/>

## Usage:
* Download the [TestFlight iOS App](https://testflight.apple.com/join/qIDSZLzE)
* Scroll to the bottom to get quick impressions.
## Code requirements:
For full functionality (including own deployment) you need:
* `XCode>=10`
* `Python>=3.6`
    * `numpy`
    * `googlemaps`
    * `polyline`
    * `flask`
    * `gunicorn`
* Billed account on `Google Cloud Platform` (get started [here](https://cloud.google.com))
    * API Dependencies (need to be enabled individually)
        * `Directions`
        * `Places`
    * `Google Cloud SDK` (get started [here](https://cloud.google.com/appengine/docs/flexible/python/quickstart))
    * Paste your keypair into the repo's main folder and name it `greentastic.keypair`




## Test backend functionality:
Create a virtual environment:

```sh
python3 -m venv env
```

Activate the environment:

```sh
source env/bin/activate
```

Install in editable mode for development:

```sh
pip install  -r requirements.txt
```
Run
```
python app.py
```
the output roots to
```
http://localhost:5000/
```
and you can query directions e.g. from Ütliberg to Zürichberg by:
```
http://localhost:5000/query_directions?source=Uetliberg&destination=Zuerichberg
```
or run it from command line by:

```
curl -X GET "http://localhost:5000/query_directions?weights=1,1,1,1,1&source=Uetliberg&destination=Zuerichberg"
```
you can also make a `POST` request via `curl` and point to a `json` with a user profile:

```
curl "http://localhost:5000/query_directions?source=Uetliberg&destination=Zuerichberg" -d '@user_profile.json'
```

## Deploy the backend as API: 
Make sure to enable the Google Cloud Platform dependencies and add the keypair, then deploy (takes several minutes):
```
gcloud app deploy
```

and then run
```
gcloud app browse
```

Currently, you can access the API on [https://clean-commuter.appspot.com/](https://clean-commuter.appspot.com/query_directions) (the root doesn't work, you have to enter a query as shown above).

# Some impressions
Type your location into the search field, upon pressing <Enter>, the app performs a handy autocompletion. Choose the desired target destination, then enter the start location or just use your current location. You will be prompted with several means of transportation (car, bike, walk, transit but even ebike, escooter or taxi). The proposals are sorted according to an overall score that combines `costs`, `duration`, `co2 emissions`, `calories burnt` and `pollution`. The intuitive color scheme allows to assess easily which transporation type is best for which metric. Choose your preferred option and Greentastic will draw the track onto your map. Easily toogle between `standard`, `hybrid` or `satellite` maps. In your profile, you can customize which metrics matter most to you. Do you want to save money? Are in a rush? Or want to be environmently friendly? Just specify the weights and Greentastics recommendation will change. Finally, the history of chosen tracks is recorded in a statistics overview page - check it out to see how much C02 you saved and what your favorite types of transporation are.   
<img align="center" src="https://github.com/jannisborn/greentastic/blob/master/assets/demo.jpeg" alt="demo" width="400"/> 
<img align="center" src="https://github.com/jannisborn/greentastic/blob/master/assets/tracks.jpeg" alt="demo" width="400"/> 
<img align="center" src="https://github.com/jannisborn/greentastic/blob/master/assets/profile.jpeg" alt="demo" width="400"/>
<img align="center" src="https://github.com/jannisborn/greentastic/blob/master/assets/tracks_hybrid.jpeg" alt="demo" width="400"/>
<img align="center" src="https://github.com/jannisborn/greentastic/blob/master/assets/stats.jpeg" alt="demo" width="400"/>



# Sources:

## Calories:

https://www.foodspring.ch/kalorienverbrauch-tabelle (per 30 minutes)
(all kind of activities are listed there)

## Prices: 
* car: 71ct per km: https://www.tcs.ch/de/der-tcs/presse/medienmitteilungen/kilometerkostenstick.php
* ebike: 3500 http://www.velosuisse.ch/de/statistik_aktuell.html
* normal bike: 1250 https://www.velojournal.ch/pdfdownload.html?filename=2010_01/1000-Franken-Velos.pdf
* taxi: https://www.20min.ch/finance/news/story/So-teuer-ist-Taxifahren-in-Schweizer-Staedten-26519985
* bike: 1250 preis neu, dann reparaturen, aber 5000 km genutzt --> 0.3 pro km
* ecar und normal car https://www.buyacar.co.uk/cars/economical-cars/electric-cars/650/cost-of-running-an-electric-car

### Possible sources for public transport fares:
* https://ec.europa.eu/transport/sites/transport/files/modes/rail/studies/doc/2016-04-price-quality-rail-pax-services-final-report.pdf 
* norwegian linear functions: https://www.researchgate.net/publication/241164152_The_relationship_between_travel_distance_and_fares_time_costs_and_generalized_costs_in_passenger_transport 


## CO2 and NOx emissions (=toxicity)

### Public transport:
Including car, tram, train, bus etc: https://www.umweltbundesamt.de/themen/verkehr-laerm/emissionsdaten#verkehrsmittelvergleich_personenverkehr  
--> Took this source for all public transport values

### Cars

E-car, diesel, hybrid, etc. 
https://www.bmu.de/fileadmin/Daten_BMU/Download_PDF/Verkehr/emob_umweltbilanz_2019_bf.pdf 

### bike, ebike, escooter:
* bike: 5g CO2 pro km according to https://dasfahrradblog.blogspot.com/2015/04/die-co2-bilanz-des-fahrrads.html 
* ferry and some others: https://www.co2nnect.org/help_sheets/?op_id=602&opt_id=98
* ebike: https://www.suedostschweiz.ch/zeitung/e-bike-fahrer-sind-nur-bedingt-sauber-unterwegs-0
* escooter: https://www.quarks.de/technik/mobilitaet/e-scooter-darum-ist-ihre-klimabilanz-gar-nicht-mal-so-gut/

--> So far we assume that electric transport like escooter and ebike are not toxic (do not have NOx emissions)

## Sources we did not use in the end:
* car 210 pro km in g CO2 https://dasfahrradblog.blogspot.com/2015/04/die-co2-bilanz-des-fahrrads.html
* fuel prices https://www.tcs.ch/de/camping-reisen/reiseinformationen/wissenswertes/fahrkosten-gebuehren/benzinpreise.php
* car service rates https://www.comparis.ch/autoversicherung/junglenker/analyse/auto-kosten
* calories: we had a different source for calories with slightly different values, also dependent on the person's weight. This might be useful at some later point when we include weight in the user profile.
https://laufleistung.net/kalorienverbrauch-berechnen/ (per 15 minutes)

## To do (where the research is not rigorous so far):
* For bike, taxi and car distinguish between base price and kilometer price? (base price for bying a car versus fuel costs etc?)
* Distinguish emissions and toxicity of long distance train, heavy rail etc (so far only as fine grained as [this source](https://www.co2nnect.org/help_sheets/?op_id=602&opt_id=98) )
* Ferry toxicity: so far, just took the value of airplanes because probably it's a lot and I can't find any per km value
* taxi toxicity: so far just the car value and a bit more because the taxi is driving around empty more often
* toxicity production of bike escooter etc?
