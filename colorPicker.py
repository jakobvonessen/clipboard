# Shows image currently in clipboard, lets user choose pixel color and copies rgb values from that pixel to clipboard.
import pyperclip, PySide2, sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PIL import ImageGrab
from notify import notify
class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Text without borders")
        self.setFocusPolicy(Qt.StrongFocus)
        bigFont = QFont("Inconsolata",30,QFont.DemiBold)
        self.container = QWidget(self)
        self.layout = QGridLayout(self.container)
        self.imageLayout = QVBoxLayout()
        self.label = QLabel(self)
        self.image = QPixmap(tempImgPath)
        self.label.setPixmap(self.image)
        self.imageLayout.addWidget(self.label)
        self.layout.addLayout(self.imageLayout,0,1)
        self.setLayout(self.layout)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.8)
        self.setAcceptDrops(True)
        self.filePath = ""
        self.label.mousePressEvent = self.onClick
        self.label.mouseMoveEvent = self.onClick
        self.connect(QShortcut(QKeySequence(Qt.Key_Escape), self), SIGNAL('activated()'), self.onExit)
        self.connect(QShortcut(QKeySequence(Qt.Key_Return), self), SIGNAL('activated()'), self.onExit)
    def onClick(self, e):
        global x,y,r,g,b
        x,y = e.x(), e.y()
        r,g,b = img.getpixel((x,y))
        self.setStyleSheet("background-color: rgb(%i,%i,%i);" % (r,g,b))
        print(r,g,b)

    def onExit(self):
        fullCopy = "rgb(%s,%s,%s)" % (r,g,b)
        pyperclip.copy(fullCopy)
        exit()

def changedFocusSlot(old, now):
    print("hej")

tempImgPath = "hej123.png"
img = ImageGrab.grabclipboard()
try:
    img.save(tempImgPath)
except AttributeError:
    notify("ERROR: No image in clipboard.")
    exit()
r,g,b,x,y = 0,0,0,0,0
app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())
