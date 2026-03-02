import os
import fasttext

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "clear_sender_model.bin")

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return fasttext.load_model(MODEL_PATH)

def predict_message(model, text: str):
    # FastText predict expects a single line of text
    text = text.replace("\n", " ").replace("\r", " ")
    labels, probabilities = model.predict(text, k=2)
    
    results = []
    for label, prob in zip(labels, probabilities):
        results.append({
            "label": str(label),
            "probability": float(prob)
        })
    return results
