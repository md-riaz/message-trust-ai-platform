import os
import fasttext

MODEL_PATH = "app/models/clear_sender_model.bin"


def train_model(training_file_path: str) -> bool:
    model = fasttext.train_supervised(
        input=training_file_path,
        epoch=25,
        lr=1.0,
        wordNgrams=2,
        dim=100,
    )
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    model.save_model(MODEL_PATH)
    return True
