#!/bin/bash

pandoc --citeproc --pdf-engine=xelatex newpaper.md -o newpaper.pdf
