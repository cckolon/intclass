from ml_modules.training import trainer
from settings import MODEL_DIRECTORY, MODEL_NAME

if __name__ == "__main__":
    trainer.train()
    trainer.evaluate()

    trainer.save_model(f"{MODEL_DIRECTORY}/{MODEL_NAME}")
