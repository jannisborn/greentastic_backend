<img align="right" width="100" height="100" src="https://github.com/jannisborn/clean_commuter/blob/ios_app/CleanConmute/AppIcon.appiconset/cleancommute_icon-76%402x.png">

# Greentastic 
### A project created @Hack Zurich 2019

<img align="center" src="https://github.com/jannisborn/greentastic/blob/master/assets/demo.jpeg" alt="demo" width="400"/>

## Usage:
* Download the TestFlight iOS App from: []()
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




