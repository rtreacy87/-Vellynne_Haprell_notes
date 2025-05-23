# 04 - Transcription Setup

Installing and configuring Whisper AI for converting D&D session audio to text.

## Prerequisites Checklist

- [ ] Python environment set up (from 01-Environment-Setup.md)
- [ ] Audio files from Craig bot recording
- [ ] Virtual environment activated

## Step 1: Install Whisper AI

```bash
# Activate virtual environment
source vellynne-env/bin/activate

# Install Whisper and dependencies
pip install openai-whisper torch torchaudio

# Verify installation
whisper --help
```

## Step 2: Create Transcription Script

```bash
cat > scripts/transcribe.sh << 'EOF'
#!/bin/bash

read -p "Session number: " SESSION_NUM
SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

# Find audio file
AUDIO_FILE=$(find "${SESSION_DIR}/audio" -name "*.wav" -o -name "*.flac" | head -n1)

if [ -z "$AUDIO_FILE" ]; then
    echo "❌ No audio file found in ${SESSION_DIR}/audio/"
    exit 1
fi

echo "🎙️ Transcribing: $(basename "$AUDIO_FILE")"

# Activate virtual environment
source vellynne-env/bin/activate

# Create transcript directory
mkdir -p "${SESSION_DIR}/transcript"

# Run Whisper transcription
whisper "$AUDIO_FILE" \
    --model medium \
    --language en \
    --output_dir "${SESSION_DIR}/transcript" \
    --output_format txt \
    --verbose True

# Rename output file
mv "${SESSION_DIR}/transcript/"*.txt "${SESSION_DIR}/transcript/raw_transcript.txt"

echo "✅ Transcription complete!"
echo "📁 Output: ${SESSION_DIR}/transcript/raw_transcript.txt"
EOF

chmod +x scripts/transcribe.sh
```

## Step 3: Create Transcript Cleaning Script

```bash
cat > scripts/clean-transcript.py << 'EOF'
#!/usr/bin/env python3
import sys
import re
import json
from pathlib import Path

def clean_transcript(input_file, output_file):
    """Clean and format raw Whisper transcript"""
    
    with open(input_file, 'r') as f:
        text = f.read()
    
    # Remove timestamps and speaker labels
    text = re.sub(r'\[\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+\]', '', text)
    text = re.sub(r'Speaker \d+:', '', text)
    
    # Fix common transcription errors
    replacements = {
        'D and D': 'D&D',
        'dungeon master': 'DM',
        'dice roll': 'dice roll',
        'twenty sided': 'd20',
        'armor class': 'AC',
        'hit points': 'HP'
    }
    
    for old, new in replacements.items():
        text = re.sub(old, new, text, flags=re.IGNORECASE)
    
    # Clean up spacing and formatting
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)
    text = text.strip()
    
    # Split into paragraphs (rough speaker changes)
    paragraphs = text.split('\n')
    formatted_text = '\n\n'.join(p.strip() for p in paragraphs if p.strip())
    
    with open(output_file, 'w') as f:
        f.write(formatted_text)
    
    return len(paragraphs), len(text.split())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean-transcript.py input.txt output.txt")
        sys.exit(1)
    
    input_file, output_file = sys.argv[1], sys.argv[2]
    paragraphs, words = clean_transcript(input_file, output_file)
    
    print(f"✅ Transcript cleaned: {paragraphs} paragraphs, {words} words")
    print(f"📁 Output: {output_file}")
EOF

chmod +x scripts/clean-transcript.py
```

## Step 4: Create Analysis Script

```bash
cat > scripts/analyze-transcript.py << 'EOF'
#!/usr/bin/env python3
import sys
import re
import json
from collections import Counter

def analyze_transcript(transcript_file):
    """Extract key moments and themes from transcript"""
    
    with open(transcript_file, 'r') as f:
        text = f.read()
    
    # Keywords for different categories
    combat_keywords = ['attack', 'damage', 'roll', 'initiative', 'spell', 'cast']
    magic_keywords = ['magic', 'spell', 'enchant', 'arcane', 'ritual', 'potion']
    creature_keywords = ['monster', 'undead', 'zombie', 'skeleton', 'dragon', 'giant']
    location_keywords = ['town', 'dungeon', 'cave', 'forest', 'mountain', 'ruins']
    
    analysis = {
        'word_count': len(text.split()),
        'combat_mentions': count_keywords(text, combat_keywords),
        'magic_mentions': count_keywords(text, magic_keywords),
        'creature_mentions': count_keywords(text, creature_keywords),
        'location_mentions': count_keywords(text, location_keywords),
        'key_quotes': extract_quotes(text),
        'timestamps': extract_timestamps(text)
    }
    
    return analysis

def count_keywords(text, keywords):
    """Count mentions of keywords in text"""
    count = 0
    for keyword in keywords:
        count += len(re.findall(keyword, text, re.IGNORECASE))
    return count

def extract_quotes(text):
    """Extract memorable quotes from transcript"""
    sentences = re.split(r'[.!?]+', text)
    quotes = []
    
    # Look for emotional or dramatic sentences
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['amazing', 'incredible', 'oh no', 'yes!', 'critical']):
            quotes.append(sentence.strip())
    
    return quotes[:5]  # Top 5 quotes

def extract_timestamps(text):
    """Extract important moments with rough timestamps"""
    # This is a simplified version - in practice you'd use the audio timestamps
    paragraphs = text.split('\n\n')
    timestamps = []
    
    for i, paragraph in enumerate(paragraphs):
        if any(word in paragraph.lower() for word in ['combat', 'fight', 'attack', 'spell']):
            timestamps.append({
                'paragraph': i + 1,
                'type': 'combat',
                'content': paragraph[:100] + '...'
            })
    
    return timestamps

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze-transcript.py transcript.txt")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    analysis = analyze_transcript(transcript_file)
    
    # Save analysis
    output_file = transcript_file.replace('.txt', '_analysis.json')
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"📊 Analysis complete:")
    print(f"   Words: {analysis['word_count']}")
    print(f"   Combat mentions: {analysis['combat_mentions']}")
    print(f"   Magic mentions: {analysis['magic_mentions']}")
    print(f"   Key moments: {len(analysis['timestamps'])}")
    print(f"📁 Analysis saved: {output_file}")
EOF

chmod +x scripts/analyze-transcript.py
```

