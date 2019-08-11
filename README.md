# Clipboard
*Python 3 scripts for working with clipboard contents, whose outputs go right back into the clipboard.*

### imageToPasteOCR.py
Primarily performs OCR on image copied to clipboard, using [pytesseract](https://pypi.org/project/pytesseract/). If run more than once, it does the following (in order):
* Saves clipboard text to file (with random filename) in the `C:\temp` folder, and copies full file search path (e.g., `C:\temp\asb2fh2.txt`) to clipboard.
* Opens `Save As` dialog, to rename the file previously saved to something else, then copies new path to clipboard.
### clipboardSearchReplace.py
GUI app to quickly perform search and replace functions on text in the clipboard. Features:
* Include a comma (**,**) to get several similar phrases at the same time, by specifying only the differences.
    * **Example**: Replace `a green boat` with `a yellow boat, a blue boat, a red boat, a black boat` by entering `green` in the *search* field, and `yellow,blue,red,black` in the *replace* field, and `,` instead of `\n` (default) in the *delimiter* field.
### colorPicker.py
Allows easy access to RGB color values of images in clipboard by showing the image, with a border showing the currently selected color, copying the `rgb(x,y,z)` values of the selected color when exiting.
### hitta.py
### notify.py
Uses the AutoHotkey
### saveClipboardImage.py
Saves current clipboard image data as an image in `C:\temp`, then copies the full search path (e.g., `C:\temp\24.png`) to clipboard.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTI3ODk4ODQwMCwxNTQ1MTE4ODExLDIxMz
Q4MDg0MjcsLTIwMzMxMjE2NjYsMTUyNDc2MzU0OCwtOTg0Mzg4
MjcsNTA0NDE0MjE0LC0zMzI0NTUzNjNdfQ==
-->