## Introduction
ZFScripting is a scripting build by Python for logging in Zhengfang system.

## Dependencies
* request

## Usage
### 1. Label the images
run the ```InputLabel.py``` and then open ```http://127.0.0.1:5000``` in your Browser. The label you input will store in ```label.db``` and images in ```./images/```
### 2. Convert them to train data
run the ```DataTool.py```, the images will be filter for noice reduction and each of them will be divided into 4 parts. Then each of part is reshaped into 1-D numpy array. Finally put them in X that is a 2-D numpy array. The labels you input which stored in ```label.db``` will be divided into 4 parts as well and mapped to integers range from 0 to 35, stored in Y, a 1-D numpy array.

### 3. Train the model


## Versions in the future
|Version|things to do|
|:------|:-----------|
|0.1|get picture samples from ZF|
|0.2|reduce the noise of the pictures with image processing|
|0.4|obtain the labels from user input or download dataset from Internet|
|0.7|train a model from the dataset with probability over 50%|
|0.9|log in ZF with the CAPTCHA recognition program|
|1.0|finish the GUI section|