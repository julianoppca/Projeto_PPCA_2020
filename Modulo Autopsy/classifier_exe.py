import sys
#sys.stdout.write("comecou a importar\n")
from keras import models
from keras.preprocessing import image
import tensorflow as tf
import numpy as np
import os


from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#sys.stdout.write("terminou de importar\n")

sys.stderr = open(os.devnull, "w")  # silence stderr
#sys.stderr = sys.__stderr__  # unsilence stderr
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.logging.set_verbosity(tf.logging.ERROR)
import warnings
warnings.filterwarnings("ignore")

# Não exibir warnings
def main():
    
    #arq_lista_docs_id = open('C:\saidas_previstas\images_docs_id.txt', 'w')  # ERRADO
    #arq_lista_general_docs = open('C:\saidas_previstas\images_general_docs.txt', 'w') # ERRADO

    #sys.stdout.write("Hello")
    #sys.stdout.write("entrou\n")
    
    #if (os.path.exists('C:\modelo_classificador_B_dist_05.h5')== True):
    #    sys.stdout.write("Achou arquivo do modelo\n")
    #else:
    #    sys.stdout.write("NAO Achou arquivo do modelo!!!!!\n")

    #model_A = models.load_model('C:\modelo_classificador_A_dist_05.h5')
    #model_B = models.load_model('C:\modelo_classificador_B_dist_05.h5')

    path_relatorios = sys.argv[1]
    
    model_A = models.load_model('.\model_A.h5')
    model_B = models.load_model('.\model_B.h5')
    
    classification_report = open(path_relatorios + "\classification_report.txt", "w")
    classification_report.write("CARREGOU MODELOS!!!")    
    
    
    
    #sys.stdout.write("carregou modelo\n")
    
    #file1 = open('C:\saida.txt', 'r') 
    

    
    arq_lista_image = open(path_relatorios + "\saida.txt", "r")
    arq_lista_docs_id = open(path_relatorios + "\images_docs_id.txt", "w")
    arq_lista_docs_general = open(path_relatorios + "\images_docs_general.txt","w")
    #classification_report = open(path_relatorios + "\classification_report.txt", "w")
    classification_report.write("ARQUIVOS CRIADOS COM SUCESSO!!!")
    
    lines = arq_lista_image.readlines() 

    for line in lines:
        path_nome_arquivo = line.strip("\n") 
        #print (path_nome_arquivo) #tira o \n do final
        
        classification_report.write("Analisando Arquivo %s\n" % path_nome_arquivo)
    
        img = image.load_img(path_nome_arquivo, target_size=(128,128))
        
        # Imagem valida
        if (img is not None):
            img_tensor = image.img_to_array(img)
            img_tensor = np.expand_dims(img_tensor, axis=0)
            img_tensor /= 255.
        
            #sys.stdout.write("carregou imagem: " + path_nome_arquivo)
        
            predicao = []
            #Preve se e DOCUMENTO OU NAO DOCUMENTO
            predicao = model_A.predict_classes(img_tensor)
            
            
            if (predicao[0]==0): #DOCUMENTO
                predicao = []
                
                # Model_B: verifica se e doc_id ou doc_geral
                predicao = model_B.predict_classes(img_tensor)
                
                if (predicao[0]==0): #docs gerais
                    arq_lista_docs_general.write("%s\n" % path_nome_arquivo)
                    classification_report.write(path_nome_arquivo + ";"+str(predicao[0])+"\n")
                    #sys.stdout.write(path_nome_arquivo + ";"+str(predicao[0]))
                else: #docs id
                    #sys.stdout.write(path_nome_arquivo+"\n")
                    #sys.stdout.write(path_nome_arquivo + ";"+str(predicao[0]))
                    classification_report.write(path_nome_arquivo + ";"+str(predicao[0])+"\n")
                    arq_lista_docs_id.write("%s\n" % path_nome_arquivo)
        else:
             classification_report.write("Arquivo corrompido %s\n")
        
            
    arq_lista_image.close()
    arq_lista_docs_id.close()
    arq_lista_docs_general.close()
            
    return #predicao[0]

if __name__ == "__main__":
    main()