from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

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
    self.btn_predict.clicked.connect(self.handle_predict)

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
      event.acceptProposedAction()
      file_path = event.mimeData().urls()[0].toLocalFile()
      self.set_image(file_path)

  def set_image(self, file_path):
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
      print(f"Image path: {self.current_image_path}")
      # Thêm code xử lý predict ở đây
    else:
      print("No image selected")

