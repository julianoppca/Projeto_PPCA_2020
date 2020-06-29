# Sample module in the public domain. Feel free to use this as a template
# for your modules (and you can remove this header and take complete credit
# and liability)
#
# Contact: Brian Carrier [carrier <at> sleuthkit [dot] org]
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# Simple data source-level ingest module for Autopsy.
# Search for TODO for the things that you need to change
# See http://sleuthkit.org/autopsy/docs/api-docs/4.4/index.html for documentation


from java.io import File
import java.util.ArrayList as ArrayList
from java.lang import ProcessBuilder
from org.sleuthkit.autopsy.coreutils import ExecUtil
#from pathlib import Path
from os.path import basename





import jarray
import inspect
import os
from java.io import File
from java.lang import System
from java.util.logging import Level
from org.sleuthkit.datamodel import SleuthkitCase
from org.sleuthkit.datamodel import AbstractFile
from org.sleuthkit.datamodel import ReadContentInputStream
from org.sleuthkit.datamodel import BlackboardArtifact
from org.sleuthkit.datamodel import BlackboardAttribute
from org.sleuthkit.autopsy.ingest import IngestModule
from org.sleuthkit.autopsy.ingest.IngestModule import IngestModuleException
from org.sleuthkit.autopsy.ingest import DataSourceIngestModule
from org.sleuthkit.autopsy.ingest import FileIngestModule
from org.sleuthkit.autopsy.ingest import IngestModuleFactoryAdapter
from org.sleuthkit.autopsy.ingest import IngestMessage
from org.sleuthkit.autopsy.ingest import IngestServices
from org.sleuthkit.autopsy.coreutils import Logger
from org.sleuthkit.autopsy.casemodule import Case
from org.sleuthkit.autopsy.casemodule.services import Services
from org.sleuthkit.autopsy.casemodule.services import FileManager
from org.sleuthkit.autopsy.casemodule.services import Blackboard
from org.sleuthkit.autopsy.datamodel import ContentUtils




from java.util import UUID
from java.lang import Class
from java.lang import System
from java.sql  import DriverManager, SQLException
from java.util.logging import Level
from java.io import File
from org.sleuthkit.datamodel import SleuthkitCase
from org.sleuthkit.datamodel import AbstractFile
from org.sleuthkit.datamodel import ReadContentInputStream
from org.sleuthkit.datamodel import BlackboardArtifact
from org.sleuthkit.datamodel import BlackboardAttribute
from org.sleuthkit.datamodel import Image
from org.sleuthkit.datamodel.TskData import DbType
from org.sleuthkit.autopsy.ingest import IngestModule
from org.sleuthkit.autopsy.ingest.IngestModule import IngestModuleException
from org.sleuthkit.autopsy.ingest import DataSourceIngestModule
from org.sleuthkit.autopsy.ingest import IngestModuleFactoryAdapter
from org.sleuthkit.autopsy.ingest import IngestModuleIngestJobSettings
from org.sleuthkit.autopsy.ingest import IngestModuleIngestJobSettingsPanel
from org.sleuthkit.autopsy.ingest import IngestMessage
from org.sleuthkit.autopsy.ingest import IngestServices
from org.sleuthkit.autopsy.ingest import IngestManager
from org.sleuthkit.autopsy.ingest import ModuleDataEvent
from org.sleuthkit.autopsy.ingest import ModuleContentEvent
from org.sleuthkit.autopsy.coreutils import Logger
from org.sleuthkit.autopsy.coreutils import PlatformUtil
from org.sleuthkit.autopsy.casemodule import Case
from org.sleuthkit.autopsy.casemodule.services import Services
from org.sleuthkit.autopsy.casemodule.services import FileManager
from org.sleuthkit.autopsy.datamodel import ContentUtils
from org.sleuthkit.autopsy.casemodule import AddLocalFilesTask
from org.sleuthkit.autopsy.casemodule.services.FileManager import FileAddProgressUpdater
from org.sleuthkit.autopsy.ingest import ModuleContentEvent

# Factory that defines the name and details of the module and allows Autopsy
# to create instances of the modules that will do the analysis.
# TODO: Rename this to something more specific. Search and replace for it because it is used a few times
class ImageClassificationVGGIngestModuleFactory(IngestModuleFactoryAdapter):

    # TODO: give it a unique name.  Will be shown in module list, logs, etc.
    moduleName = "Image Classifier using VGG16"

    def getModuleDisplayName(self):
        return self.moduleName

    # TODO: Give it a description
    def getModuleDescription(self):
        return "Image classification using VGG16"

    def getModuleVersionNumber(self):
        return "1.0"

    def isDataSourceIngestModuleFactory(self):
        return True

    def createDataSourceIngestModule(self, ingestOptions):
        # TODO: Change the class name to the name you'll make below
        return ImageClassificationVGGIngestModule()


