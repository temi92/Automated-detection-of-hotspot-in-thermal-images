# Automated-detection-of-hotspot-in-thermal-images
A  CNN network trained for detecting hotspot in thermal imagery
The binary detection method determines whether an image contains hotspots globally. 
A pre trained VGG16 keras model is used to extract arbitary feature vectors that globally describe the image. Based on the extracted features, a Logistic Regression classifier is trained on the features for image classification purposes.

##Instructions on using the VGG16 model for extracting features from the image

```bash
python feature.py [-h] -i IMAGES -o OUTPUT
optional arguments:
-h --help show this help message and exit
-i IMAGES, --images IMAGES path to input images
-o OUTPUT, --output OUTPATH path to output hdf5 file
```
