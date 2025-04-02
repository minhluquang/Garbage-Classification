from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
import os
import tensorflow as tf
import cv2
import numpy as np
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication 
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class Classify(QMainWindow):  
  def __init__(self, widget):
    super(Classify, self).__init__()
    loadUi("ui/classify.ui", self)  
    self.widget = widget
    self.lbl_result.hide()
    self.lbl_predict.hide()

    self.lbl_image.setAcceptDrops(True)  
    self.lbl_image.setScaledContents(False)  
    self.original_label_size = self.lbl_image.size()

    self.current_image_path = None
    self.btn_predict_file.clicked.connect(self.handle_predict)
    self.btn_choose_img_file.clicked.connect(self.openFileDialog)

    self.btn_predict_file.setEnabled(False)
    self.btn_predict_file.setStyleSheet("""
        QPushButton:disabled {
            background-color: #A0A0A0; 
            color: #ffffff; 
            border: 1px solid #808080; 
        }""")

    model_path = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "../models/densenet201.h5")
    )
    self.model = tf.keras.models.load_model(model_path)


  def openFileDialog(self):
    file_dialog = QFileDialog(self)
    file_dialog.setWindowTitle("Open File")
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)") 
    file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

    if file_dialog.exec():
      selected_files = file_dialog.selectedFiles()
      print("Selected File:", selected_files[0])
      self.set_image(selected_files[0])
      self.btn_predict_file.setEnabled(True)

  def dragEnterEvent(self, event):
    if event.mimeData().hasUrls():
      event.acceptProposedAction()
    else:
      event.ignore()

  def dragMoveEvent(self, event):
    if event.mimeData().hasUrls():
      event.acceptProposedAction()
    else:
      event.ignore()

  def dropEvent(self, event):
    if event.mimeData().hasUrls():
      file_path = event.mimeData().urls()[0].toLocalFile()
      valid_extensions = (".png", ".jpg", ".jpeg")
      if file_path.lower().endswith(valid_extensions):
        event.acceptProposedAction()
        self.set_image(file_path)
        self.btn_predict_file.setEnabled(True)
      else:
        event.ignore()
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Thông báo")
        msg.setText(f"Vui lòng chọn tập tin ảnh .png, .jpg, hoặc .jpeg!")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.exec()

  def set_image(self, file_path):
    self.lbl_path.setText(f"Image: {file_path}")

    self.lbl_result.hide()
    self.lbl_predict.hide()
    
    self.current_image_path = file_path
    original_pixmap = QPixmap(file_path)
        
    # Tính toán tỷ lệ khung hình
    image_ratio = original_pixmap.width() / original_pixmap.height()
    label_ratio = self.original_label_size.width() / self.original_label_size.height()
    
    # Tính toán kích thước mới cho label
    if image_ratio > label_ratio:  # Ảnh rộng hơn
      new_width = self.original_label_size.width()
      new_height = int(new_width / image_ratio)
    else:  # Ảnh cao hơn
      new_height = self.original_label_size.height()
      new_width = int(new_height * image_ratio)
    
    # Điều chỉnh kích thước label
    self.lbl_image.setFixedSize(new_width, new_height)
    
    # Scale ảnh theo kích thước mới của label
    scaled_pixmap = original_pixmap.scaled(
      new_width, 
      new_height,
      Qt.AspectRatioMode.KeepAspectRatio,
      Qt.TransformationMode.SmoothTransformation
    )
    
    self.lbl_image.setPixmap(scaled_pixmap)
    
    # Căn giữa label trong cửa sổ
    self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

  def handle_predict(self):
    if self.current_image_path:
        print(f"Predicting for: {self.current_image_path}")

        # Đọc ảnh và chuyển sang RGB
        img = cv2.imread(self.current_image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Resize đúng kích thước model yêu cầu (224, 224)
        img = cv2.resize(img, (224, 224))

        # Chuẩn hóa ảnh về khoảng [0,1]
        img_array = img.astype(np.float32) / 255.0

        # Thêm batch dimension (1, 224, 224, 3)
        img_array = np.expand_dims(img_array, axis=0)  # Sửa lỗi ở đây, dùng img_array thay vì img

        # Dự đoán
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)
        print(predictions)

        className = ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes', 'green-glass', 
            'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']

        confidence = np.max(predictions, axis=1)

        # Hiển thị kết quả
        self.lbl_predict.setText(f"{className[predicted_class[0]]} ({round(confidence[0] * 100, 2)}%)")
        self.lbl_result.show()
        self.lbl_predict.show()
    else:
        print("No image selected")


