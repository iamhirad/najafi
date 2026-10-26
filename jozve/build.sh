#!/bin/sh
# Build the Persian lecture notes (needs XeLaTeX, xepersian, Vazirmatn font, gnuplot)
cd "$(dirname "$0")"
xelatex -shell-escape -interaction=nonstopmode main.tex > build.log 2>&1
xelatex -shell-escape -interaction=nonstopmode main.tex > build.log 2>&1
grep -E "^!" build.log || echo "OK: main.pdf"
