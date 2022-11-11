"""
Two Neural Networks are used here:

'vggface_resnet50' - a NN with ResNet50 architecture,
trained on VGGFace2: a dataset for recognising faces across pose and age.
This model is able to predict a celebrity on the images.
'predict_celebrity' function uses this model.

Multitask Neural Network
is built on top of the 'vggface_resnet50'
has three outputs, which predict a gender, a race and an age
'predict_person' function uses this model.
"""
import base64
from http.client import HTTPException

import requests
from io import BytesIO
from pathlib import Path
from PIL import Image

import numpy as np
import tensorflow as tf

from keras.models import load_model

from keras_vggface import utils

# VGGface Model works with images 224 x 224
IMAGE_SIZE = 224


def predict_person_base64img(base64img: str) -> str:
    """
    1. converts: a string (with the image in base64) -> to bytes -> to image
    2. calls 'predict_person' function to get a prediction
    """
    base64_img_bytes = base64img.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    img_bytes = BytesIO(decoded_image_data)
    img = Image.open(img_bytes)
    img = img.convert('RGB')
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE))

    return predict_person(img)


def predict_person_url(img_url: str) -> str:
    """
    1. Reads the image from bytes (response.content)
    2. Calls 'predict_person' function to get a prediction
    """
    img_url = "https://udemyinsta.s3.eu-north-1.amazonaws.com/70470690-5c68-47ca-9fa9-79eb0f0e6fde.jpg"
    try:
        response = requests.get(img_url)
    except Exception as ex:
        raise HTTPException(500, "S3 is not available")
    img_bytes = BytesIO(response.content)
    img = Image.open(img_bytes)
    img = img.convert('RGB')
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE))

    return predict_person(img)


def predict_person_path(img_url: str) -> str:
    """
    1. Reads the image from os.PathLike
    2. Calls 'predict_person' function to get a prediction
    """
    # img_url = "img/me_2.jpg"
    img_url = "img/brad_pitt.jpg"
    img = tf.keras.utils.load_img(img_url, target_size=(IMAGE_SIZE, IMAGE_SIZE))

    return predict_person(img)


def predict_person(img) -> str:
    """
    Loads a trained Multitask Neural Network,
    which is able to predict: gender, race and age of a person.
    The Multitask NN is based on 'resnet50' model,
    which was trained to detect celebrities on pictures.

    Returns predictions.
    """

    # These are mappings that were used during learning the Multitask NN model
    gender_mapping = {0: 'Male', 1: 'Female'}
    race_mapping = dict(list(enumerate(('White', 'Black', 'Asian', 'Indian', 'Others'))))
    max_age = 120

    path = Path("ckpt")
    ckpt_filename = "checkpoint_best.h5"
    ckpt_path = str(path / ckpt_filename)
    model_multitask = load_model(ckpt_path)

    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    # we are using resnet50 - therefore version2
    x = utils.preprocess_input(x, version=2)
    predicted_labels = model_multitask.predict(x)
    gender, race, age = \
        int(predicted_labels[0][0] > 0.5), np.argmax(predicted_labels[1][0]), predicted_labels[2][0]

    gender_mapped = gender_mapping[gender]
    race_mapped = race_mapping[race]
    age_abs = int(age[0] * max_age)

    return f"gender: {gender_mapped}, race: {race_mapped}, age: {age_abs}"


def predict_celebrity_base64img(base64img: str) -> str:
    """
    1. converts: a string (with the image in base64) -> to bytes -> to image
    2. calls 'predict_celebrity' function to get a prediction
    """
    base64_img_bytes = base64img.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    img_bytes = BytesIO(decoded_image_data)
    img = Image.open(img_bytes)
    img = img.convert('RGB')
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE))

    return predict_celebrity(img)


def predict_celebrity(img) -> str:
    """
    Loads a trained 'resnet50' Neural Network,
    which is able to predict celebrities on pictures.

    Returns a prediction.
    """
    path = Path("ckpt")
    cpkt_filename = "resnet50face.h5"
    ckpt_path = str(path / cpkt_filename)

    vggface_model = load_model(ckpt_path)

    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    # we are using resnet50 -- therefore version2
    x = utils.preprocess_input(x, version=2)

    predictions = vggface_model.predict(x)
    res = utils.decode_predictions(predictions)[0][0]

    accuracy = res[1]
    accuracy = accuracy.item()

    if accuracy < 0.7:
        person = "not yet known"
    else:
        # the model gives a result in the form "b' Brad_Pitt'"
        person = res[0][3:-1]

    return f"name: {person}"
