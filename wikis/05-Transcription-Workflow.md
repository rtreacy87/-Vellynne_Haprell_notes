# 05 - Transcription Workflow

Complete process for converting D&D session audio to clean, analyzable text.

## Prerequisites Checklist

- [ ] Whisper AI installed (from 04-Transcription-Setup.md)
- [ ] Audio files downloaded and processed
- [ ] Transcription scripts ready

## Step 1: Prepare Audio File

```bash
# Check audio file quality
SESSION_NUM=01  # Replace with your session number
SESSION_DIR="sessions/session-${SESSION_NUM}"

# Find and verify audio file
find "${SESSION_DIR}/audio" -name "*.wav" -o -name "*.flac" -exec file {} \;

# If needed, convert/optimize audio
./scripts/process-audio.sh
```

## Step 2: Run Initial Transcription

```bash
# Activate Python environment
source vellynne-env/bin/activate

# Run transcription with different quality levels
cd "${SESSION_DIR}"

# Quick transcription (for testing)
whisper audio/processed/*.wav --model base --output_format txt

# High-quality transcription (recommended)
whisper audio/processed/*.wav \
    --model medium \
    --language en \
    --temperature 0.2 \
    --output_format txt \
    --output_format srt \
    --verbose True
```

## Step 3: Clean and Format Transcript

```bash
# Use the cleaning script
python3 ../../scripts/clean-transcript.py \
    "$(basename *.txt)" \
    "cleaned_transcript.txt"

# Manual cleaning checklist:
echo "📝 Manual Review Checklist:"
echo "- Fix character names and D&D terms"
echo "- Identify speaker changes"
echo "- Correct spell names and game mechanics"
echo "- Remove filler words and false starts"
echo "- Add paragraph breaks for clarity"
```

## Step 4: Extract Key Information

```bash
# Run content analysis
python3 ../../scripts/analyze-transcript.py cleaned_transcript.txt

# Create manual notes file
cat > key_moments.md << 'EOF'
# Session Key Moments

## Combat Encounters
- [ ] Encounter 1: [Description]
- [ ] Encounter 2: [Description]

## Story Developments
- [ ] Plot point 1: [Description]
- [ ] Character development: [Description]

## Magic & Discoveries
- [ ] Spell/magic item: [Description]
- [ ] Lore discovery: [Description]

## Memorable Quotes
- "[Quote 1]" - Character
- "[Quote 2]" - Character

## Vellynne's Interests
- [ ] Undead encounters: [Details]
- [ ] Magical phenomena: [Details]
- [ ] Research opportunities: [Details]
EOF
```

## Step 5: Create Content Outline

```bash
cat > content_outline.md << 'EOF'
# Session Content Outline for Vellynne's Journal

## Initial Observations
**Target: 150 words**
- Weather/environment in Icewind Dale
- Party status and location
- Vellynne's initial thoughts

## Magical Phenomena Recorded
**Target: 200 words**
- Spells witnessed during session
- Magical items discovered or used
- Arcane environmental effects

## Specimen Studies
**Target: 250 words**
- Creatures encountered (especially undead)
- Behavioral observations
- Combat effectiveness notes

## Party Analysis
**Target: 200 words**
- Individual character performance
- Group tactics and coordination
- Magical abilities demonstrated

## Research Implications
**Target: 200 words**
- Connections to Vellynne's studies
- New questions raised
- Future research directions

## Illustrations Needed
- [ ] Creature sketch: [Description]
- [ ] Magical diagram: [Description]
- [ ] Location map: [Description]
- [ ] Item study: [Description]
EOF
```

## Step 6: Quality Assurance

