# Copyright 2019-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from __future__ import absolute_import
import logging
import os
import base64
import sys
import io
from pathlib import Path

import json

import torch
import torchvision
from PIL import Image
import torchvision.transforms as transforms
import torchvision


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

# To use new EIA inference API, customer should use attach_eia(model, eia_ordinal_number)
# VERSIONS_USE_NEW_API = ["1.8.1"]


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


def input_fn(request_body, request_content_type):

    """An input_fn that loads a pickled tensor"""

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if request_content_type == "application/x-b64-image":

        logger.info(request_body[:20])

        if isinstance(request_body, str):
            request_body = request_body.encode()

        img_bytes = base64.b64decode(request_body)

        return transform_image(img_bytes)
    else:
        # Handle other content-types here or raise an Exception
        # if the content type is not supported.
        pass


def model_fn(model_dir):

    logger.error(os.listdir())

    # model_dir = Path(model_dir) / "best_model.pth"

    logger.error(list(Path(model_dir).iterdir()))

    model_dir = Path("./modelcom") / "best_model.pth"

    model = torchvision.models.resnet18(pretrained=True)

    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 2)

    for param in model.parameters():
        param.requires_grad = False

    model.load_state_dict(torch.load(str(model_dir)))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model.to(device)

    model.eval()

    # model = model.eval()

    return model


def predict_fn(input_data, model):

    # input_data is the returned value from input_fn
    # The return value should be of the correct type to be passed as the first argument to output_fn. If you use the default output_fn,
    # this should be a torch.Tensor.

    # with torch.jit.optimized_execution(True, {"target_device": "eia:0"}):
    with torch.no_grad():
        outputs = model(input_data)
        _, y_hat = outputs.max(1)

    return str(y_hat.item())

    # with torch.no_grad():
    #   return model(input_data.to(device))


def output_fn(prediction, content_type):

    data = json.dumps({"result": prediction})

    return data
