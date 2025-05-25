#!/bin/bash

SESSION_NUM=01
LETTER_PATH="vellynne-notes/session01/letter-to-rothbart.md"
OUTPUT_DIR="vellynne-notes/session01/output"

echo "📝 Generating PDF for Letter to Rothbart..."
mkdir -p "$OUTPUT_DIR"

# Convert markdown to PDF using pandoc
pandoc "$LETTER_PATH" \
  --template=templates/letter_template.tex \
  --pdf-engine=xelatex \
  -o "$OUTPUT_DIR/Letter_to_Rothbart_Web.pdf"

echo "✅ Letter PDF created: $OUTPUT_DIR/Letter_to_Rothbart_Web.pdf"
echo "📤 Ready for Discord sharing"

# Make the PDF web-optimized
python3 scripts/optimize-pdf.py "$OUTPUT_DIR/Letter_to_Rothbart_Web.pdf" "$OUTPUT_DIR/Letter_to_Rothbart_Web.pdf" "web"