# clean_commuter
Hack Zurich 2019


## Requirements

- `conda>=3.7`

## Usage

Create a conda environment:

```sh
conda env create -f conda.yml
```

Activate the environment:

```sh
conda activate hackzurich
```

Install in editable mode for development:

```sh
pip install -e .
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

