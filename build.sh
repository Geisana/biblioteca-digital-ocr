#!/usr/bin/env bash

apt-get update

apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils

pip install -r requirements.txt