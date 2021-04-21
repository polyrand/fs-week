
Here's an example to train a new model.

In order to run the training script use:

```
python3 train.py --download-data
python3 train.py --train --epochs 2 --optmizer adam
```

When the training finishes, the best model weights will be saved to a file called `best_model.pth`.


**NOTE**: The `train.py` script is still missing some features. Feel free to implement them:

* Choosing the folder to save the downloaded data
* Choosing the name and folder to save the best model
* Whatever comes to your mind!