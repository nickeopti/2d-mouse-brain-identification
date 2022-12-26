import os
import sys

sys.path.insert(0, os.getcwd())

import argparse

from mbi.utils.metrics import Metrics
from mbi.data_loader.base_data_loader import BaseDataLoader
from mbi.data_loader.data_loader import TripletDataLoader
from mbi.models.base_model import BaseModel
from mbi.models.resnet50 import ResNet50V2Model
from mbi.paths import PATHS


def predict(model: BaseModel, data_loader: BaseDataLoader, image_path: str):
    model.compile_model()

    metrics_val = Metrics(data_loader, model=model, dataset_path=PATHS.TEST_PATH)
    predictions = metrics_val.predict(image_path)

    return predictions


def prepare(img_size: int, weights_path: str):
    try:
        if img_size < 224:
            raise Exception("Image size should be bigger than 224")
    except ValueError:
        raise Exception("Provide a correct image size")

    input_shape = (img_size, img_size, 3)
    data_loader = TripletDataLoader(input_shape=input_shape)
    model = ResNet50V2Model(
        input_shape=input_shape, imagenet=False, weights_path=weights_path
    )

    return model, data_loader


def main():
    parser = argparse.ArgumentParser(
        description="Predict atlas plate for image"
    )
    parser.add_argument("image", help="The image to predict atlas plate for")
    parser.add_argument("image_size", type=int, help="The size of images (224 or 1024)")
    parser.add_argument("weights", help="Path to model weights")
    args = parser.parse_args()

    model, data_loader = prepare(args.image_size, args.weights)

    predictions = predict(model, data_loader, args.image)
    print(predictions)


if __name__ == "__main__":
    main()
