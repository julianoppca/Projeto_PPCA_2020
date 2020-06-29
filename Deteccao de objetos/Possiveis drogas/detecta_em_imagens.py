# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 15:23:59 2020

@author: spi112884
"""
from imageai.Detection.Custom import CustomObjectDetection
import os

arr = os.listdir('validation/images')


detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("detection_model-ex-011--loss-0007.150.h5")
detector.setJsonPath("json/detection_config.json")
detector.loadModel()

for imagem in arr:
    print (imagem)
    detections = detector.detectObjectsFromImage(input_image='validation/images/'+imagem, output_image_path=imagem)
    for detection in detections:
        print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])