```bash
# Run quality check
../../scripts/transcript-quality.sh

# Create review checklist
cat > review_checklist.md << 'EOF'
# Transcript Review Checklist

## Accuracy (Target: 95%+)
- [ ] Character names spelled correctly
- [ ] D&D terms and mechanics accurate
- [ ] Location names consistent
- [ ] Spell names correct

## Completeness
- [ ] All major story beats captured
- [ ] Combat encounters documented
- [ ] Character interactions preserved
- [ ] Important quotes identified

## Formatting
- [ ] Clear paragraph breaks
- [ ] Speaker identification where needed
- [ ] Consistent terminology
- [ ] Readable flow

## Content Analysis
- [ ] Key moments tagged
- [ ] Vellynne-relevant content highlighted
- [ ] Research connections noted
- [ ] Illustration opportunities marked
EOF
```

## Step 7: Prepare for Content Creation

```bash
# Update session status
jq '.status = "ready_for_writing" | .transcription_complete = now' \
   session-info.json > session-info.json.tmp && \
   mv session-info.json.tmp session-info.json

# Create writing workspace
mkdir -p ../content
cp content_outline.md ../content/
cp key_moments.md ../content/

echo "✅ Transcription workflow complete!"
echo "📁 Files ready for content creation:"
echo "   - cleaned_transcript.txt"
echo "   - content_outline.md"
echo "   - key_moments.md"
echo "   - cleaned_transcript_analysis.json"
```

## Advanced Techniques

### Speaker Identification
```bash
# If you have individual tracks from Craig
for track in audio/individual/*.wav; do
    speaker_name=$(basename "$track" .wav)
    whisper "$track" --output_format txt --output_dir "transcript/speakers/"
    mv "transcript/speakers/"*.txt "transcript/speakers/${speaker_name}.txt"
done
```

### Timestamp Preservation
```bash
# Keep timestamps for reference
whisper audio/processed/*.wav \
    --model medium \
    --output_format srt \
    --word_timestamps True

# Extract important timestamps
grep -n "combat\|spell\|discovery" *.srt > important_timestamps.txt
```

### Batch Processing
```bash
# Process multiple sessions
for session in sessions/session-*; do
    if [ -f "$session/audio/processed/"*.wav ]; then
        echo "Processing $(basename $session)..."
        cd "$session"
        whisper audio/processed/*.wav --model medium --output_format txt
        cd ../..
    fi
done
```

## Troubleshooting

### Poor Transcription Quality
1. **Check audio quality**: Ensure clear recording, minimal background noise
2. **Try different models**: Start with `base`, upgrade to `medium` or `large`
3. **Adjust temperature**: Lower values (0.0-0.2) for more conservative transcription
4. **Split long files**: Process in 30-60 minute chunks

### Memory Issues
```bash
# Use smaller model
whisper audio.wav --model tiny

# Process in chunks
ffmpeg -i audio.wav -f segment -segment_time 1800 -c copy chunk_%03d.wav
```

### Missing Content
1. **Manual review**: Listen to audio while reading transcript
2. **Check individual tracks**: Some speakers may be clearer on separate tracks
3. **Use SRT format**: Timestamps help identify missing sections
4. **Cross-reference**: Compare with session notes if available

## Quality Metrics

### Accuracy Targets
- **Character names**: 100% correct
- **D&D terminology**: 95% correct
- **General dialogue**: 90% correct
- **Background chatter**: 70% acceptable

### Completeness Targets
- **Major story beats**: 100% captured
- **Combat encounters**: 95% detailed
- **Character interactions**: 90% preserved
- **Rules discussions**: 80% documented

## Next Steps

With clean transcripts ready:

1. ✅ Audio successfully transcribed
2. ✅ Content cleaned and formatted
3. ✅ Key moments identified
4. ✅ Content outline created
5. ✅ Quality verified

Continue to **[06-Content-Analysis.md](06-Content-Analysis.md)** to analyze transcripts for Vellynne's journal content.

## Quick Reference

```bash
# Complete workflow
./scripts/full-transcription.sh

# Quality check
./scripts/transcript-quality.sh

# Manual transcription
whisper audio.wav --model medium --output_format txt
```
