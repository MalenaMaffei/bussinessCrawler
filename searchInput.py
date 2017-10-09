import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
import io
import sitesScraper

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 input dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        search = self.getText()
        self.show()

        stdout = sys.stdout
        sys.stdout = io.StringIO()

        sitesScraper.main(search)

        output = sys.stdout.getvalue()
        sys.stdout = stdout
        print("stdout desde gui: " + output)



    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Start Search","Search Terms:", QLineEdit.Normal, "for ex: Restaurants")
        if okPressed and text != '':
            return(text + " in Miami")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    # app.exec_()
