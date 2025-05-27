# Rothbart Letter Automation System

This document outlines the automated workflow for generating Vellynne Harpell's letters to Rothbart based on D&D session recordings.

## Overview

The system consists of three main components:
1. **Session Recording & Transcription** - Creates session directory and transcribes audio
2. **Transcript Analysis & Summarization** - Processes transcript to extract key events
3. **Letter Generation** - Creates a new letter using the template and previous letters

## 1. Session Recording & Transcription

### Script: `scripts/transcribe-session.sh`

```bash
#!/bin/bash

# Check if session number was provided
if [ -z "$1" ]; then
  echo "❌ Error: Session number required"
  echo "Usage: ./scripts/transcribe-session.sh SESSION_NUM"
  exit 1
fi

# Get session number and pad with zeros
SESSION_NUM=$1
SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create session directory
SESSION_DIR="vellynne-notes/session${SESSION_PADDED}"
mkdir -p "${SESSION_DIR}/audio"
mkdir -p "${SESSION_DIR}/transcript"
mkdir -p "${SESSION_DIR}/content"
mkdir -p "${SESSION_DIR}/output"

echo "📁 Created session directory: ${SESSION_DIR}"

# Find audio file (assumes it's already in the audio directory)
AUDIO_FILE=$(find "${SESSION_DIR}/audio" -name "*.wav" -o -name "*.flac" | head -n1)

if [ -z "$AUDIO_FILE" ]; then
    echo "❌ No audio file found in ${SESSION_DIR}/audio/"
    echo "Please place your session recording in ${SESSION_DIR}/audio/"
    exit 1
fi

echo "🎙️ Found audio file: $(basename "$AUDIO_FILE")"

# Activate virtual environment
source vellynne-env/bin/activate

echo "🔄 Transcribing audio with Whisper..."

# Run Whisper transcription
whisper "$AUDIO_FILE" \
    --model medium \
    --language en \
    --output_dir "${SESSION_DIR}/transcript" \
    --output_format txt \
    --verbose True

# Rename output file with timestamp
TRANSCRIPT_FILE="${SESSION_DIR}/transcript/session${SESSION_PADDED}_transcript_${TIMESTAMP}.txt"
mv "${SESSION_DIR}/transcript/"*.txt "$TRANSCRIPT_FILE"

echo "✅ Transcription complete!"
echo "📄 Transcript saved to: $TRANSCRIPT_FILE"

# Deactivate virtual environment
deactivate

# Create summarization instructions file
echo "📝 Creating summarization instructions..."
cat > "${SESSION_DIR}/transcript/summarization_instructions.md" << EOL
# Session ${SESSION_PADDED} Transcript Summarization Instructions

## Input File
- Transcript: \`$(basename "$TRANSCRIPT_FILE")\`

## Steps for Summarization

1. Review the transcript in \`${SESSION_DIR}/transcript/$(basename "$TRANSCRIPT_FILE")\`
2. Extract the following key information:
   - Main events and encounters
   - NPCs encountered
   - Combat details (especially involving Rothbart)
   - Discoveries and revelations
   - Items acquired
   - Locations visited
   - Any vampire or undead-related information
   - Information relevant to Rothbart's dampir nature

3. Format the summary as bullet points under appropriate headings
4. Save the summary to \`${SESSION_DIR}/content/session${SESSION_PADDED}_summary_${TIMESTAMP}.md\`

## Example Summary Format

\`\`\`markdown
# Session ${SESSION_PADDED} Summary

## Key Events
- [Event 1]
- [Event 2]

## Combat Encounters
- [Combat details]

## NPCs
- [NPC interactions]

## Discoveries
- [Important revelations]

## Items & Locations
- [Relevant items and places]

## Undead & Vampire Information
- [Details relevant to Rothbart]
\`\`\`

## Next Steps
After completing the summary, proceed to letter generation using:
\`./scripts/generate-rothbart-letter.sh ${SESSION_NUM}\`
EOL

echo "✅ Setup complete for Session ${SESSION_PADDED}"
echo "📋 Next steps:"
echo "1. Review and summarize the transcript following instructions in:"
echo "   ${SESSION_DIR}/transcript/summarization_instructions.md"
echo "2. After summarization, run the letter generation script:"
echo "   ./scripts/generate-rothbart-letter.sh ${SESSION_NUM}"
```

