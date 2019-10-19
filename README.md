<img align="right" width="100" height="100" src="https://github.com/jannisborn/clean_commuter/blob/ios_app/CleanConmute/AppIcon.appiconset/cleancommute_icon-76%402x.png">

# Greentastic 
### A project created @Hack Zurich 2019

<img align="right" src="https://github.com/jannisborn/greentastic/blob/master/assets/demo.jpeg" alt="demo" width="400"/>

## Usage:
* Download the TestFlight iOS App from (coming soon...): []()
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

and then run:
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

