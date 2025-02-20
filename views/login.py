from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi
import MySQLdb as mdb
import MySQLdb.cursors
import bcrypt
from config.db_config import connect_db

class Login(QMainWindow):  
    def __init__(self, widget):
        super(Login, self).__init__()
        loadUi("ui/login.ui", self)  
        self.widget = widget
        self.btn_login.clicked.connect(self.loginAccount)
        self.btn_signup.clicked.connect(self.gotoSignup)

    def gotoSignup(self):
        from views.signup import Signup  
        signup = Signup(self.widget)
        self.widget.addWidget(signup)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    # Login
    def loginAccount(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if self.queryLoginAccount(username, password):
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText("Đăng nhập thành công!")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            # Code navigate to the main here
            # ...
            msg.exec()
        else: 
            QtWidgets.QMessageBox.warning(self, "Thông báo", "Đăng nhập thất bại")

    # Query to login
    def queryLoginAccount(self, username, password):
        try:
            conn = connect_db()
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)

            query = "SELECT * FROM accounts WHERE username = %s"
            cursor.execute(query, (username,))

            result = cursor.fetchone()
            conn.close()

            if result:
                print(f"Input password: {password}, database password: {result['password']} ")
                hashed_password = result['password'].encode('utf-8')
                return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

            return False
        except mdb.Error as e:
            print(f"Database error: {e}")
            return False