## 2. Transcript Analysis & Summarization

This is a manual step guided by the instructions generated in the previous script. The user will:

1. Review the transcript
2. Create a summary following the provided format
3. Save the summary to the content directory

## 3. Letter Generation

### Script: `scripts/generate-rothbart-letter.sh`

```bash
#!/bin/bash

# Check if session number was provided
if [ -z "$1" ]; then
  echo "❌ Error: Session number required"
  echo "Usage: ./scripts/generate-rothbart-letter.sh SESSION_NUM"
  exit 1
fi

# Get session number and pad with zeros
SESSION_NUM=$1
SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Set up directories
SESSION_DIR="vellynne-notes/session${SESSION_PADDED}"
TEMPLATE_PATH="content/letter_template.md"

# Check if session directory exists
if [ ! -d "$SESSION_DIR" ]; then
    echo "❌ Session directory not found: ${SESSION_DIR}"
    exit 1
fi

# Find the latest summary file
SUMMARY_FILE=$(find "${SESSION_DIR}/content" -name "session${SESSION_PADDED}_summary_*.md" | sort | tail -n1)

if [ -z "$SUMMARY_FILE" ]; then
    echo "❌ No summary file found in ${SESSION_DIR}/content/"
    echo "Please create a summary file first following the instructions in:"
    echo "${SESSION_DIR}/transcript/summarization_instructions.md"
    exit 1
fi

echo "📄 Found summary file: $(basename "$SUMMARY_FILE")"

# Find previous letters (up to 2 most recent)
PREV_LETTERS=$(find vellynne-notes -name "letter-to-rothbart.md" | grep -v "session${SESSION_PADDED}" | sort -r | head -n2)

# Create letter generation instructions
LETTER_INSTRUCTIONS="${SESSION_DIR}/content/letter_generation_instructions.md"

echo "📝 Creating letter generation instructions..."
cat > "$LETTER_INSTRUCTIONS" << EOL
# Letter to Rothbart Generation Instructions - Session ${SESSION_PADDED}

## Input Files
- Template: \`${TEMPLATE_PATH}\`
- Summary: \`$(basename "$SUMMARY_FILE")\`
EOL

# Add previous letters to instructions if found
if [ ! -z "$PREV_LETTERS" ]; then
    echo "- Previous Letters:" >> "$LETTER_INSTRUCTIONS"
    for letter in $PREV_LETTERS; do
        echo "  - \`$letter\`" >> "$LETTER_INSTRUCTIONS"
    done
fi

# Continue with instructions
cat >> "$LETTER_INSTRUCTIONS" << EOL

## Task
Generate a new letter from Vellynne Harpell to Rothbart based on the session summary, using the letter template and referencing previous letters for tone and continuity.

## Requirements
1. Follow the structure of the template
2. Replace placeholder text with content from the summary
3. Maintain Vellynne's scholarly, slightly teasing tone
4. Include references to:
   - Rothbart's dampir nature
   - Vellynne's necromantic research
   - Their philosophical differences
   - Helpful information or items
5. Add at least one diagram or illustration reference
6. Include a postscript with an additional detail or tease

## Output
Save the completed letter as \`${SESSION_DIR}/letter-to-rothbart.md\`

## Next Steps
After generating the letter:
1. Review and edit for tone and content
2. If you want to convert to other formats, use:
   \`./scripts/convert-letter-format.sh ${SESSION_NUM} [format]\`
   Where format can be html, pdf, or all
EOL

# Create a starter letter file
LETTER_FILE="${SESSION_DIR}/letter-to-rothbart.md"
CURRENT_DATE=$(date +"%Y-%m-%d")

echo "📄 Creating starter letter file..."
cat > "$LETTER_FILE" << EOL
# Correspondence from Vellynne Harpell
## Tenth Black Staff of Blackstaff Academy
### ${CURRENT_DATE} - To: Rothbart

*Delivered by raven familiar*

---

Dear Rothbart,

[REPLACE WITH PERSONALIZED GREETING REFERENCING RECENT EVENTS FROM SUMMARY]

[PARAGRAPH 1: REFERENCE ROTHBART'S ACTIONS FROM THE SUMMARY, ESPECIALLY RELATED TO UNDEAD]

[PARAGRAPH 2: SCHOLARLY OBSERVATIONS ABOUT SOMETHING FROM THE SUMMARY]

[PARAGRAPH 3: REQUEST FOR INFORMATION FRAMED AS ACADEMIC INTEREST]

[PARAGRAPH 4: OFFER HELPFUL INFORMATION OR ITEM]

[PARAGRAPH 5: CLOSING WITH CONCERN AND TEASING]

With scholarly interest and perpetual amusement,

*Vellynne Harpell*
Tenth Black Staff of Blackstaff Academy

P.S. [ADD POSTSCRIPT WITH ADDITIONAL DETAIL OR TEASE]

---

**Enclosed:**
- [ITEM OR INFORMATION RELEVANT TO THE SESSION]

![Diagram: [DESCRIPTION]](images/diagram1.png)
EOL

echo "✅ Letter generation setup complete!"
echo "📋 Next steps:"
echo "1. Review the letter generation instructions:"
echo "   $LETTER_INSTRUCTIONS"
echo "2. Edit the starter letter file:"
echo "   $LETTER_FILE"
echo "3. After completing the letter, you can convert it to other formats using:"
echo "   ./scripts/convert-letter-format.sh ${SESSION_NUM} [format]"
```

