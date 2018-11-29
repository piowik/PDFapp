# PDFapp

Simple python 3 program to process multiple PDFs (merge, encrypt, decrypt, rotate, watermark, add bookmarks, include javascript)

Includes simple GUI

# Requirements
Python 3

PyPDF2
```bash
pip install PyPDF2
```

# Usage:
Command line
```bash
python pdfapp.py -h
usage: pdfapp [-h] [-o OUTPUT] [-e ENCRYPT] [--use_40bit] [--add_bookmarks]
              [-d DECRYPT] [--rotate {90,180,270}] [--watermark WATERMARK]
              [-j JAVASCRIPT] [-jf JAVASCRIPTFILE]
              PATH [PATH ...]

positional arguments:
  PATH                  input path(s), multiple files will be merged

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output path (default out.pdf)
  -e ENCRYPT, --encrypt ENCRYPT
                        encrypt output file with password
  --use_40bit           use 40 bit encryption instead of 128bit
  --add_bookmarks       add bookmarks pointing beginnings of merged PDFs
  -d DECRYPT, --decrypt DECRYPT
                        decrypt pdf file
  --rotate {90,180,270}
                        clockwise rotation in degrees
  --watermark WATERMARK
                        watermark .pdf path
  -j JAVASCRIPT, --javascript JAVASCRIPT
                        add javascript to pdf
  -jf JAVASCRIPTFILE, --javascriptfile JAVASCRIPTFILE
                        add javascript from file to pdf
```

GUI
```bash
python pdfapp-gui.py
```
