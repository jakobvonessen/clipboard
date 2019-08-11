import requests, pyperclip
from bs4 import BeautifulSoup

def getThing(type,searchIn):
    startIndx = 0
    endIndx = 0
    try:
        startIndx = searchIn.index(type)+len(type)+2
        endIndx = startIndx + searchIn[startIndx:].index(",")
    except ValueError:
        print("Didn't find anything")
        exit()
    return searchIn[startIndx:endIndx].strip('"')

def getAddress(searchPhrase):
    url = "https://www.hitta.se/sök?vad="
    (true, false, null) = True, False, None
    res = requests.get(url+searchPhrase)
    res.raise_for_status()
    html = res.text
    soup = BeautifulSoup(html,features="html.parser")
    soupRes = soup.select(".result-row__text-container")
    results = []
    if len(soupRes) > 0:
        for result in soupRes:
            rows = [x for x in result.getText().strip().split('\n') if len(x) > 0 and x[0].lower() in "abcdefghijklmnopqrstuvwxyzåäö1234567890" and "-" not in x]
            rowsRes = ""
            for row in rows:
                rowsRes += row + "\n"
            results.append(rowsRes)
    else:
        scripts = soup.select("script")
        fakeJson = scripts[7].getText()
        namn = getThing("name",fakeJson)
        adress = getThing("streetAddress",fakeJson)
        postkod = getThing("postalCode",fakeJson)
        stad = getThing("addressLocality",fakeJson)
        results.append("%s\n%s\n%s %s" % (namn,adress,postkod, stad))
    return results

import sys, webbrowser
from PySide2 import QtCore
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Hejsan123")
        self.edit = QLineEdit("")
        bigFont = QFont("Times",20)
        self.edit.setFont(bigFont)
        self.button = QPushButton("Hitta")
        self.button.setFont(bigFont)
        self.layout = QGridLayout()
        self.layout.addWidget(self.edit,1,1)
        self.layout.addWidget(self.button,2,1)
        self.layout.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.resultsLayout = QGridLayout()
        #self.layout.addLayout(self.resultsLayout)
        self.resultsLayout.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.search)
        self.setWindowOpacity(0.8)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.resultButtons = []
        self.spacing = []
        self.connect(QShortcut(QKeySequence(QtCore.Qt.Key_A), self), QtCore.SIGNAL('activated()'), self.copyAddress)
        self.connect(QShortcut(QKeySequence(QtCore.Qt.Key_N), self), QtCore.SIGNAL('activated()'), self.copyName)
        self.connect(QShortcut(QKeySequence(QtCore.Qt.Key_P), self), QtCore.SIGNAL('activated()'), self.copyPostCode)
        self.connect(QShortcut(QKeySequence(QtCore.Qt.Key_M), self), QtCore.SIGNAL('activated()'), self.openMaps)

    def getProps(self, char):
        return resultsProps[self.propText+char]

    def openMaps(self):
        address = self.getProps("a")
        postCode = self.getProps("p")
        url = r"https://www.google.com/maps/search/"
        webbrowser.open("%s%s, %s" % (url,address,postCode))

    def copyPostCode(self):
        postCode = self.getProps("p")
        pyperclip.copy(postCode)

    def copyAddress(self):
        address = getProps("a")
        pyperclip.copy(address)

    def copyName(self):
        name = getProps("n")
        pyperclip.copy(name)

    def getProp(self, char):
        for key in resultsProps.keys():
            if key.endswith(char):
                return resultsProps[key]

    def resetResults(self):
        for resultButton in self.resultButtons:
            resultButton.deleteLater()
        self.resultButtons = []

    def search(self):
        self.results = getAddress(self.edit.text())
        self.resetResults()
        self.showResults()
        #for i in reversed(range(self.resultsLayout.count())):
        #    self.resultsLayout.itemAt(i).widget().setParent(None)

    def showResult(self):
        self.propText = self.sender().text()
        self.resetResults()
        props = ["n","a","p"]
        fullProps = "%s\n%s\n%s" % (resultsProps[self.propText+"n"], resultsProps[self.propText+"a"], resultsProps[self.propText+"p"])
        button = self.makeButton("Go back",0)
        button.clicked.connect(self.showResults)
        button = self.makeButton(fullProps,1)
        button.clicked.connect(self.copyText)
        for indx,prop in enumerate(props):
            button = self.makeButton(resultsProps[self.propText+prop],indx+2)
            button.clicked.connect(self.copyText)
    def makeButton(self, text, indx):
        startIndx = 3
        buttonButton = QPushButton(text)
        self.resultButtons.append(buttonButton)
        self.layout.addWidget(buttonButton,startIndx+indx,1)
        return buttonButton

    def copyText(self):
        pyperclip.copy(self.sender().text())

    def showResults(self):
        self.resetResults()
        for index,result in enumerate(self.results):
            resultRows = result.split('\n')
            name = resultRows[0]
            indx = 1 if len(resultRows) == 3 else 2
            address = resultRows[indx]
            postCity = resultRows[indx+1]
            resultButton = QPushButton()
            buttonText = "%s %s %s" % (name, address, postCity)
            resultButton.setText(buttonText)
            resultsProps[buttonText+"n"] = name
            resultsProps[buttonText+"a"] = address
            resultsProps[buttonText+"p"] = postCity
            resultButton.clicked.connect(self.showResult)
            self.resultButtons.append(resultButton)
            self.layout.addWidget(resultButton,3+index,1)
        self.layout.layout().update()

    def mousePressEvent(self, e):
        self.offset = e.pos()

    def mouseMoveEvent(self, e):
        x = e.globalX()
        y = e.globalY()
        xW = self.offset.x()
        yW = self.offset.y()
        self.move(x-xW,y-yW)
resultsProps = {}
app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())

#results =  getAddress("Jonas von Essen"):
