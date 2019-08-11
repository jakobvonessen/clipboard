from PIL import ImageGrab

def notify(msg):
    import subprocess
    exePath = r"C:\Program Files\AutoHotkey\AutoHotkey.exe"
    ahkPath = r"C:\Drive\Dropbox (Personal)\apps\ahk\notify.ahk"
    cmd = "\"%s\" \"%s\" \"%s\"" % (exePath, ahkPath, msg)
    print(cmd)
    subprocess.call(cmd)

import os, pyperclip
img = ImageGrab.grabclipboard()
basePath = r"C:\TEMP"
indx = 0
suffix = ".png"
while indx < 10000:
    fullPath = os.path.join(basePath,str(indx) + suffix)
    if not os.path.isfile(fullPath):
        break
    indx+=1
print(fullPath)
if img is not None:
    img.save(fullPath)
    pyperclip.copy(fullPath)
    notify("Done: %s" % fullPath)
else:
    notify("ERROR: No image in clipboard.")
    pyperclip.copy("ERROR: No image in clipboard.")
