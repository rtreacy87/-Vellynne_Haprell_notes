# 02 - Project Structure

Creating an organized project structure for efficient journal creation workflow.

## Prerequisites Checklist

- [ ] Environment setup completed (from 01-Environment-Setup.md)
- [ ] Basic command line familiarity
- [ ] Project directory created (`vellynne-notes`)

## Overview

We'll create a comprehensive folder structure that supports the entire workflow from audio recording to final PDF generation. This structure will help you stay organized as your collection of session journals grows.

## Step 1: Create Detailed Directory Structure

```bash
# Navigate to your project directory
cd vellynne-notes

# Create the complete directory structure
mkdir -p {
  audio/{raw,processed},
  transcripts/{raw,cleaned,analyzed},
  content/{drafts,final,templates},
  images/{generated,processed,assets},
  output/{pdf,web,archive},
  scripts/{transcription,content,images,layout},
  config,
  docs,
  resources/{fonts,textures,references}
}

# Create subdirectories for session organization
mkdir -p sessions/{session-{01..20}}

# Verify structure
tree -L 3 || find . -type d | sort
```

## Step 2: Create Configuration Files

### Main Configuration File
```bash
cat > config/settings.json << 'EOF'
{
  "project": {
    "name": "Vellynne Harpell Research Notes",
    "campaign": "Icewind Dale",
    "current_session": 1,
    "dm_name": "Your DM Name",
    "party_members": [
      "Character 1",
      "Character 2", 
      "Character 3",
      "Character 4"
    ]
  },
  "audio": {
    "format": "wav",
    "sample_rate": 44100,
    "channels": 2,
    "max_duration_hours": 6
  },
  "transcription": {
    "model": "base",
    "language": "en",
    "temperature": 0.2,
    "chunk_length": 30
  },
  "images": {
    "style": "medieval manuscript",
    "resolution": "1024x1024",
    "format": "png",
    "aging_intensity": 0.7
  },
  "output": {
    "pdf_dpi": 300,
    "page_size": "letter",
    "margins": "1in",
    "font_size": "12pt"
  }
}
EOF
```

### Session Template Configuration
```bash
cat > config/session-template.json << 'EOF'
{
  "header": {
    "title": "Research Notes of Vellynne Harpell",
    "subtitle": "Tenth Black Staff of Blackstaff Academy",
    "date_format": "Dale Reckoning",
    "session_format": "Session {number} - {title}"
  },
  "sections": [
    {
      "name": "Initial Observations",
      "description": "Session overview from Vellynne's perspective",
      "required": true,
      "word_count_target": 150
    },
    {
      "name": "Magical Phenomena Recorded", 
      "description": "Spells witnessed and arcane discoveries",
      "required": false,
      "word_count_target": 200
    },
    {
      "name": "Specimen Studies",
      "description": "Detailed notes on creatures encountered",
      "required": false,
      "word_count_target": 250
    },
    {
      "name": "Party Analysis",
      "description": "Combat effectiveness and tactical observations",
      "required": true,
      "word_count_target": 200
    },
    {
      "name": "Research Implications",
      "description": "Connections to ongoing studies and new questions",
      "required": true,
      "word_count_target": 200
    }
  ],
  "illustrations": {
    "minimum": 2,
    "maximum": 5,
    "types": ["creature_study", "magical_diagram", "location_map", "item_illustration"]
  }
}
EOF
```

## Step 3: Create Utility Scripts

