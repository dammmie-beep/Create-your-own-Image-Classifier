# Create-your-own-Image-Classifier
## Overview
This project is part of the AI Programming with Python Nanodegree by Udacity. It entails developing an image classifier using PyTorch, followed by transforming it into a command-line application.

## Installation
Ensure you have Python installed along with the following libraries:

PyTorch
ArgParse
JSON
PIL (Python Imaging Library)
NumPy
Pandas
Matplotlib
Scikit-learn

For running iPython Notebooks, it's recommended to install Anaconda, which packages all the required libraries and software for this project.

## Usage
### Jupyter Notebook
To view the Jupyter Notebook, navigate to the main project directory and run one of the following commands:
```
ipython notebook Image Classifier Project.ipynb
# or
jupyter notebook Image Classifier Project.ipynb
```
This will open the project file in your browser through the iPython Notebook software.

## Command Line Application
Navigate to the main project directory for the following functionalities:

### Training the Network
```
# Basic usage
python train.py data_directory

# Options
python train.py data_dir --save_dir save_directory  # Set checkpoint save directory
python train.py data_dir --arch "vgg13"            # Choose model architecture
python train.py data_dir --learning_rate 0.01 --hidden_units 512 --epochs 20  # Set hyperparameters
python train.py data_dir --gpu                     # Use GPU for training
```

### Making Predictions
```
# Basic usage
python predict.py /path/to/image checkpoint

# Options
python predict.py input checkpoint --top_k 3                      # Return top K classes
python predict.py input checkpoint --category_names cat_to_name.json  # Map categories to names
python predict.py input checkpoint --gpu                          # Use GPU for inference
```

Note: Replace data_directory, data_dir, /path/to/image, and input with actual paths as needed.
