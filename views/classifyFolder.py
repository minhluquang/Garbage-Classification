from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
import os
import tensorflow as tf
import cv2
import numpy as np
from pathlib import Path
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication 
import shutil  # For moving files
import matplotlib.pyplot as plt
from PyQt6.QtGui import QImage, QPixmap
import io

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class ClassifyFolder(QMainWindow):  
    def __init__(self, widget):
        super(ClassifyFolder, self).__init__()
        loadUi("ui/classifyFolder.ui", self)  
        self.widget = widget
        self.lbl_predicting.hide()
        self.lbl_result.hide()

        self.btn_predict.clicked.connect(self.handle_predict)
        self.btn_input_folder.clicked.connect(self.openFolderDialog)
        self.btn_output_folder.clicked.connect(self.handle_outputFolder)

        model_path = Path(__file__).resolve().parent.parent / "models/densenet201.h5"
        self.model = tf.keras.models.load_model(model_path)

        self.input_folder = None  # Store selected input folder
        self.output_folder = None  # Store selected output folder
        self.prediction_done = False  # Track whether prediction is completed

        self.btn_output_folder.setEnabled(False)  # Disable output folder button initially
        self.btn_output_folder.setStyleSheet("""
            QPushButton:disabled {
                background-color: #A0A0A0; 
                color: #ffffff; 
                border: 1px solid #808080; 
            }""")

        self.btn_predict.setEnabled(False)
        self.btn_predict.setStyleSheet("""
            QPushButton:disabled {
                background-color: #A0A0A0; 
                color: #ffffff; 
                border: 1px solid #808080; 
            }""")

    def openFolderDialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if not folder_path:  
            return

        self.input_folder = folder_path  # Store the input folder path
        print(f"Selected input folder: {self.input_folder}")
        self.lbl_input_path.setText(f"Input Folder: {self.input_folder}")

        image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")

        # Recursively find all image files in the folder and subfolders
        image_files = [str(file.resolve()) for file in Path(folder_path).rglob("*") if file.suffix.lower() in image_extensions]
        self.lbl_output_path.setText("Output folder:")
        self.lbl_predicting.hide()
        self.lbl_result.hide()

        if not image_files:
            self.btn_predict.setEnabled(False)
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText(f"Thư mục bạn chọn không chứa hình ảnh nào cả!")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.exec()
            # QMessageBox.warning(self, "No Images Found", "The selected folder does not contain any images.")
            return
        self.btn_predict.setEnabled(True)
        self.current_image_path = image_files  # Store selected images

        # Reset prediction status
        self.prediction_done = False
        self.btn_output_folder.setEnabled(False)  # Ensure output folder button is disabled

    def handle_outputFolder(self):
        if not self.prediction_done:
            # QMessageBox.warning(self, "Prediction Required", "You must complete the prediction before selecting the output folder.")
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText(f"Bạn phải hoàn thành việc dự đoán trước khi chọn thư mục đầu ra.")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.exec()
            return

        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not folder_path:  
            return

        self.output_folder = folder_path  # Store chosen output folder
        print(f"Selected output folder: {self.output_folder}")

        # Move images into corresponding folders
        self.move_images_to_folders()
        # Lưu biểu đồ vào thư mục output
        self.save_statistics_chart()

    def handle_predict(self):
        if not self.input_folder:
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText(f"Bạn phải chọn folder cần phân loại trước khi bấm vào nút này!")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.exec()

            # QMessageBox.warning(self, "Input Folder Required", "You must select an input folder before predicting.")
            return

        if self.current_image_path:  # Ensure list is not empty
            print(f"Predicting for: {self.current_image_path}")
            self.lbl_result.setText('')
            self.btn_output_folder.setEnabled(False)
            className = [
                'battery', 'biological', 'brown-glass', 'cardboard', 'clothes',
                'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass'
            ]
            
            # Dictionary to store counts of predicted classes
            self.class_counts = {name: 0 for name in className}  # Store in self for use in move_images_to_folders
            self.image_class_map = {}  # Store image paths mapped to predicted class

            countPredict = 0

            for image_path in self.current_image_path:
                countPredict += 1
                self.lbl_predicting.show()
                self.lbl_predicting.setText(f'Predicting... ({countPredict}/{len(self.current_image_path)})')
                QApplication.processEvents()

                # Read image and convert to RGB
                img = cv2.imread(image_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Resize to model input size
                img = cv2.resize(img, (224, 224))

                # Normalize image
                img_array = img.astype(np.float32) / 255.0

                # Expand dimensions to match model input
                img_array = np.expand_dims(img_array, axis=0)

                # Predict
                predictions = self.model.predict(img_array)
                predicted_class = np.argmax(predictions, axis=1)[0]  # Get the predicted index

                # Update class count
                predicted_label = className[predicted_class]
                self.class_counts[predicted_label] += 1

                # Store mapping of image to predicted class
                self.image_class_map[image_path] = predicted_label

            # Format results for display
            result_text = "\n".join([f"{name}: {count}" for name, count in self.class_counts.items() if count > 0])

            # Display results
            self.lbl_result.setText(result_text)
            self.lbl_result.show()

            # Enable output folder button after successful prediction
            self.prediction_done = True
            self.btn_output_folder.setEnabled(True)
            self.show_statistics()
        else:
            print("No images selected")

    def move_images_to_folders(self):
        """Moves the images into corresponding class folders inside the output directory."""
        if not self.output_folder:
            # QMessageBox.warning(self, "Output Folder Required", "You must select an output folder first.")
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText(f"Bạn phải chọn folder cần lưu trước khi bấm vào nút này!")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.exec()

            return

        for image_path, class_name in self.image_class_map.items():
            class_folder = os.path.join(self.output_folder, class_name)

            # Create class folder if it doesn't exist
            if not os.path.exists(class_folder):
                os.makedirs(class_folder)

            # Move image to class folder
            dest_path = os.path.join(class_folder, os.path.basename(image_path))
            shutil.move(image_path, dest_path)

        # QMessageBox.information(self, "Success", "Images have been moved to their respective folders.")
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Thông báo")
        msg.setText(f"Hình ảnh đã được di chuyển vào các thư mục tương ứng.")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.exec()
        print(f"Images successfully moved to: {self.output_folder}")
        self.lbl_output_path.setText(f'Output Folder: {self.output_folder}')

    def show_statistics(self):
        if not self.class_counts:
            # QMessageBox.warning(self, "No Data", "No classification data available.")
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText(f"Không có dữ liệu phân loại nào.")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.exec()
            return

        labels = list(self.class_counts.keys())
        values = list(self.class_counts.values())

        plt.figure(figsize=(8, 5))
        plt.bar(labels, values, color=['blue', 'green', 'red', 'orange', 'purple'])
        plt.xlabel("Loại rác thải")
        plt.ylabel("Số lượng ảnh")
        plt.title("Thống kê phân loại rác thải")
        plt.xticks(rotation=45)
        plt.savefig("temp/statistics.png", bbox_inches="tight") 
        plt.close()
        self.show_chart_window("temp/statistics.png")

    def show_chart_window(self, image_path):
        dialog = QDialog(self)
        dialog.setWindowTitle("Thống kê phân loại")
        layout = QVBoxLayout()

        label = QLabel(dialog)
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        dialog.setLayout(layout)
        dialog.exec()

    def save_statistics_chart(self):
        if not self.class_counts or not self.output_folder:
            return

        labels = list(self.class_counts.keys())
        values = list(self.class_counts.values())

        plt.figure(figsize=(8, 5))
        plt.bar(labels, values, color=['blue', 'green', 'red', 'orange', 'purple'])
        plt.xlabel("Loại rác thải")
        plt.ylabel("Số lượng ảnh")
        plt.title("Thống kê phân loại rác thải")
        plt.xticks(rotation=45)

        # Lưu vào thư mục output
        output_image_path = os.path.join(self.output_folder, "statistics.png")
        plt.savefig(output_image_path, bbox_inches="tight")
        plt.close()

        print(f"Saved statistics chart to: {output_image_path}")
        # self.show_chart_window(output_image_path)
