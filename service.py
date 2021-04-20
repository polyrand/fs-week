import io
import json
from functools import lru_cache

from pathlib import Path

import torchvision.transforms as transforms
from PIL import Image
import torchvision
import torch

import logging

from flask import Flask, jsonify, request

MODELS_DIR = Path("models")
ASSETS_DIR = Path("assets")
MODEL_NAME = "best_model.pth"


@lru_cache()
def load_model():
    model = torchvision.models.resnet18(pretrained=True)

    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 2)

    for param in model.parameters():
        param.requires_grad = False

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model = model.to(device)

    class2idx = json.loads(Path(ASSETS_DIR / "class2idx.json").read_text())
    idx2class = {v: k for k, v in class2idx.items()}

    model.load_state_dict(torch.load(MODELS_DIR / MODEL_NAME))

    model = model.eval()

    return model, idx2class


app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():

    if request.method == "POST":
        # we will get the file from the request
        file = request.files["file"]
        # convert that to bytes
        img_bytes = file.read()
        # class_id, class_name = get_prediction(image_bytes=img_bytes)
        pred_class = get_prediction(image_bytes=img_bytes)
        return jsonify(pred_class)
        # return jsonify({"class_id": class_id, "class_name": class_name})


def transform_image(image_bytes):
    my_transforms = transforms.Compose(
        [
            transforms.Resize(235),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    model = load_model()[0]
    idx2class = load_model()[1]
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return idx2class[int(predicted_idx)]


if __name__ == "__main__":
    app.run()


# run with
# FLASK_ENV=development FLASK_APP=app.py flask run

# import requests

# resp = requests.post("http://localhost:5000/predict",
#                     files={"file": open('<PATH/TO/.jpg/FILE>/cat.jpg','rb')})
