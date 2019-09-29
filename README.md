# Greentastic
A project created @Hack Zurich 2019


## Requirements 
* `flask`
* `numpy`
* `googlemaps`
* `polyline`


For own deployment you additionally need:
* Billed account on `Google Cloud Platform` (get started [here](https://cloud.google.com))
    * API Dependencies: 
        * `Directions`
        * `Places`
    * `Google Cloud SDK` (get started [here](https://cloud.google.com/appengine/docs/flexible/python/quickstart))
    * Paste your keypair into the repo's main folder and name it `greentastic.keypair`
* `gunicorn`



## Usage

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

## Test backend functionality:

In one terminal window, run 

```
python app.py
```

The output can be seen in localhost:5000, but it won't work because the parameter weights is missing. To test the code with the parameter, open a new terminal window and type

```
curl -X GET "localhost:5000/query_directions?weights=1,1,1,1,1&source=Uetliberg,%20Zuerich\&destination=Opernhaus%20Zuerich,%20Falkenstrasse,%20Zuerich"
```

Weighting can be varied, e.g. putting 3,1,1,1 set higher importance on the duration.

