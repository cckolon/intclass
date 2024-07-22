# Integral Classifier

Training a neural network to predict whether functions are integrable.

## Installation

1. Clone the repo and `cd` into it.
1. Make a virtual environment: `pip -m venv .venv`
1. Activate it: `source .venv/bin/activate`
1. Install requirements: `pip install -r requirements.txt`
1. Create/migrate the db: `python migrate.py`
1. Make some training data: `python make_data.py 1000`
1. train the model