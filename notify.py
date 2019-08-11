def notify(msg):
    import subprocess
    exePath = r"C:\Program Files\AutoHotkey\AutoHotkey.exe"
    ahkPath = r"C:\Drive\Dropbox (Personal)\apps\ahk\notify.ahk"
    cmd = "\"%s\" \"%s\" \"%s\"" % (exePath, ahkPath, msg)
    subprocess.call(cmd)
