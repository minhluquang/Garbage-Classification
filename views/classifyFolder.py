from PyQt6.QtWidgets import QMainWindow, QLabel, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
import os
# import tensorflow as tf
# from tensorflow.keras.models import load_model
import cv2
import numpy as np
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class ClassifyFolder(QMainWindow):  
  def __init__(self, widget):
    super(ClassifyFolder, self).__init__()
    loadUi("ui/classifyFolder.ui", self)  
    self.widget = widget
    self.lbl_predicting.hide()
    self.lbl_result.hide()

    # self.btn_predict.clicked.connect(self.handle_predict)
    self.btn_input_folder.clicked.connect(self.openFolderDialog)
  

    # model_path = os.path.join(os.path.dirname(__file__), "../models/resnet50.h5")
    # self.model = load_model(model_path) 


  def openFolderDialog(self):
    folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")

    if not folder_path:  
      return

    image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
    image_files = [
      os.path.join(folder_path, file)
      for file in os.listdir(folder_path)
      if file.lower().endswith(image_extensions)
    ]

    print("Image Files:", image_files)
    # Set image_files to self....

  # def handle_predict(self):
    # Your logic is here