### Session Management Script
```bash
cat > scripts/new-session.sh << 'EOF'
#!/bin/bash

# Get session number and title
read -p "Session number: " SESSION_NUM
read -p "Session title: " SESSION_TITLE
read -p "Session date (YYYY-MM-DD): " SESSION_DATE

# Pad session number with zeros
SESSION_PADDED=$(printf "%02d" $SESSION_NUM)

# Create session directory structure
SESSION_DIR="sessions/session-${SESSION_PADDED}"
mkdir -p "${SESSION_DIR}"/{audio,transcript,content,images,output}

# Create session info file
cat > "${SESSION_DIR}/session-info.json" << EOL
{
  "session_number": ${SESSION_NUM},
  "session_title": "${SESSION_TITLE}",
  "session_date": "${SESSION_DATE}",
  "created": "$(date -Iseconds)",
  "status": "planning",
  "files": {
    "audio": null,
    "transcript": null,
    "content": null,
    "images": [],
    "final_pdf": null
  }
}
EOL

# Create content template
cat > "${SESSION_DIR}/content/draft.md" << EOL
# Research Notes of Vellynne Harpell
## Tenth Black Staff of Blackstaff Academy
### ${SESSION_DATE} - Session ${SESSION_NUM}: ${SESSION_TITLE}

---

## Initial Observations

*Weather, location, party status from Vellynne's perspective*

[Write your observations here]

---

## Magical Phenomena Recorded

*Spells witnessed, their effects and variations*

[Document magical events here]

---

## Specimen Studies

*Detailed notes on undead/creatures encountered*

[Record creature observations here]

---

## Party Analysis

*Combat effectiveness observations and individual capabilities*

[Analyze party performance here]

---

## Research Implications

*How session events relate to ongoing studies*

[Connect to Vellynne's research here]

---

*End of Session ${SESSION_NUM} Notes*
EOL

echo "✅ Session ${SESSION_PADDED} created: ${SESSION_DIR}"
echo "📝 Draft template ready: ${SESSION_DIR}/content/draft.md"
echo "📁 Audio files go in: ${SESSION_DIR}/audio/"
echo "🎨 Images will be saved to: ${SESSION_DIR}/images/"
EOF

chmod +x scripts/new-session.sh
```

### Project Status Script
```bash
cat > scripts/status.sh << 'EOF'
#!/bin/bash

echo "📊 Vellynne Notes Project Status"
echo "================================"
echo

# Count sessions
SESSION_COUNT=$(find sessions -name "session-*" -type d | wc -l)
echo "📚 Total Sessions: ${SESSION_COUNT}"

# Check for audio files
AUDIO_COUNT=$(find sessions -name "*.wav" -o -name "*.mp3" -o -name "*.m4a" | wc -l)
echo "🎙️  Audio Files: ${AUDIO_COUNT}"

# Check for transcripts
TRANSCRIPT_COUNT=$(find sessions -name "*transcript*" | wc -l)
echo "📝 Transcripts: ${TRANSCRIPT_COUNT}"

# Check for generated images
IMAGE_COUNT=$(find sessions -name "*.png" -o -name "*.jpg" | wc -l)
echo "🎨 Generated Images: ${IMAGE_COUNT}"

# Check for final PDFs
PDF_COUNT=$(find sessions -name "*.pdf" | wc -l)
echo "📄 Final PDFs: ${PDF_COUNT}"

echo
echo "📁 Recent Sessions:"
find sessions -name "session-info.json" -exec dirname {} \; | sort | tail -5 | while read session_dir; do
    if [ -f "${session_dir}/session-info.json" ]; then
        title=$(jq -r '.session_title' "${session_dir}/session-info.json" 2>/dev/null || echo "Unknown")
        date=$(jq -r '.session_date' "${session_dir}/session-info.json" 2>/dev/null || echo "Unknown")
        status=$(jq -r '.status' "${session_dir}/session-info.json" 2>/dev/null || echo "Unknown")
        echo "  $(basename $session_dir): $title ($date) - $status"
    fi
done

echo
echo "💾 Disk Usage:"
du -sh . 2>/dev/null || echo "Unable to calculate disk usage"
EOF

chmod +x scripts/status.sh
```

## Step 4: Create Resource Directories

### Download Essential Resources
```bash
# Create placeholder files for resources
cat > resources/fonts/README.md << 'EOF'
# Fonts for Vellynne's Notes

Place medieval/manuscript style fonts here:

## Recommended Fonts:
- **Headers**: Cinzel, Uncial Antiqua, or similar Gothic fonts
- **Body Text**: EB Garamond, Crimson Text, or similar serif fonts  
- **Handwriting**: Kalam, Caveat, or similar script fonts

## Free Font Sources:
- Google Fonts (fonts.google.com)
- Font Squirrel (fontsquirrel.com)
- DaFont (dafont.com) - check licenses

## Installation:
1. Download font files (.ttf or .otf)
2. Place in this directory
3. Install on your system for use in layout software
EOF

cat > resources/textures/README.md << 'EOF'
# Textures and Backgrounds

Place parchment, paper, and aging textures here:

## Recommended Textures:
- Aged parchment backgrounds
- Paper textures with stains
- Ink blot overlays
- Wax seal images
- Border decorations

## Free Texture Sources:
- Unsplash (unsplash.com)
- Pixabay (pixabay.com)
- Freepik (freepik.com) - check attribution requirements

## File Formats:
- High resolution PNG or JPG
- Minimum 300 DPI for print quality
- Transparent PNG for overlays
EOF

cat > resources/references/README.md << 'EOF'
# Reference Materials

Store reference images and documents here:

## Character References:
- Vellynne Harpell official artwork
- Icewind Dale location maps
- D&D monster manual images
- Medieval manuscript examples

## Style References:
- Leonardo da Vinci's notebooks
- Medieval illuminated manuscripts
- Scientific illustration examples
- Fantasy art references

## Campaign Materials:
- Session notes from DM
- Character sheets
- Campaign timeline
- Location descriptions
EOF
```

