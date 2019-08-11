# Clipboard
*Python 3 scripts for working with clipboard contents, whose outputs go right back into the clipboard.*

### imageToPasteOCR.py
Primarily performs OCR on image copied to clipboard, using [pytesseract](https://pypi.org/project/pytesseract/). If run more than once, it does the following (in order):
* Saves clipboard text to file (with random filename) in the `C:\temp` folder, and copies full file search path (e.g., `C:\temp\asb2fh2.txt`) to clipboard.
* Opens `Save As` dialog, to rename the file previously saved to something else, then copies new path to clipboard.
### clipboardSearchReplace.py
GUI app to quickly perform search and replace functions on text in the clipboard. Features:
* Include a comma (**,**) to get several similar phrases at the same time, by specifying only the differences. 

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIwNTM3NTUwOTYsMTUyNDc2MzU0OCwtOT
g0Mzg4MjcsNTA0NDE0MjE0LC0zMzI0NTUzNjNdfQ==
-->