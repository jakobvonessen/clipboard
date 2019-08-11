import wx, wx.adv
from wx.lib import sized_controls as sizedControls
from ObjectListView import ObjectListView, ColumnDefn
import os
import pyperclip

# SETTINGS
headerPath = "headers.csv"
headers = {}
exportPath = "export"
smallFont = 5
largeFont = 9
lineWidth = 1.0
clipboard = pyperclip.paste()
tempClipboard = ""
for piece in clipboard.split('\n'):
    tempClipboard += piece + '\n' #.strip()+'\n'
tempClipboard = tempClipboard[:-len('\n')]
nCount = len(clipboard.split('\n'))
fontSize = 30
smallFontSize = 20


########################################################################
class item(object):
    """
    Model of the item object

    Contains the following attributes:
    'ISBN', 'Author', 'Manufacturer', 'easyDesc'
    """
    #----------------------------------------------------------------------
    def __init__(self, easyDesc, PLCDesc):
        self.easyDesc = easyDesc
        self.PLCDesc = PLCDesc

########################################################################

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.parent = parent
        self.createLayout()
        self.Bind(wx.EVT_MENU,self.onQuit,id=123)
        self.Bind(wx.EVT_MENU,self.toggleCheckbox,id=456)
        entries = [wx.AcceleratorEntry() for i in range(3)]
        entries[0].Set(wx.ACCEL_CTRL, ord('N'), 1)
        entries[1].Set(wx.ACCEL_CTRL, ord('A'), 456)
        entries[2].Set(wx.ACCEL_CTRL, ord('W'), 123)
        accel = wx.AcceleratorTable(entries)

    def onQuit(self,e):
        self.parent.Close(True)

    def onCopy(self, e):
        print(self.splitVisibleClipboard)
        pyperclip.copy(self.splitVisibleClipboard)
        self.onQuit(e)

    def oj(self, e):
        print("oj")

    def createLayout(self):
        self.clipboardField = wx.TextCtrl(self, wx.ID_ANY, style=wx.SUNKEN_BORDER|wx.TE_MULTILINE, size=(-1,fontSize*6))
        global clipboardField
        clipboardField = self.clipboardField
        self.clipboardField.Enable(False)
        self.clipboardField.SetValue(tempClipboard)
        self.clipboardFont = wx.Font(fontSize, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Arial')
        clipboardField.SetFont(self.clipboardFont)
        self.findField = wx.TextCtrl(self, wx.ID_ANY, style=wx.SUNKEN_BORDER, size=(1500, fontSize))
        self.findField.Bind(wx.EVT_KEY_UP, self.onFind)
        self.findField.SetFont(self.clipboardFont)
        self.replaceField = wx.TextCtrl(self, wx.ID_ANY, style=wx.SUNKEN_BORDER, size=(1500, fontSize))
        self.replaceField.Bind(wx.EVT_KEY_UP, self.onReplace)
        self.replaceField.SetFont(self.clipboardFont)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        checkboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.clipboardField, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(self.findField, 2)
        mainSizer.Add(self.replaceField, 3)
        #buttonSizer.Add(self.exportButton, 0, wx.ALL|wx.CENTER, 5)
        self.auxFont = wx.Font(smallFontSize, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Arial')
        self.multiplePastesBox = wx.CheckBox(self, wx.ID_ANY)
        self.multiplePastesBox.SetLabelText("Multiple")
        self.multiplePastesBox.SetFont(self.auxFont)
        self.multiplePastesBox.Bind(wx.EVT_CHECKBOX, self.onCheckbox)
        checkboxSizer.Add(self.multiplePastesBox)
        self.multipleSeparatorField = wx.TextCtrl(self, wx.ID_ANY,style=wx.SUNKEN_BORDER,size=(smallFontSize*2, -1))
        self.multipleSeparatorField.SetValue(",")
        self.multipleSeparatorField.SetFont(self.auxFont)
        self.multipleSeparatorField.Enable(False)
        self.multipleSeparatorField.Bind(wx.EVT_KEY_UP, self.update)
        checkboxSizer.Add(self.multipleSeparatorField)
        self.multipleSeparatorSeparatorField = wx.TextCtrl(self,wx.ID_ANY,style=wx.SUNKEN_BORDER,size=(smallFontSize*2,-1))
        self.multipleSeparatorSeparatorField.SetValue(r"\n")
        self.multipleSeparatorSeparatorField.SetFont(self.auxFont)
        self.multipleSeparatorSeparatorField.Enable(False)
        self.multipleSeparatorSeparatorField.Bind(wx.EVT_KEY_UP, self.update)
        checkboxSizer.Add(self.multipleSeparatorSeparatorField)
        self.prependField = wx.TextCtrl(self, wx.ID_ANY, style=wx.SUNKEN_BORDER, size=(smallFontSize*10, -1))
        self.prependField.SetFont(self.auxFont)
        self.prependField.Bind(wx.EVT_KEY_UP, self.update)
        self.appendField = wx.TextCtrl(self, wx.ID_ANY, style=wx.SUNKEN_BORDER, size=(smallFontSize*10, -1))
        self.appendField.SetFont(self.auxFont)
        self.appendField.Bind(wx.EVT_KEY_UP, self.update)
        checkboxSizer.Add(self.prependField)
        checkboxSizer.Add(self.appendField)
        mainSizer.Add(checkboxSizer, 0, wx.CENTER)
        self.SetSizer(mainSizer)
        self.visibleClipboard = tempClipboard
        self.actualReplaceStr = tempClipboard
        self.splitVisibleClipboard = tempClipboard
        self.replaceStr = ""
        self.findStr = ""
        self.parent.SetStatusText("Ready.")
        self.actuallyFocus = True

    def update(self, e):
        if e.GetEventObject() == self.multipleSeparatorSeparatorField:
            if self.multipleSeparatorSeparatorField.GetValue() == "":
                self.multipleSeparatorSeparatorField.SetValue(r"\n")
                self.multipleSeparatorSeparatorField.SelectAll()
        self.updateClipboard()

    def toggleCheckbox(self,e):
        self.multiplePastesBox.SetValue(not self.multiplePastesBox.GetValue())
        self.updateClipboard()

    def onCheckbox(self, e):
        if self.multiplePastesBox.GetValue():
            self.multipleSeparatorField.Enable()
            self.multipleSeparatorSeparatorField.Enable()
            if self.actuallyFocus:
                self.multipleSeparatorField.SetFocus()
                self.multipleSeparatorField.SelectAll()
            self.actuallyFocus = True
        else:
            self.multipleSeparatorField.Disable()
            self.multipleSeparatorSeparatorField.Disable()
        self.updateClipboard()

    def enableCheckbox(self):
        self.multiplePastesBox.SetValue(True)

    def disableCheckbox(self):
        self.multiplePastesBox.SetValue(False)

    def onFind(self, e):
        self.checkForEnter(e)
        self.findStr = self.findField.GetValue()
        self.updateClipboard()
        e.DoAllowNextEvent()

    def checkForEnter(self,e):
        if e.GetKeyCode() == 13:
            if wx.KeyboardState.ControlDown(e):
                self.onCopy(e)

    def onReplace(self, e):
        self.checkForEnter(e)
        if chr(e.GetKeyCode()) == ",":
            self.actuallyFocus = False
            self.enableCheckbox()
            self.onCheckbox(e)
            self.updateClipboard()
        if not "," in e.GetEventObject().GetValue():
            self.disableCheckbox()
        self.replaceStr = self.replaceField.GetValue()
        self.updateClipboard()
        e.DoAllowNextEvent()
    def updateClipboard(self):
        tempReplaceStr = "{x}"
        separatorSeparator = self.multipleSeparatorSeparatorField.GetValue()
        separatorSeparator = replaceLinebreaksAndTabs(separatorSeparator)
        self.findStr = replaceLinebreaksAndTabs(self.findStr)
        self.replaceStr = replaceLinebreaksAndTabs(self.replaceStr)
        self.visibleClipboard = tempClipboard.replace(self.findStr, self.replaceStr)
        if '\n' in self.findStr:
            rows = self.visibleClipboard.split('\r')
            self.visibleClipboard = ""
            for row in rows:
                self.visibleClipboard+=row.strip("\r")
        if self.visibleClipboard != tempClipboard.upper().replace(self.findStr.upper(),self.replaceStr.upper()):
            if 1: # Replace with checked box (that gets checked automatically)
                self.visibleClipboard = self.visibleClipboard.replace(capitalize(self.findStr),capitalize(self.replaceStr))
        if self.multiplePastesBox.GetValue():
            self.actualReplaceStr = ""
            multipleValues = self.replaceStr.split(self.multipleSeparatorField.GetValue())
            for value in multipleValues:
                self.actualReplaceStr += tempClipboard.replace(self.findStr, value) + separatorSeparator
            self.actualReplaceStr = self.actualReplaceStr[:-len(separatorSeparator)]
            self.parent.SetStatusText(str(len(multipleValues)))
        else:
            self.actualReplaceStr = self.visibleClipboard
            self.parent.SetStatusText("1")
        self.splitVisibleClipboard = ""
        for value in self.actualReplaceStr.split(separatorSeparator):
            self.splitVisibleClipboard+= self.prependField.GetValue() + value + self.appendField.GetValue() + separatorSeparator
        self.splitVisibleClipboard = self.splitVisibleClipboard[:-len(separatorSeparator)]
        self.clipboardField.SetValue(self.visibleClipboard)

def capitalize(string):
    string = string[0].upper() + string[1:] if len(string) > 1 else string
    return string

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="Clipboard Find and Replace",size=(1500,400))
        #self.setIcon()
        self.CreateStatusBar()
        self.Center()
        MainPanel(self)

    def setIcon(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(os.getcwd() + r"\img\graphIcon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
def replaceLinebreaksAndTabs(origStr):
    sepValues = [r'\n',r'\t']
    repValues = ['\n','\t']
    for indx in range(len(sepValues)):
        origStr = origStr.replace(sepValues[indx],repValues[indx])
    return origStr

########################################################################
class GenApp(wx.App):
    #----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    #----------------------------------------------------------------------
    def OnInit(self):
        # create frame here
        frame = MainFrame()
        frame.Show()
        return True

#----------------------------------------------------------------------
def main():
    app = GenApp()
    app.MainLoop()

if __name__ == "__main__":
    main()
