"""
Following this tutorial
https://huggingface.co/docs/transformers/en/tasks/sequence_classification
Fine-tuning MathBERT
https://huggingface.co/tbs17/MathBERT
"""

import os

import evaluate
import numpy as np
from transformers import (
    AutoModelForSequenceClassification,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

from data_generation.load_training_data import success_fail_dataset
from ml_modules.shared import tokenizer
from settings import MODEL_DIRECTORY

os.makedirs(MODEL_DIRECTORY, exist_ok=True)

accuracy = evaluate.load("accuracy")


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)


id2label = {0: "FAILURE", 1: "SUCCESS"}
label2id = {"FAILURE": 0, "SUCCESS": 1}


def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
    )


training_set = success_fail_dataset["train"].map(tokenize_function)
test_set = success_fail_dataset["test"].map(tokenize_function)

model = AutoModelForSequenceClassification.from_pretrained(
    "tbs17/MathBERT",
    num_labels=2,
    id2label=id2label,
    label2id=label2id,
)

training_args = TrainingArguments(
    output_dir=f"{MODEL_DIRECTORY}/checkpoints",
    learning_rate=1e-5,
    num_train_epochs=3,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    eval_strategy="steps",
)

trainer = Trainer(
    model=model,
    args=training_args,
    compute_metrics=compute_metrics,
    train_dataset=training_set,
    eval_dataset=test_set,
    data_collator=DataCollatorWithPadding(tokenizer),
)
