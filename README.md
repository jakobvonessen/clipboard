# Clipboard
*Python 3 scripts for working with clipboard contents, whose outputs go right back into the clipboard.*

### imageToPasteOCR.py
Primarily performs OCR on image copied to clipboard, using [pytesseract](https://pypi.org/project/pytesseract/). If run more than once, it does the following (in order):
* Saves clipboard text to file (with random filename) in the `C:\temp` folder, and copies full file search path (e.g., `C:\temp\asb2fh2.txt`) to clipboard.
* Opens `Save As` dialog, to rename the file previously saved to something else, then copies new path to clipboard.
### clipboardSearchReplace.py
GUI app to quickly perform search and replace functions on text in the clipboard. Features:
* 
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjIzMzAxMzI3LDE1MjQ3NjM1NDgsLTk4ND
M4ODI3LDUwNDQxNDIxNCwtMzMyNDU1MzYzXX0=
-->