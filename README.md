## Identifying 2D brain slices in a 2D reference atlas using Siamese Networks

This repository contains code for the following paper [[arXiv]](https://arxiv.org/abs/2109.06662):
> Justinas Antanavicius, Roberto Leiras, & Raghavendra Selvan. (2021). 
> Identifying partial mouse brain microscopy images from Allen reference atlas using a contrastively learned semantic space. 

## Dataset Directory Structure
        
	|-- data
	    |-- atlas            # The name of dataset
	        |-- 30.jpg       # The position of atlas plate
            |-- ...
        |-- train
            |-- 30.jpg       # The position of brain slice
            |-- ...
        |-- val
        |-- test

## Training

`% train --help `
```
usage: train [-h] [--iters ITERS] image_size

Train Siamese Networks with triplet semi-hard loss

positional arguments:
  image_size     The size of images (224 or 1024)

options:
  -h, --help     show this help message and exit
  --iters ITERS  Number of iterations to train for
```

By default, the Siamese Networks use ResNet50v2 as a base network. Paths to the images are specified in `paths.py`



## Testing

`% evaluate --help `
```
usage: evaluate [-h] [-v] image_size weights

Evaluate trained ResNet50v2 on the test dataset

positional arguments:
  image_size       The size of images (224 or 1024)
  weights          Path to model weights

options:
  -h, --help       show this help message and exit
  -v, --visualize  Visualize predicted atlas plates
```

## Citation
If you find this code useful in your research, please consider citing us:
```
@misc{antanavicius2021identifying,
      title={Identifying partial mouse brain microscopy images from Allen reference atlas using a contrastively learned semantic space}, 
      author={Justinas Antanavicius and Roberto Leiras and Raghavendra Selvan},
      year={2021},
      eprint={2109.06662},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```