# Clipboard
*Scripts related to clipboard contents, whose outputs go right back into the clipboard.*

### imageToPasteOCR.py
Primarily performs OCR on image copied to clipboard, using [pytesseract](https://pypi.org/project/pytesseract/). If run more than once, it does the following (in order):
1. Saves clipboard text to file (with random filename) in the `C:\temp` folder, and copies full file search path (e.g., `C:\temp\asb2fh2.txt`) to clipboard.
2. Opens `File Save`
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTgwOTA0Mjk2MywxNTI0NzYzNTQ4LC05OD
QzODgyNyw1MDQ0MTQyMTQsLTMzMjQ1NTM2M119
-->