## 4. Format Conversion (Optional)

### Script: `scripts/convert-letter-format.sh`

```bash
#!/bin/bash

# Check if session number was provided
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "❌ Error: Session number and format required"
  echo "Usage: ./scripts/convert-letter-format.sh SESSION_NUM FORMAT"
  echo "Formats: html, pdf, all"
  exit 1
fi

# Get session number and pad with zeros
SESSION_NUM=$1
SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
FORMAT=$2

# Set up directories
SESSION_DIR="vellynne-notes/session${SESSION_PADDED}"
LETTER_FILE="${SESSION_DIR}/letter-to-rothbart.md"
OUTPUT_DIR="${SESSION_DIR}/output"

# Check if letter file exists
if [ ! -f "$LETTER_FILE" ]; then
    echo "❌ Letter file not found: ${LETTER_FILE}"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function to convert to HTML
convert_to_html() {
    echo "🔄 Converting to HTML format..."
    
    # Generate HTML version
    pandoc "$LETTER_FILE" \
      --standalone \
      --template=templates/letter_template.html \
      -o "${OUTPUT_DIR}/letter-to-rothbart.html"
      
    echo "✅ HTML version created: ${OUTPUT_DIR}/letter-to-rothbart.html"
}

# Function to convert to PDF
convert_to_pdf() {
    echo "🔄 Converting to PDF format..."
    
    # Generate PDF version
    pandoc "$LETTER_FILE" \
      --template=templates/letter_template.tex \
      --pdf-engine=xelatex \
      -o "${OUTPUT_DIR}/letter-to-rothbart.pdf"
      
    echo "✅ PDF version created: ${OUTPUT_DIR}/letter-to-rothbart.pdf"
}

# Process based on format
case $FORMAT in
    "html")
        convert_to_html
        ;;
    "pdf")
        convert_to_pdf
        ;;
    "all")
        convert_to_html
        convert_to_pdf
        echo "✅ All formats generated successfully!"
        ;;
    *)
        echo "❌ Unknown format: $FORMAT"
        echo "Valid formats: html, pdf, all"
        exit 1
        ;;
esac

echo "🎉 Conversion complete!"
```

## Complete Workflow

### Master Script: `scripts/rothbart-letter-workflow.sh`