## Step 5: Complete Transcription Workflow

```bash
cat > scripts/full-transcription.sh << 'EOF'
#!/bin/bash

read -p "Session number: " SESSION_NUM
SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "🎯 Full Transcription Workflow for Session ${SESSION_PADDED}"
echo "=================================================="

# Step 1: Transcribe audio
echo "Step 1: Transcribing audio..."
./scripts/transcribe.sh

# Step 2: Clean transcript
echo "Step 2: Cleaning transcript..."
python3 scripts/clean-transcript.py \
    "${SESSION_DIR}/transcript/raw_transcript.txt" \
    "${SESSION_DIR}/transcript/cleaned_transcript.txt"

# Step 3: Analyze content
echo "Step 3: Analyzing content..."
python3 scripts/analyze-transcript.py \
    "${SESSION_DIR}/transcript/cleaned_transcript.txt"

# Step 4: Update session info
if [ -f "${SESSION_DIR}/session-info.json" ]; then
    jq '.status = "transcribed" | .files.transcript = "cleaned_transcript.txt"' \
       "${SESSION_DIR}/session-info.json" > "${SESSION_DIR}/session-info.json.tmp" && \
       mv "${SESSION_DIR}/session-info.json.tmp" "${SESSION_DIR}/session-info.json"
fi

echo "✅ Transcription workflow complete!"
echo "📁 Files created:"
echo "   - Raw transcript: ${SESSION_DIR}/transcript/raw_transcript.txt"
echo "   - Cleaned transcript: ${SESSION_DIR}/transcript/cleaned_transcript.txt"
echo "   - Analysis: ${SESSION_DIR}/transcript/cleaned_transcript_analysis.json"
echo
echo "🎯 Ready for content creation!"
EOF

chmod +x scripts/full-transcription.sh
```

## Step 6: Quality Control

```bash
cat > scripts/transcript-quality.sh << 'EOF'
#!/bin/bash

read -p "Session number: " SESSION_NUM
SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

TRANSCRIPT="${SESSION_DIR}/transcript/cleaned_transcript.txt"

if [ ! -f "$TRANSCRIPT" ]; then
    echo "❌ Transcript not found: $TRANSCRIPT"
    exit 1
fi

echo "📊 Transcript Quality Report"
echo "==========================="

# Basic stats
WORD_COUNT=$(wc -w < "$TRANSCRIPT")
LINE_COUNT=$(wc -l < "$TRANSCRIPT")
CHAR_COUNT=$(wc -c < "$TRANSCRIPT")

echo "📝 Basic Statistics:"
echo "   Words: $WORD_COUNT"
echo "   Lines: $LINE_COUNT"
echo "   Characters: $CHAR_COUNT"

# Check for common issues
echo
echo "🔍 Quality Checks:"

# Check for repeated phrases (transcription errors)
REPEATED=$(grep -o '\b\w\+\s\+\1\b' "$TRANSCRIPT" | wc -l)
echo "   Repeated words: $REPEATED"

# Check for incomplete sentences
INCOMPLETE=$(grep -c '\.\.\.' "$TRANSCRIPT")
echo "   Incomplete sentences: $INCOMPLETE"

# Check for speaker identification
SPEAKERS=$(grep -c -i 'speaker\|player\|dm' "$TRANSCRIPT")
echo "   Speaker references: $SPEAKERS"

# Estimate session length (rough: 150 words per minute)
ESTIMATED_MINUTES=$((WORD_COUNT / 150))
echo "   Estimated session length: ${ESTIMATED_MINUTES} minutes"

echo
if [ $WORD_COUNT -gt 1000 ] && [ $REPEATED -lt 10 ]; then
    echo "✅ Transcript quality: Good"
else
    echo "⚠️  Transcript may need manual review"
fi
EOF

chmod +x scripts/transcript-quality.sh
```

## Troubleshooting

### Common Issues
- **Whisper fails**: Check audio format (WAV preferred), reduce file size
- **Poor accuracy**: Try different model sizes (tiny/base/small/medium/large)
- **Memory errors**: Use smaller audio chunks or lighter model
- **Missing words**: Manual review and correction needed

### Model Selection
- `tiny`: Fastest, lowest accuracy
- `base`: Good balance for most sessions
- `medium`: Better accuracy, slower (recommended)
- `large`: Best accuracy, requires more memory

## Next Steps

With transcription set up:

1. ✅ Whisper AI installed and configured
2. ✅ Transcription workflow created
3. ✅ Cleaning and analysis scripts ready
4. ✅ Quality control measures in place

Continue to **[05-Transcription-Workflow.md](05-Transcription-Workflow.md)** for the complete process of converting audio to usable text.

## Quick Commands

```bash
# Full transcription workflow
./scripts/full-transcription.sh

# Check transcript quality
./scripts/transcript-quality.sh

# Manual transcription only
./scripts/transcribe.sh
```
