# Automated-detection-of-hotspot-in-thermal-images
A  CNN network trained for detecting hotspot in thermal imagery via transfer learning.
The binary detection method determines whether an image contains hotspots or not. 
A pre trained VGG16 keras model is used to extract arbitary feature vectors that globally describe the image. Based on the extracted features, a Logistic Regression classifier is trained on the features for image classification purposes. For images that contain hotspot, the hotspot regions are localised using Otsus's adaptive thresholding techniques.

## Instructions on using the VGG16 model for extracting features from training and testing data.

```bash
python feature_extraction.py [-h] -i IMAGES -o OUTPUT
optional arguments:
-h --help show this help message and exit
-i IMAGES, --images IMAGES path to input images
-o OUTPUT, --output OUTPATH path to output hdf5 file
```
### Example - Extracting features from training images
  ```python feature_extraction.py -i ../training_test_data/training/ -o features_training.hdf5```
  
### Example - Extracting features from testing images
  python feature_extraction.py -i ../training_test_data/testing/ -o features_testing.hdf5

Once the features have been extracted, a Logistric Regression model can be trained on the extracted features

```bash
python classifier.py [-h] -train TRAIN_HDF5 -test TEST_HDF5
optional arguments:
-h --help show this help message and exit
-train TRAIN_HDF5, --train_hdf5 TRAIN_HDF5 path to trained hdf5 file
-test TEST_HDF5, --test TEST_HDF5 path to test hdf5 file
```
### Example - Training a classifier on the extracted features
  ```python classifier.py -train features_training.hdf5 -test features.hdf5```
  Output from the python script would be a `model.cpickle` file
  
