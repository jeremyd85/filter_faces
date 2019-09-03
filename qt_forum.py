from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
import sys


class App():
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.widgets = []
        self.widget_count = 0
        self.layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        for w in self.widgets:
            for k, v in w:
                self.layout.addWidget(v)
        self.layout.addWidget(QPushButton(""))
        self.setLayout(self.layout)
        self.show()

    def add_text_field(self, name):
        self.widgets.append({name, QLineEdit(name)})

    def add_label(self, name):
        self.widgets.append({name, QLabel})

    def exit(self):


class StartApp():

    def __init__(self, widget):
        self.widget = widget
        sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication([])
    ex = App("Add User")
    sys.exit(app.exec_())


