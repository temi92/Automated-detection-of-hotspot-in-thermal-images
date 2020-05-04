from parse_images import generate_images
from data_encoder import DatasetWriter
from sklearn.preprocessing import LabelEncoder
import numpy as np
import progressbar
import random
import os
import tensorflow as tf
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to input images")
ap.add_argument("-o", "--output", required=True, help="path to output hdf5 file")
ap.add_argument("-c,", "--cnn", required = True,  choices=["mobilenet",  "vgg16"])
args = vars(ap.parse_args())

config = tf.compat.v1.ConfigProto()
#config.gpu_options.per_process_gpu_memory_fraction = 0.3


config.gpu_options.allow_growth = True
session = tf.compat.v1.InteractiveSession(config=config)



#note V166 model takes (512 x 7 x7 ) and mobileNet takes (1280 x 7 x7)
print("loading network...")
if args["cnn"] == "vgg16":
    model = tf.keras.applications.VGG16(weights="imagenet", include_top=False)
    shape = (512, 7, 7)
else:
    model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False)
    shape = (1280, 7, 7)


IMAGES = args["images"]
batch_size=32 #batch size pass through neural network..

#generate and shuffle images..
image_paths = list(generate_images(IMAGES))
random.shuffle(image_paths)

# extract the class labels from the image paths then encode the
# labels
labels = [p.split(os.path.sep)[-2] for p in image_paths]
le = LabelEncoder()
labels = le.fit_transform(labels)



#write to HDF5 format
dataset = DatasetWriter((len(image_paths), shape[0]* shape[1]* shape[2]), args["output"], "features",buff_size=1000)
dataset.store_class_labels(le.classes_)



# initialize the progress bar
widgets = ["Extracting Features from dataset: ", progressbar.Percentage(), " ",
progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=len(image_paths),widgets=widgets).start()


# loop over the images in patches
for i in np.arange(0, len(image_paths), batch_size):
    #extract the batch of images and labels
    batch_paths = image_paths[i:i + batch_size]
    batch_labels = labels[i:i + batch_size]
    batch_images = []

    #loop over images in the current batch

    for(j, image_path) in enumerate(batch_paths):
        #load image using keras..
        image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224,224))
        image = tf.keras.preprocessing.image.img_to_array(image)


        #preprocess images..

        image = np.expand_dims(image, axis=0)
        image = tf.keras.applications.imagenet_utils.preprocess_input(image)

        batch_images.append(image)

    #pass images through the network
    batch_images = np.vstack(batch_images)
    features = model.predict(batch_images, batch_size=batch_size)

    print (features.shape)
    #reshape the features..
    features = features.reshape((features.shape[0], shape[0]* shape[1]* shape[2]))

    #add the features and labels to HDF5 
    dataset.add_chunk(features, batch_labels)
    pbar.update(i)
dataset.close()
pbar.finish()

