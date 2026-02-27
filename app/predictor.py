import os
import fasttext

MODEL_PATH = "app/models/clear_sender_model.bin"


def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return fasttext.load_model(MODEL_PATH)


def predict_message(model, text: str):
    labels, probabilities = model.predict(text, k=2)
    return {
        "labels": list(labels),
        "probabilities": [float(p) for p in probabilities],
    }
