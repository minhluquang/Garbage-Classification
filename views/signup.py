from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi
import re
import MySQLdb as mdb
from config.db_config import connect_db
import bcrypt

class Signup(QMainWindow):  
    def __init__(self, widget):
        super(Signup, self).__init__()
        loadUi("ui/signup.ui", self)  
        self.widget = widget
        self.btn_signup.clicked.connect(self.createAccount)
        self.btn_login.clicked.connect(self.gotoLogin)

    # Goto Login Page
    def gotoLogin(self):
        from views.login import Login 
        login = Login(self.widget)
        self.widget.addWidget(login)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    # Validation create account
    def show_message(self, title, text, msg_type):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning if msg_type == "warning" else QtWidgets.QMessageBox.Icon.Information)
        msg.exec()

    def validation(self, username, password, confirmPassword):
        if not re.fullmatch(r"^[a-zA-Z0-9]{4,20}$", username):
            self.show_message("Thông báo", " - Username phải có 4-20 ký tự.\n - Chỉ chứa chữ, số.", "warning")
            return False

        if not (8 <= len(password) <= 32):
            self.show_message("Thông báo", " - Mật khẩu phải có từ 8 đến 32 ký tự.", "warning")
            return False

        if not re.search(r"[A-Z]", password):
            self.show_message("Thông báo", " - Mật khẩu phải có ít nhất một chữ cái viết hoa.", "warning")
            return False

        if not re.search(r"[a-z]", password):
            self.show_message("Thông báo", " - Mật khẩu phải có ít nhất một chữ cái viết thường.", "warning")
            return False

        if not re.search(r"[0-9]", password):
            self.show_message("Thông báo", " - Mật khẩu phải có ít nhất một chữ số.", "warning")
            return False

        if not re.search(r"[!@#$%^&*()_+]", password):
            self.show_message("Thông báo", " - Mật khẩu phải có ít nhất một ký tự đặc biệt (!@#$%^&*()_+).", "warning")
            return False

        if password != confirmPassword:
            self.show_message("Thông báo", " - Mật khẩu nhập lại không khớp.", "warning")
            return False

        return True
        
    # Hash password
    def hash_password(self, password):
        salt = bcrypt.gensalt()  
        hashed = bcrypt.hashpw(password.encode(), salt)  
        return hashed

    # Query create account
    def queryCreateAccount(self, username, password):
        try:
            hashed_pwd = self.hash_password(password)

            conn = connect_db()
            cursor = conn.cursor()

            query = "INSERT INTO accounts (username, password, status, role_id) VALUES (%s, %s, 1, 2);"
            cursor.execute(query, (username, hashed_pwd))

            conn.commit() 
            conn.close()
            return True
        except mdb.Error as e:
            print(f"Database error: {e}")
            return False
    
    # Query check username is exist
    def queryCheckExistUsername(self, username):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = "SELECT * FROM accounts WHERE username = %s"
            cursor.execute(query, (username,))

            result = cursor.fetchone()
            
            conn.close()
            return result is not None
        except mdb.Error as e:
            print(f"Database error: {e}")
            return False

    # Create account
    def createAccount(self):
        username = self.input_username.text()
        password = self.input_password.text()
        confirmPassword = self.input_confirmPassword.text()

        if self.validation(username, password, confirmPassword):
            if self.queryCheckExistUsername(username):
                QtWidgets.QMessageBox.warning(self, "Thông báo", "Username này đã tồn tại trong hệ thống!")
                return

            if (self.queryCreateAccount(username, password)):
                msg=QtWidgets.QMessageBox()
                msg.setWindowTitle("Thông báo")
                msg.setText("Đăng ký thành công!")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msg.buttonClicked.connect(self.gotoLogin) 
                msg.exec()
            else:
                QtWidgets.QMessageBox.warning(self, "Thông báo", "Đăng ký thất bại")
