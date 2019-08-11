import pyperclip, os, sys
from pytesseract import image_to_string as ocr, TesseractError
from random import randint
from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PIL import ImageGrab
from notify import notify

def getRandomFileName(ext):
    randStr = ''.join(str(randint(0,9)) for x in range(10))
    fileName = "file%s" % randStr
    basePath = r"C:\TEMP"
    return os.path.join(basePath,"%s.%s" % (fileName,ext))

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        #saveFile = QtWidgets.QAction("&Save file", self)
        #saveFile.triggered.connect(self.onFileSave)
        self.onFileSave()

    def onFileSave(self):
        #newPath = QtWidgets.QFileDialog.getSaveFileName(self, "Rename file")
        newPath = QtWidgets.QFileDialog.getSaveFileName(None, 'Rename file', imgPath, 'All Files(*.*)')
        newPath = newPath[0]
        if newPath != '':
            if os.path.isfile(newPath):
                os.replace(imgPath, newPath)
            else:
                os.rename(imgPath,newPath)
            newPath = newPath.replace('/','\\')
            pyperclip.copy(newPath)
            notify("Done: %s" % newPath)
        quit()

imgPath = pyperclip.paste()
imgText = ""
if len(imgPath) < 200 and os.path.isfile(imgPath):
    try:
        imgText = ocr(imgPath)
        pyperclip.copy(imgText)
        notify("Done: %s" % imgText)
    except TesseractError:
        app = QApplication()
        window = Window()
        window.show()
        sys.exit(app.exec_())
else:
    img = ImageGrab.grabclipboard()
    print(type(img))
    print(img)
    if img is not None:
        fakePath = getRandomFileName("png")
        img.save(fakePath)
        imgText = ocr(fakePath)
        pyperclip.copy(imgText)
        notify("Done: %s" % imgText)
    else:
        filename = getRandomFileName("txt")
        with open(filename,"w+",newline='') as file:
            file.write(imgPath)
        imgText = filename
        pyperclip.copy(imgText)
        notify("Done: %s" % imgText)
