import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
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

        # stdout = sys.stdout
        # sys.stdout = io.StringIO()
        #
        # sitesScraper.main(search)
        #
        # output = sys.stdout.getvalue()
        # sys.stdout = stdout
        # print("stdout desde gui: " + output)



    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Start Search","Search Terms:", QLineEdit.Normal, "for ex: Restaurants")
        if okPressed and text != '':
            return(text + " in Miami")

class OutLog:
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.moveCursor(QtGui.QTextCursor.End)
        self.edit.insertPlainText( m )

        if self.color:
            self.edit.setTextColor(tc)

        if self.out:
            self.out.write(m)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    sys.stdout = OutLog( edit, sys.stdout)
    sys.stderr = OutLog( edit, sys.stderr, QtGui.QColor(255,0,0) )


    ex = App()
    sys.exit(app.exec_())
    # app.exec_()
