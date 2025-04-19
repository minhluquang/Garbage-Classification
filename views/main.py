from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidgetItem, QStackedWidget, QLabel, QFrame, QMessageBox
from PyQt6.uic import loadUi
import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt  
from PyQt6.QtGui import QPixmap
from views.classify import Classify
from views.classifyFolder import ClassifyFolder
from views.login import Login  

class Main(QMainWindow):  
    def __init__(self, widget):
        super(Main, self).__init__()
        self.widget = widget 
        loadUi("ui/main.ui", self)

        pixmap = QPixmap("assets/logo/rYsmlp2i1B1SmuA1dU6WxHCF40StOs37.jpg")
        pixmap = pixmap.scaled(int(self.lbl_logo.width() * 2.5),  
                       int(self.lbl_logo.height() * 2.5),  
                       Qt.AspectRatioMode.KeepAspectRatio,  
                       Qt.TransformationMode.SmoothTransformation)  
        self.lbl_logo.setPixmap(pixmap)
        self.lbl_logo.setScaledContents(False)  
        self.lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.hide()

        self.btn_predict_file.setIcon(QIcon("assets/icon/image-gallery.png"))
        self.btn_predict_file.setIconSize(QSize(24, 24)) 
        self.btn_predict_file.setStyleSheet("padding-left: 10px; text-align: left;")

        self.btn_predict_folder.setIcon(QIcon("assets/icon/folder.png"))
        self.btn_predict_folder.setIconSize(QSize(24, 24)) 
        self.btn_predict_folder.setStyleSheet("padding-left: 10px; text-align: left;")

        self.btn_logout.setIcon(QIcon("assets/icon/logout.png"))
        self.btn_logout.setIconSize(QSize(24, 24)) 
        self.btn_logout.setStyleSheet("padding-left: 10px; text-align: left;")

        self.btn_predict_file.clicked.connect(lambda: self.switchPage(0))
        self.btn_predict_folder.clicked.connect(lambda: self.switchPage(1))
        self.btn_logout.clicked.connect(lambda: self.switchPage(2))
            
        self.setupUI()
        self.switchPage(0)

    def setupUI(self):
        while self.stackedWidget.count() > 0:
            self.stackedWidget.removeWidget(self.stackedWidget.widget(0))
            
        self.classify_page = Classify(self)
        self.stackedWidget.addWidget(self.classify_page)
        
        self.classify_folder_page = ClassifyFolder(self)
        self.stackedWidget.addWidget(self.classify_folder_page)
        
        print(f"Số widget trong stackedWidget: {self.stackedWidget.count()}")

    def switchPage(self, index):
        if index == 2:  # Nếu bấm vào Logout
            self.logout()
            return  
        if index < self.stackedWidget.count():
            self.stackedWidget.setCurrentIndex(index)
            self.updateButtonStyle(index)  # Cập nhật màu nút
        else:
            print(f"Lỗi: Không có trang với index {index}")

    def updateButtonStyle(self, index):
        """ Cập nhật màu nền của button tương ứng """
        default_style = """
            QPushButton {
                background-color: none;
                color: black;
                border: none;
                text-align: left;
                padding-left: 10px;
            }
        """
        active_style = """
            QPushButton {
                background-color: #007BFF; 
                color: white;
                border-radius: 5px;
                padding-left: 10px;
            }
        """

        # Reset tất cả button về default
        self.btn_predict_file.setStyleSheet(default_style)
        self.btn_predict_folder.setStyleSheet(default_style)
        self.btn_logout.setStyleSheet(default_style)

        # Đổi màu nút tương ứng với trang đang mở
        if index == 0:
            self.btn_predict_file.setStyleSheet(active_style)
        elif index == 1:
            self.btn_predict_folder.setStyleSheet(active_style)
        elif index == 2:
            self.btn_logout.setStyleSheet(active_style)

    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Bạn có chắc chắn muốn thoát?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit() 

    
   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())