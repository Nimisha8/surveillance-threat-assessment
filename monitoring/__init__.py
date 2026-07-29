import os
from importlib.resources import files


def resource_filename(package, resource):
    # Modern replacement for the deprecated pkg_resources.resource_filename
    return str(files(package) / resource)


def pose_predictor_model_location():
    return resource_filename(__name__, "models/shape_predictor_68_face_landmarks.dat")


def pose_predictor_five_point_model_location():
    return resource_filename(__name__, "models/shape_predictor_5_face_landmarks.dat")


def face_recognition_model_location():
    return resource_filename(__name__, "models/dlib_face_recognition_resnet_model_v1.dat")


def cnn_face_detector_model_location():
    return resource_filename(__name__, "models/mmod_human_face_detector.dat")