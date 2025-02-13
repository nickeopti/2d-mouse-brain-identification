import os
import sys
import glob
import argparse
from tqdm import tqdm
import numpy as np

sys.path.insert(0, os.getcwd())

from mbi.trainers.base_trainer import BaseTrain
from mbi.models.base_model import BaseModel
from mbi.data_loader.base_data_loader import BaseDataLoader
from mbi.data_loader.data_loader import TripletDataLoader
from mbi.models.resnet50 import ResNet50V2Model
from mbi.utils.metrics import Metrics
from mbi.paths import PATHS
from mbi.utils.cuda import set_cuda_memory
from mbi.utils.helper import create_folder_if_not_exists


class MainTrain(BaseTrain):
    def __init__(self, model: BaseModel, data_loader: BaseDataLoader, iters: int = 10_000):
        super().__init__(model, data_loader)
        self.iters = iters

    def train(self):
        self.model.compile_model()
        metrics = Metrics(
            self.data_loader, model=self.model, dataset_path=PATHS.VAL_PATH
        )

        # variables for saving models and logs
        save_dir = "output"
        base_file_name = (
            f"{self.model.get_model_name()}_{self.data_loader.input_shape[0]}"
        )
        log_path = os.path.join(save_dir, "logs", f"{base_file_name}.txt")
        create_folder_if_not_exists(log_path)

        # store logs of loss and mean absolute error
        losses = []
        avg_losses = []
        mae_val_list = []
        best_mae_list = []
        best_mae = None

        print(
            f"Training settings: input shape: {self.model.input_shape}, network: {self.model.get_model_name()}"
        )

        for i in tqdm(range(self.iters)):
            x, y = next(self.data_loader.get_train_data())
            loss = self.model.model.train_on_batch(x, y)
            losses.append(loss)

            if i % 5 == 0 and i != 0:
                avg_losses.append(np.mean(losses[-100:]))
                print(f"Average train loss in last 100 iterations: {avg_losses[-1]}")

                # compute Mean Absolute Error
                mae_val = metrics.compute()

                # if mae improved
                if not best_mae or mae_val < best_mae:
                    best_mae = mae_val
                    # delete existing models
                    for filename in glob.glob(f"{save_dir}/models/{base_file_name}*"):
                        print(f"Deleting {filename}")
                        os.remove(filename)
                    # save a new model
                    path = os.path.join(
                        save_dir,
                        "models",
                        base_file_name + f"_{best_mae}.hdf5",
                    )
                    create_folder_if_not_exists(path)
                    self.model.save(path)

                best_mae_list.append(best_mae)
                mae_val_list.append(mae_val)

                # save logs
                f = open(log_path, "w")
                for u in range(len(avg_losses)):
                    f.write(f"{avg_losses[u]}; {mae_val_list[u]}; {best_mae_list[u]}\n")
                f.close()


def main():
    parser = argparse.ArgumentParser(
        description="Train Siamese Networks with triplet semi-hard loss"
    )
    parser.add_argument("image_size", help="The size of images (224 or 1024)")
    parser.add_argument("--iters", type=int, default=10_000, help="Number of iterations to train for")
    args = parser.parse_args()

    try:
        img_size = int(args.image_size)
        if img_size < 224:
            raise Exception("Image size should be bigger than 224")
    except ValueError:
        raise Exception("Provide a correct image size")

    set_cuda_memory()

    input_shape = (img_size, img_size, 3)
    data_loader = TripletDataLoader(
        input_shape=input_shape, augmentation=True, batch_size=16
    )
    model = ResNet50V2Model(input_shape=input_shape, freeze=False, imagenet=True)
    trainer = MainTrain(model=model, data_loader=data_loader, iters=args.iters)
    trainer.train()


if __name__ == "__main__":
    main()
