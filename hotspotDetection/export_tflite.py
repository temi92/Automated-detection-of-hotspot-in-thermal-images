# -*- coding: utf-8 -*-
"""
Created on Mon May  4 21:26:50 2020

@author: Drones
"""
import tensorflow as tf

IMG_SIZE = (224, 224, 3)
model = tf.keras.applications.MobileNetV2(input_shape=(IMG_SIZE),include_top = False, weights="imagenet")

converter = tf.lite.TFLiteConverter.from_keras_model(model)

tflite_model = converter.convert()
file = open("mobileNetv2.tflite", "wb")
file.write(tflite_model)
