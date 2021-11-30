# Data-Preserved

Script allowing to blur the most sensitive information on images.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed the latest version of Tesseract :
  * https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.0.0-rc1.20211030.exe (Windows 32 bits)
  * https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-rc1.20211030.exe (Windows 64 bits)
  * sudo apt install tesseract-ocr (Debian)
  * brew install tesseract (MacOS)
* Python >= 3.6

## Installing Data-Preserved

To install data-preserved, follow these steps:

```
pip install -r requirements.txt
```

## Using Data-Preserved

To use data-preserved, follow these steps:

```
usage: main.py [-h] [-b] [-p] [-m] [-4] [-6] [-a] [-o DIR] FILE

Hide sensitive information in images

positional arguments:
  FILE                  Image path to anonymize

optional arguments:
  -h, --help            show this help message and exit
  -b , --bin            Tesseract binary path
  -p, --phone           Anonymize phone numbers
  -m, --mail            Anonymize email addresses
  -4, --ipv4            Anonymize IPv4
  -6, --ipv6            Anonymize IPv6
  -a, --all             Anonymize all information
  -o DIR, --output DIR  Output directory
```
