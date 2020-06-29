from imageai.Detection import ObjectDetection
from imageai.Detection.Custom import CustomObjectDetection
import os
import filetype
import sys
import tensorflow as tf


from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#sys.stdout.write("terminou de importar\n")

sys.stderr = open(os.devnull, "w")  # silence stderr
#sys.stderr = sys.__stderr__  # unsilence stderr


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.logging.set_verbosity(tf.logging.ERROR)
import warnings
warnings.filterwarnings("ignore")


from keras import models
from keras.preprocessing import image
import tensorflow as tf
import numpy as np
import os

from pathlib import Path

import csv
import shutil




def main():
    
    if hasattr(sys, "_MEIPASS"):
        datadir_model = os.path.join(sys._MEIPASS, 'yolo.h5')
        datadir_model_gun = os.path.join(sys._MEIPASS, 'model_gun_detect.h5')
        datadir_model_gun_config = os.path.join(sys._MEIPASS, 'detection_gun_config.json')
    else:
        datadir_model = 'yolo.h5'
        datadir_model_gun = 'model_gun_detect.h5'
        datadir_model_gun_config = 'detection_gun_config.json'
      
    
        
    path_relatorios = sys.argv[1]
    detection_report = open(path_relatorios + "\detection_report.txt", "w")
    #classification_report.write("ENTROU NA FUNCAO!!!")    
    
    
    #classification_report = open(path_relatorios + "\classification_report.txt", "w")
    detection_report.write("CARREGOU MODELOS!!!")  


    
    execution_path = os.getcwd()
    
    # Detecção de pessoas e carros
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path , datadir_model))
    detector.loadModel()
    
    detection_report.write("CARREGOU PESSOAS!!!") 
    
    
    # Deteccção de armas
    detector_gun = CustomObjectDetection()
    detector_gun.setModelTypeAsYOLOv3()
    detector_gun.setModelPath(os.path.join(execution_path , datadir_model_gun))
    detector_gun.setJsonPath(os.path.join(execution_path , datadir_model_gun_config))
    detector_gun.loadModel()
    
    detection_report.write("CARREGOU ARMAS!!!")  
    
    
    arq_lista_image = open(path_relatorios + "\saida.csv", "r")
    
    path_pai = Path(path_relatorios).parent
    
    output_folder = os.path.abspath(str(path_pai) + '\\Deteccoes')
    person_folder = os.path.abspath(str(path_pai) + '\\Deteccoes\Pessoas')
    car_folder = os.path.abspath(str(path_pai) + '\\Deteccoes\Carros')
    gun_folder = os.path.abspath(str(path_pai) + '\\Deteccoes\Armas')

    
    try:
        os.mkdir(output_folder)
    except OSError:
        print ("Creation of the directory %s failed")
    else:
        print ("Successfully created the directory")
        
    
    if not os.path.exists(person_folder):
        os.mkdir(person_folder)
    if not os.path.exists(car_folder):
        os.mkdir(car_folder)
    if not os.path.exists(gun_folder):
        os.mkdir(gun_folder)
        
        
    detection_report.write(output_folder)
    
    
    lines = arq_lista_image.readlines() 
    
    
    #with open(path_relatorios +"\arquivo_deteccoes.csv", mode="w") as file:
    #    writer = csv.writer(file, delimiter=';')
        
    detection_report.write("\n**** Relatorio_deteccoes:" + path_relatorios + "\Relatorio_deteccoes.csv") 
    file = open(path_relatorios + "\Relatorio_deteccoes.csv","w") 
    
    for line in lines:
        path_nome_arquivo = line.strip("\n") 
        corrupt_check = filetype.guess(path_nome_arquivo)
         
        # Imagem valida
        if (corrupt_check is not None):
            
            detections_gun = detector_gun.detectObjectsFromImage(input_image=os.path.join(path_nome_arquivo), output_image_path=os.path.join(output_folder, os.path.basename(path_nome_arquivo)))
            
            # Deleta arquivo gerado se não foi detectada arma
            if (not detections_gun):
                detection_report.write("\nDELETANDO: " + os.path.join(output_folder, os.path.basename(path_nome_arquivo)))
                os.remove(os.path.join(output_folder, os.path.basename(path_nome_arquivo)))
            else: #detectou arma
                file.write("gun;" + line) 
                shutil.move(os.path.join(output_folder, os.path.basename(path_nome_arquivo)),gun_folder)
                continue




            # Detecta pessoas e carros
            custom_objects = detector.CustomObjects(person=True, car=True)
            detection_report.write("\nDetectando obj no arquivo: " + path_nome_arquivo)
            detections = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=os.path.join(path_nome_arquivo), output_image_path=os.path.join(output_folder, os.path.basename(path_nome_arquivo)), minimum_percentage_probability=30)
                
            # Deleta arquivo gerado se não foi detectado objetos
            if (not detections):
                detection_report.write("\nDELETANDO: " + os.path.join(output_folder, os.path.basename(path_nome_arquivo)))
                os.remove(os.path.join(output_folder, os.path.basename(path_nome_arquivo)))
                
            # Adiciona classe e path do arquivo ao csv e move o carquivo marcado para a pasta correspondente
            else:
                maxValue = max(detections, key=lambda x:x["percentage_probability"])
                #writer.writerow([maxValue.get("name"), execution_path]) # Exemplo: pessoa;C:/teste/image01.jpg 
                file.write(maxValue.get("name")+";" + line)
                
                if (maxValue.get("name")=="person"): #Move arquivo para a pasta Pessoa 
                    shutil.move(os.path.join(output_folder, os.path.basename(path_nome_arquivo)),person_folder)
                
                else: # move arquivo para a pasta Carro
                    shutil.move(os.path.join(output_folder, os.path.basename(path_nome_arquivo)),car_folder)
                    
                      
                
                
        
        else:
            detection_report.write("Arquivo corrompido %s\n")
        
    
    arq_lista_image.close()
    file.close()

            
    return 

if __name__ == "__main__":
    main()
