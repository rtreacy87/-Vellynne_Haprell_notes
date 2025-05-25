!/bin/bash

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

deactivate