```bash
#!/bin/bash

# Check if session number was provided
if [ -z "$1" ]; then
  echo "❌ Error: Session number required"
  echo "Usage: ./scripts/rothbart-letter-workflow.sh SESSION_NUM"
  exit 1
fi

SESSION_NUM=$1
WORKFLOW_TYPE=${2:-"full"}

echo "🚀 Starting Rothbart Letter workflow for Session ${SESSION_NUM}"
echo "=================================================="

case $WORKFLOW_TYPE in
    "full")
        # Step 1: Transcription
        echo "🎙️ Step 1: Transcribing session..."
        ./scripts/transcribe-session.sh "$SESSION_NUM" || exit 1
        
        echo "⚠️ Manual step required: Summarize the transcript"
        echo "Follow instructions in vellynne-notes/session$(printf "%02d" $SESSION_NUM)/transcript/summarization_instructions.md"
        echo "Press Enter when summary is complete to continue..."
        read
        
        # Step 2: Letter Generation
        echo "✍️ Step 2: Setting up letter generation..."
        ./scripts/generate-rothbart-letter.sh "$SESSION_NUM" || exit 1
        
        echo "⚠️ Manual step required: Complete the letter"
        echo "Edit the letter in vellynne-notes/session$(printf "%02d" $SESSION_NUM)/letter-to-rothbart.md"
        echo "Press Enter when letter is complete to continue..."
        read
        
        echo "✅ Markdown letter workflow complete!"
        
        # Ask if user wants to convert to other formats
        read -p "Do you want to convert the letter to other formats? (y/n): " CONVERT
        if [[ $CONVERT == "y" ]]; then
            read -p "Which format? (html/pdf/all): " FORMAT
            ./scripts/convert-letter-format.sh "$SESSION_NUM" "$FORMAT"
        fi
        ;;
        
    "transcribe")
        # Just transcription
        echo "🎙️ Transcribing session..."
        ./scripts/transcribe-session.sh "$SESSION_NUM" || exit 1
        ;;
        
    "letter")
        # Just letter generation
        echo "✍️ Setting up letter generation..."
        ./scripts/generate-rothbart-letter.sh "$SESSION_NUM" || exit 1
        ;;
        
    "convert")
        # Just format conversion
        read -p "Which format? (html/pdf/all): " FORMAT
        ./scripts/convert-letter-format.sh "$SESSION_NUM" "$FORMAT"
        ;;
        
    *)
        echo "❌ Unknown workflow type: $WORKFLOW_TYPE"
        echo "Valid options: full, transcribe, letter, convert"
        exit 1
        ;;
esac

echo "🎉 Workflow complete for Session ${SESSION_NUM}!"
```

## Installation & Setup

1. Create the necessary directories:
   ```bash
   mkdir -p scripts templates content
   mkdir -p vellynne-notes
   ```

2. Make all scripts executable:
   ```bash
   chmod +x scripts/transcribe-session.sh
   chmod +x scripts/generate-rothbart-letter.sh
   chmod +x scripts/convert-letter-format.sh
   chmod +x scripts/rothbart-letter-workflow.sh
   ```

3. Create a letter template:
   ```bash
   mkdir -p content
   touch content/letter_template.md
   ```

4. Ensure dependencies are installed:
   - Whisper AI for transcription
   - Pandoc for format conversion (optional)
   - LaTeX for PDF generation (optional)

## Usage

### Full Workflow

```bash
./scripts/rothbart-letter-workflow.sh 01
```

This will:
1. Create session directory and transcribe audio
2. Prompt for manual summarization
3. Set up letter generation
4. Prompt for letter completion
5. Optionally convert to other formats

### Individual Steps

```bash
# Just transcription
./scripts/transcribe-session.sh 01

# Just letter generation setup
./scripts/generate-rothbart-letter.sh 01

# Convert to other formats (optional)
./scripts/convert-letter-format.sh 01 html
./scripts/convert-letter-format.sh 01 pdf
./scripts/convert-letter-format.sh 01 all
```

## Templates

The system relies on the following template:
- `content/letter_template.md` - Base template for Rothbart letters

Optional format conversion templates:
- `templates/letter_template.html` - HTML template
- `templates/letter_template.tex` - LaTeX template for PDF generation