# Data Source-level ingest module.  One gets created per data source.
# TODO: Rename this to something more specific. Could just remove "Factory" from above name.
class ImageClassificationVGGIngestModule(DataSourceIngestModule):

    _logger = Logger.getLogger(ImageClassificationVGGIngestModuleFactory.moduleName)

    def log(self, level, msg):
        self._logger.logp(level, self.__class__.__name__, inspect.stack()[1][3], msg)

    def __init__(self):
        self.context = None

    # Where any setup and configuration is done
    # 'context' is an instance of org.sleuthkit.autopsy.ingest.IngestJobContext.
    # See: http://sleuthkit.org/autopsy/docs/api-docs/4.4/classorg_1_1sleuthkit_1_1autopsy_1_1ingest_1_1_ingest_job_context.html
    # TODO: Add any setup code that you need here.
    def startUp(self, context):
        exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model\\image_classifier.exe")
        self.log(Level.INFO, "PATH EXE ***** " + exe_path)
        self.pathToEXE = File(exe_path)
        if not self.pathToEXE.exists():
            raise IngestModuleException("EXE was not found in module folder")


        # Throw an IngestModule.IngestModuleException exception if there was a problem setting up
        #raise IngestModuleException("Oh No!")
        pass
 

        
        # Throw an IngestModule.IngestModuleException exception if there was a problem setting up
        # raise IngestModuleException("Oh No!")
        self.context = context

    # Where the analysis is done.
    # The 'dataSource' object being passed in is of type org.sleuthkit.datamodel.Content.
    # See: http://www.sleuthkit.org/sleuthkit/docs/jni-docs/4.4/interfaceorg_1_1sleuthkit_1_1datamodel_1_1_content.html
    # 'progressBar' is of type org.sleuthkit.autopsy.ingest.DataSourceIngestModuleProgress
    # See: http://sleuthkit.org/autopsy/docs/api-docs/4.4/classorg_1_1sleuthkit_1_1autopsy_1_1ingest_1_1_data_source_ingest_module_progress.html
    # TODO: Add your analysis code in here.
    def process(self, dataSource, progressBar):

        # we don't know how much work there is yet
        progressBar.switchToIndeterminate()

        # Use blackboard class to index blackboard artifacts for keyword search
        blackboard = Case.getCurrentCase().getServices().getBlackboard()

        # For our example, we will use FileManager to get all
        # files with the word "test"
        # in the name and then count and read them
        # FileManager API: http://sleuthkit.org/autopsy/docs/api-docs/4.4/classorg_1_1sleuthkit_1_1autopsy_1_1casemodule_1_1services_1_1_file_manager.html
        
        #Localiza arquivov .jpg
        fileManager = Case.getCurrentCase().getServices().getFileManager()
        imagefiles_jpg = fileManager.findFiles(dataSource, "%.jpg")
        imagefiles_jpeg = fileManager.findFiles(dataSource, "%.jpeg")
        imagefiles_png = fileManager.findFiles(dataSource, "%.png")
        imagefiles_bmp = fileManager.findFiles(dataSource, "%.bmp")

        imagefiles = imagefiles_jpg + imagefiles_jpeg + imagefiles_png + imagefiles_bmp

        numFiles = len(imagefiles)
        self.log(Level.INFO, "found " + str(numFiles) + " files")
        progressBar.switchToDeterminate(numFiles)
        fileCount = 0


        # Create Reports Directory, if it exists then continue on processing		
        reportsDir = os.path.join(Case.getCurrentCase().getCaseDirectory(), "Relatorio")
        self.log(Level.INFO, "create Directory " + reportsDir)
        try:
		    os.mkdir(reportsDir)
        except:
		    self.log(Level.INFO, "Reports Directory already exists " + reportsDir)

        arq_lista_images = open(reportsDir + "\saida.txt", "w")


        
        for file in imagefiles:

            # Check if the user pressed cancel while we were busy
            if self.context.isJobCancelled():
                return IngestModule.ProcessResult.OK

            #self.log(Level.INFO, "Processing file: " + lclDbPath)
            self.log(Level.INFO, "### Processing file: " + file.getLocalPath())
            arq_lista_images.write("%s\n" % file.getLocalPath())
            fileCount += 1
            
        arq_lista_images.close()

        ######### CLASSIFICACAO DE IMAGENS ###############
        # Run the EXE, saving output to reportFile
        self.log(Level.INFO, "##################### Running program on data source")
        cmd = ArrayList()
        cmd.add(self.pathToEXE.toString())
        # Adiciona o argumento para o executavel: path da pasta de relatorios
        cmd.add(reportsDir)



        processBuilder = ProcessBuilder(cmd)
        self.log(Level.WARNING, "AQUI!!!!!!!")
        resultado = ExecUtil.execute(processBuilder)
            
        self.log(Level.WARNING, "------------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>" + str(resultado))


        ###### Exibe as imagens com DOCUMENTOS DE IDENTIFICACAO
        arq_lista_docs_id = open(reportsDir + "\images_docs_id.txt", "r")
        lines = arq_lista_docs_id.readlines() 
        fileManager = Case.getCurrentCase().getServices().getFileManager()

        for line in lines:           
            line = line.strip('\n')
            path, filename = os.path.split(line)
            parent_dir = os.path.basename(os.path.dirname(line)) + "/"
            #self.log(Level.INFO, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> Diretorio " + parent_dir)
            #self.log(Level.INFO, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> Arquivo " + filename)

            arquivo = fileManager.findFiles(dataSource, filename , parent_dir)

            numFiles2 = len(arquivo)
            #self.log(Level.INFO, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> found " + str(numFiles2) + " files")

            if arquivo:
                art = arquivo[0].newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
                att = BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_SET_NAME, ImageClassificationVGGIngestModuleFactory.moduleName, "Documentos_ID")
                art.addAttribute(att)

                try:
                    # index the artifact for keyword search
                    blackboard.indexArtifact(art)
                except Blackboard.BlackboardException as e:
                    self.log(Level.SEVERE, "Error indexing artifact " + art.getDisplayName())
                
                arquivo.clear()   
        arq_lista_docs_id.close()
        
        ###### Exibe as imagens com DOCUMENTOS GERAIS
        lines = []
        arq_lista_docs_gerais = open(reportsDir + "\images_docs_general.txt", "r")
        lines = arq_lista_docs_gerais.readlines() 
        fileManager = Case.getCurrentCase().getServices().getFileManager()

        for line in lines:           
            line = line.strip('\n')
            path, filename = os.path.split(line)
            parent_dir = os.path.basename(os.path.dirname(line)) + "/"
            #self.log(Level.INFO, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> Diretorio " + parent_dir)
            #self.log(Level.INFO, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> Arquivo " + filename)

            arquivo = fileManager.findFiles(dataSource, filename , parent_dir)

            numFiles2 = len(arquivo)
            #self.log(Level.INFO, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> found " + str(numFiles2) + " files")

            if arquivo:
                art = arquivo[0].newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
                att = BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_SET_NAME, ImageClassificationVGGIngestModuleFactory.moduleName, "Documentos_gerais")
                art.addAttribute(att)

                try:
                    # index the artifact for keyword search
                    blackboard.indexArtifact(art)
                except Blackboard.BlackboardException as e:
                    self.log(Level.SEVERE, "Error indexing artifact " + art.getDisplayName())
                
                arquivo.clear()   
                
        arq_lista_docs_gerais.close()


            
        """




            # Make an artifact on the blackboard.  TSK_INTERESTING_FILE_HIT is a generic type of
            # artfiact.  Refer to the developer docs for other examples.
            art = file.newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
            att = BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_SET_NAME, ImageClassificationIngestModuleFactory.moduleName, "Whastapp Contacts Detected")
            art.addAttribute(att)

            try:
                # index the artifact for keyword search
                blackboard.indexArtifact(art)
            except Blackboard.BlackboardException as e:
                self.log(Level.SEVERE, "Error indexing artifact " + art.getDisplayName())
            # Update the progress bar
            progressBar.progress(fileCount)


        chatFiles = fileManager.findFiles(dataSource, "msgstore.db")
        #BitTorrentForensic = fileManager.findFiles(dataSource, "%", "/Roaming/BitTorrent")

        numFiles = len(chatFiles)
        self.log(Level.INFO, "found " + str(numFiles) + " files")
        progressBar.switchToDeterminate(numFiles)
        fileCount = 0
        for file in chatFiles:

            # Check if the user pressed cancel while we were busy
            if self.context.isJobCancelled():
                return IngestModule.ProcessResult.OK

            self.log(Level.INFO, "Processing file: " + file.getName())
            fileCount += 1

            lclDbPath = os.path.join(Case.getCurrentCase().getTempDirectory(), str(file.getId()) +  "-" + str(file.getName()) + ".db")
            ContentUtils.writeToFile(file, File(lclDbPath))

            # Make an artifact on the blackboard.  TSK_INTERESTING_FILE_HIT is a generic type of
            # artfiact.  Refer to the developer docs for other examples.
            art = file.newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
            att = BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_SET_NAME, ImageClassificationIngestModuleFactory.moduleName, "Whastapp Contacts Detected")
            art.addAttribute(att)

            try:
                # index the artifact for keyword search
                blackboard.indexArtifact(art)
            except Blackboard.BlackboardException as e:
                self.log(Level.SEVERE, "Error indexing artifact " + art.getDisplayName())
            # Update the progress bar
            progressBar.progress(fileCount)

        #Post a message to the ingest messages in box.
        message = IngestMessage.createMessage(IngestMessage.MessageType.DATA,
            "Finished search for whatsapp", "Found %d files" % fileCount)
        IngestServices.getInstance().postMessage(message)


        """

        

        return IngestModule.ProcessResult.OK