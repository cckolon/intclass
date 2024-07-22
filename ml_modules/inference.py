import os

from transformers import AutoModelForSequenceClassification, pipeline

from ml_modules.shared import tokenizer
from settings import MODEL_DIRECTORY, MODEL_NAME

absolute_path = os.path.realpath(f"{MODEL_DIRECTORY}/{MODEL_NAME}")
model = AutoModelForSequenceClassification.from_pretrained(
    absolute_path
)

classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
    device=0,
)
