from parse_images import generate_images
from data_encoder import DatasetWriter
from sklearn.preprocessing import LabelEncoder
import numpy as np
import progressbar
import random
import os
import tensorflow as tf



config = tf.compat.v1.ConfigProto()
#config.gpu_options.per_process_gpu_memory_fraction = 0.3


config.gpu_options.allow_growth = True
session = tf.compat.v1.InteractiveSession(config=config)



TRAINING_IMAGES="../training_test_data/testing/test_images_1"
batch_size=32 #batch size pass through neural network..

#genereate and shuffle images..
image_paths = list(generate_images(TRAINING_IMAGES))
random.shuffle(image_paths)

# extract the class labels from the image paths then encode the
# labels
labels = [p.split(os.path.sep)[-2] for p in image_paths]
le = LabelEncoder()
labels = le.fit_transform(labels)

#load model..
print("loading network...")
model = tf.keras.applications.VGG16(weights="imagenet", include_top=False)

#write to HDF5 format
dataset = DatasetWriter((len(image_paths), 512*7*7), "features_testing.hdf5", "features",buff_size=1000)
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
    features = features.reshape((features.shape[0], 512 * 7 * 7))

    #add the features and labels to HDF5 
    dataset.add_chunk(features, batch_labels)
    pbar.update(i)
dataset.close()
pbar.finish()