## Step 5: Create Documentation

```bash
cat > docs/workflow.md << 'EOF'
# Vellynne Notes Workflow

## Quick Reference

### Starting a New Session
1. `./scripts/new-session.sh` - Create session structure
2. Record session with Craig bot
3. Download audio to `sessions/session-XX/audio/`

### Processing Workflow
1. **Transcribe**: `whisper audio.wav --output_dir transcript/`
2. **Analyze**: Review transcript for key moments
3. **Write**: Fill in content template in Vellynne's voice
4. **Illustrate**: Generate images with AI tools
5. **Layout**: Assemble final document
6. **Export**: Create PDF for distribution

### File Naming Convention
- Audio: `Session_XX_YYYY-MM-DD.wav`
- Transcript: `Session_XX_YYYY-MM-DD_transcript.txt`
- Content: `Session_XX_YYYY-MM-DD_journal.md`
- Final: `Vellynne_Notes_Session_XX.pdf`

### Quality Checklist
- [ ] Transcription accuracy >95%
- [ ] Content captures session highlights
- [ ] Images match medieval manuscript style
- [ ] Layout is readable and authentic
- [ ] PDF is high resolution (300 DPI)
EOF

cat > docs/troubleshooting.md << 'EOF'
# Troubleshooting Guide

## Common Issues

### Audio Processing
**Problem**: Whisper fails to transcribe
- Check audio file format (WAV recommended)
- Ensure file isn't corrupted
- Try smaller chunk sizes

**Problem**: Poor transcription quality
- Use higher quality audio recording
- Reduce background noise
- Try different Whisper model (small, medium, large)

### Image Generation
**Problem**: Images don't match style
- Refine prompts with more specific descriptors
- Use style references in prompts
- Adjust generation parameters

**Problem**: API rate limits
- Implement delays between requests
- Use local Stable Diffusion instead
- Batch process images

### Layout Issues
**Problem**: Fonts not displaying correctly
- Ensure fonts are installed system-wide
- Check font file formats
- Use fallback fonts in templates

**Problem**: Images not positioning correctly
- Check image resolution and aspect ratio
- Adjust layout template margins
- Use consistent image sizes
EOF
```

## Step 6: Initialize Version Control

```bash
# Add all new files to git
git add .

# Create initial commit
git commit -m "Complete project structure setup

- Created organized directory structure
- Added configuration files and templates
- Created utility scripts for session management
- Added documentation and troubleshooting guides
- Set up resource directories for fonts and textures"

# Create development branch
git checkout -b development

# Return to main branch
git checkout main

echo "✅ Project structure complete!"
echo "📁 Use './scripts/status.sh' to check project status"
echo "🆕 Use './scripts/new-session.sh' to create a new session"
```

## Directory Structure Overview

```
vellynne-notes/
├── audio/                  # Raw and processed audio files
├── sessions/              # Individual session directories
│   └── session-XX/        # Each session's complete workflow
├── scripts/               # Automation and utility scripts
├── config/                # Configuration files and templates
├── resources/             # Fonts, textures, and references
├── docs/                  # Documentation and guides
└── output/                # Final PDFs and archives
```

## Next Steps

With your project structure in place:

1. ✅ Organized directory structure created
2. ✅ Configuration files set up
3. ✅ Utility scripts ready
4. ✅ Documentation in place
5. ✅ Version control initialized

Continue to **[03-Audio-Capture.md](03-Audio-Capture.md)** to set up session recording with Craig bot.

## Tips for Organization

- **Use the session scripts**: They maintain consistent naming and structure
- **Keep sessions separate**: Each session gets its own complete directory
- **Version control regularly**: Commit after each major step
- **Document as you go**: Update session-info.json files with progress
- **Clean up regularly**: Archive completed sessions to keep workspace tidy
