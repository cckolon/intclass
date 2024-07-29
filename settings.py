import logging
import os

# database
MIGRATIONS_DIRECTORY = "migrations"
DATABASE_NAME = os.getenv("DATABASE_NAME", "postgres")
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASS = os.getenv("DATABASE_PASS", "secret")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "5432"))


# training data generation
INTEGRATION_VARIABLE_NAME = "x"
INTEGRATION_TIMEOUT = 5
GENERATION_TIMEOUT = 10
FUNCTION_COMPLEXITY = 10
DATA_GENERATION_BATCH_SIZE = 50
DATA_GENERATION_BATCH_TIMEOUT_SECONDS = 60

# models
MODEL_DIRECTORY = "models"
MODEL_NAME = "intclass"

# logging
LOG_LEVEL = logging.DEBUG

# multiprocessing
MAX_WORKERS = os.cpu_count()

# temporal
TEMPORAL_SERVER = os.getenv("TEMPORAL_SERVER", "localhost")
TEMPORAL_PORT = 7233
