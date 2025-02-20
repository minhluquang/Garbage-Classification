import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from views.login import Login 

app = QApplication(sys.argv)
widget = QStackedWidget()

login_screen = Login(widget)
widget.addWidget(login_screen)  
widget.setFixedSize(1200, 700)  
widget.show() 

sys.exit(app.exec())
