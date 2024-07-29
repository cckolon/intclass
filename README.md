# Integral Classifier

Training a neural network to predict whether functions are integrable. Based on the work of Lample and Charton in [Deep Learning for Symbolic Mathematics](https://arxiv.org/pdf/1912.01412).

## Installation

1. Install [direnv](https://direnv.net/) and [hook into your shell](https://direnv.net/docs/hook.html).
1. Install [the temporal CLI](https://learn.temporal.io/getting_started/python/dev_environment/#set-up-a-local-temporal-service-for-development-with-temporal-cli).
1. Install [docker](https://docs.docker.com/engine/install/).
1. Install [Python 3.11](https://www.python.org/downloads/) if you don't already have it.
1. Clone the repo and `cd` into it.
1. Make a blank `.env` file: `touch .env`
1. Make a virtual environment: `python -m venv .venv`
1. Activate it: `source .venv/bin/activate`
1. Install requirements: `pip install -r requirements.txt`

## Running the Database
1. Bring the db up: `startdb`
1. Migrate the db: `migrate`

## Making Training Data

1. Install
1. Run the database
1. Start the temporal development server: `temporal server start-dev`
1. Start a worker: `runworker`
1. Start the data generation workflow: `startwf`

## Using Multiple Computers to Generate Training Data

1. Pick one computer (the "server") that will run the temporal server.
1. Clone the repo and run the installation steps for all computers (temporal CLI is only required on the server).
1. Set the `DATABASE_HOST` and `TEMPORAL_SERVER` environment variables on all computers to the IP of the server.
1. On the server: run the database.
1. On the server: `temporal server start-dev --ip 0.0.0.0`
1. On all computers: `runworker`
1. On the server: `startwf`

## Running the Model

1. Train the model: `python train.py`
1. Run the model interactively: `python infer.py`