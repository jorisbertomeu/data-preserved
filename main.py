#!/usr/bin/python3
# encoding: utf-8

from os.path import basename, join, exists, dirname
from pytesseract import image_to_data, pytesseract
from cv2 import imread, imwrite, GaussianBlur
from argparse import ArgumentParser
from PIL import Image
from re import match
from sys import argv

TESSERACT_WIN_64 = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSERACT_WIN_86 = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

LEFT, TOP, WIDTH, HEIGHT = 6, 7, 8, 9
PATTERN_MAIL = """(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))"""
PATTERN_PHONE = """(?:\+33|0)\d(?:\.|\s)?\d{2}(?:\.|\s)?\d{2}(?:\.|\s)?\d{2}(?:\.|\s)?\d{2}"""
PATTERN_IP_V4 = """((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])(?::(?:[0-9]|[1-9][0-9]{1,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?"""
PATTERN_IP_V6 = """(?:(?:(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){6}:[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){5}:([0-9A-Fa-f]{1,4}:)?[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){4}:([0-9A-Fa-f]{1,4}:){0,2}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){3}:([0-9A-Fa-f]{1,4}:){0,3}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){2}:([0-9A-Fa-f]{1,4}:){0,4}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){6}((\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b)\.){3}(\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b))|(([0-9A-Fa-f]{1,4}:){0,5}:((\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b)\.){3}(\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b))|(::([0-9A-Fa-f]{1,4}:){0,5}((\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b)\.){3}(\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b))|([0-9A-Fa-f]{1,4}::([0-9A-Fa-f]{1,4}:){0,5}[0-9A-Fa-f]{1,4})|(::([0-9A-Fa-f]{1,4}:){0,6}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){1,7}:))|\[(?:(?:(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){6}:[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){5}:([0-9A-Fa-f]{1,4}:)?[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){4}:([0-9A-Fa-f]{1,4}:){0,2}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){3}:([0-9A-Fa-f]{1,4}:){0,3}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){2}:([0-9A-Fa-f]{1,4}:){0,4}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){6}((\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b)\.){3}(\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b))|(([0-9A-Fa-f]{1,4}:){0,5}:((\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b)\.){3}(\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b))|(::([0-9A-Fa-f]{1,4}:){0,5}((\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b)\.){3}(\b((25[0-5])|(1\d{2})|(2[0-4]\d)|(\d{1,2}))\b))|([0-9A-Fa-f]{1,4}::([0-9A-Fa-f]{1,4}:){0,5}[0-9A-Fa-f]{1,4})|(::([0-9A-Fa-f]{1,4}:){0,6}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){1,7}:))\](?::(?:[0-9]|[1-9][0-9]{1,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?"""

# Traitement des arguments

parser = ArgumentParser(description="Hide sensitive information in images")
parser.add_argument("path", metavar="FILE", type=str, help="Image path to anonymize")
parser.add_argument("-b", "--bin", metavar="", type=str, default=None, help="Tesseract binary path")
parser.add_argument("-p", "--phone", action="store_true", default=False, help="Anonymize phone numbers")
parser.add_argument("-m", "--mail", action="store_true", default=False, help="Anonymize email addresses")
parser.add_argument("-4", "--ipv4", action="store_true", default=False, help="Anonymize IPv4")
parser.add_argument("-6", "--ipv6", action="store_true", default=False, help="Anonymize IPv6")
parser.add_argument("-a", "--all", action="store_true", default=False, help="Anonymize all information")
parser.add_argument("-o", "--output", metavar="DIR", type=str, default=None, help="Output directory")
args = parser.parse_args()

# Initialisation de Tesseract

if args.bin and exists(args.bin):
    pytesseract.tesseract_cmd = args.bin
elif exists(TESSERACT_WIN_64):
    pytesseract.tesseract_cmd = TESSERACT_WIN_64
elif exists(TESSERACT_WIN_86):
    pytesseract.tesseract_cmd = TESSERACT_WIN_86
else:
    print("Please install Tesseract or indicate the path")

 # Extraction du texte

positions = []
data = image_to_data(Image.open(args.path))
for l in data.splitlines():
    e = l.split("\t")
    if match(PATTERN_MAIL, e[-1]) and (args.mail or args.all):
        p = (int(e[LEFT]), int(e[TOP]), int(e[WIDTH]), int(e[HEIGHT]))
        positions.append(p)
    if match(PATTERN_IP_V6, e[-1]) and (args.ipv6 or args.all):
        p = (int(e[LEFT]), int(e[TOP]), int(e[WIDTH]), int(e[HEIGHT]))
        positions.append(p)
    if match(PATTERN_IP_V4, e[-1]) and (args.ipv4 or args.all):
        p = (int(e[LEFT]), int(e[TOP]), int(e[WIDTH]), int(e[HEIGHT]))
        positions.append(p)
    if match(PATTERN_PHONE, e[-1]) and (args.phone or args.all):
        p = (int(e[LEFT]), int(e[TOP]), int(e[WIDTH]), int(e[HEIGHT]))
        positions.append(p)

# Modification de l'image

img = imread(args.path)

for x, y, w, h in positions:
    roi = img[y:y+h, x:x+w]
    blur = GaussianBlur(roi, (51, 51), 0)
    img[y:y+h, x:x+w] = blur

# Enregistrement de l'image

name = basename(args.path).split(".")[0]
ext = basename(args.path).split(".")[-1]

if not args.output:
    path = join(dirname(args.path), f"{name}.edited.{ext}")
else:
    path = join(args.output, f"{name}.{ext}")

imwrite(path, img)
print(f"Saved in {path}")
