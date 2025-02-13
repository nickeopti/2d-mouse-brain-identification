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


def evaluate(
    model: BaseModel, data_loader: BaseDataLoader, weights: str, visualize: bool = False
):
    model.compile_model()
    # model.load(weights)

    # compute MAE
    metrics_val = Metrics(data_loader, model=model, dataset_path=PATHS.TEST_PATH)
    mae = metrics_val.compute(visualize=visualize)

    return mae


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate trained ResNet50v2 on the test dataset"
    )
    parser.add_argument("image_size", help="The size of images (224 or 1024)")
    parser.add_argument("weights", help="Path to model weights")
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help="Visualize predicted atlas plates",
    )
    args = parser.parse_args()

    try:
        img_size = int(args.image_size)
        if img_size < 224:
            raise Exception("Image size should be bigger than 224")
    except ValueError:
        raise Exception("Provide a correct image size")

    input_shape = (img_size, img_size, 3)
    data_loader = TripletDataLoader(input_shape=input_shape)
    model = ResNet50V2Model(
        input_shape=input_shape, imagenet=False, weights_path=args.weights
    )
    evaluate(model, data_loader, weights=args.weights, visualize=args.visualize)


if __name__ == "__main__":
    main()
