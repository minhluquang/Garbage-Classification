import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from views.login import Login 
from views.classify import Classify
from views.classifyFolder import ClassifyFolder
from views.main import Main

app = QApplication(sys.argv)
widget = QStackedWidget()

login_screen = Login(widget)
widget.addWidget(login_screen)  

# main = Main(widget)
# widget.addWidget(main)


widget.setFixedSize(1200, 700)  
widget.show() 

sys.exit(app.exec())
