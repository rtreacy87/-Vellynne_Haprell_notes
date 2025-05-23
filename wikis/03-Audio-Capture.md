# 03 - Audio Capture

Setting up Craig bot for high-quality D&D session recording with separate participant tracks.

## Prerequisites Checklist

- [ ] Discord server with admin permissions
- [ ] D&D group uses Discord for voice chat
- [ ] Project structure set up (from 02-Project-Structure.md)
- [ ] Basic Discord bot management knowledge

## Overview

Craig is a Discord bot that records voice channels with separate tracks for each participant. This gives us clean audio for transcription and the ability to identify individual speakers.

## Step 1: Invite Craig Bot to Your Server

### Add Craig to Discord Server
```bash
# Open Craig's website
echo "🌐 Opening Craig bot website..."
echo "Visit: https://craig.chat/"
echo
echo "1. Click 'Invite Craig'"
echo "2. Select your D&D Discord server"
echo "3. Grant necessary permissions:"
echo "   - View Channels"
echo "   - Connect to Voice Channels"
echo "   - Use Voice Activity"
echo "   - Send Messages"
```

### Verify Craig Installation
```bash
# Create a test script to verify Craig is working
cat > scripts/test-craig.sh << 'EOF'
#!/bin/bash

echo "🎙️  Craig Bot Test Checklist"
echo "=========================="
echo
echo "In your Discord server:"
echo "1. Join a voice channel"
echo "2. Type: :craig:, join"
echo "3. Craig should join the voice channel"
echo "4. Type: :craig:, leave"
echo "5. Craig should leave and provide a download link"
echo
echo "✅ If Craig responds to commands, setup is complete!"
echo "❌ If Craig doesn't respond, check bot permissions"
EOF

chmod +x scripts/test-craig.sh
./scripts/test-craig.sh
```

## Step 2: Configure Craig for D&D Sessions

### Create Craig Configuration
```bash
cat > config/craig-settings.md << 'EOF'
# Craig Bot Configuration for D&D Sessions

## Basic Commands

### Start Recording
```
:craig:, join
```
- Craig joins voice channel and starts recording
- Each participant gets a separate audio track
- Recording starts immediately

### Stop Recording  
```
:craig:, leave
```
- Craig stops recording and leaves channel
- Provides download link via DM
- Files available for 7 days

## Advanced Options

### High Quality Recording
```
:craig:, join --format flac
```
- Records in FLAC format for highest quality
- Larger file sizes but better for transcription
- Recommended for important sessions

### Auto-Download Setup
```
:craig:, join --auto-download
```
- Automatically uploads to cloud storage
- Requires Craig premium subscription
- Good for regular campaigns

## Recording Best Practices

### Before Session
1. Test Craig in empty voice channel
2. Ensure all players have good microphones
3. Ask players to minimize background noise
4. Set up consistent naming convention

### During Session
1. Start Craig before players join
2. Announce recording start to group
3. Take note of important timestamps
4. Don't stop/start recording unnecessarily

### After Session
1. Stop Craig recording
2. Download files immediately
3. Rename files with session info
4. Back up to multiple locations
EOF
```

### Create Recording Workflow Script
```bash
cat > scripts/start-recording.sh << 'EOF'
#!/bin/bash

# Get session information
read -p "Session number: " SESSION_NUM
read -p "Session date (YYYY-MM-DD): " SESSION_DATE

# Pad session number
SESSION_PADDED=$(printf "%02d" $SESSION_NUM)

echo "🎙️  Starting Recording for Session ${SESSION_PADDED}"
echo "=============================================="
echo
echo "1. Join your D&D voice channel in Discord"
echo "2. Type in chat: :craig:, join --format flac"
echo "3. Wait for Craig to join and confirm recording"
echo "4. Announce to group: 'Recording started for session ${SESSION_NUM}'"
echo
echo "📝 Recording Details:"
echo "   Session: ${SESSION_NUM}"
echo "   Date: ${SESSION_DATE}"
echo "   Format: FLAC (high quality)"
echo "   Expected file: Session_${SESSION_PADDED}_${SESSION_DATE}.flac"
echo
echo "⏰ Remember to:"
echo "   - Note important timestamps during play"
echo "   - Stop recording with: :craig:, leave"
echo "   - Download files immediately after session"
echo
echo "Press Enter when recording has started..."
read

# Create session directory if it doesn't exist
SESSION_DIR="sessions/session-${SESSION_PADDED}"
mkdir -p "${SESSION_DIR}/audio"

# Update session info
if [ -f "${SESSION_DIR}/session-info.json" ]; then
    # Update existing session info
    jq --arg date "$SESSION_DATE" '.session_date = $date | .status = "recording"' \
       "${SESSION_DIR}/session-info.json" > "${SESSION_DIR}/session-info.json.tmp" && \
       mv "${SESSION_DIR}/session-info.json.tmp" "${SESSION_DIR}/session-info.json"
else
    # Create new session info
    cat > "${SESSION_DIR}/session-info.json" << EOL
{
  "session_number": ${SESSION_NUM},
  "session_date": "${SESSION_DATE}",
  "status": "recording",
  "recording_started": "$(date -Iseconds)",
  "files": {
    "audio": "Session_${SESSION_PADDED}_${SESSION_DATE}.flac",
    "transcript": null,
    "content": null,
    "images": [],
    "final_pdf": null
  }
}
EOL
fi

echo "✅ Session ${SESSION_PADDED} recording setup complete!"
echo "📁 Audio files should be saved to: ${SESSION_DIR}/audio/"
EOF

chmod +x scripts/start-recording.sh
```

## Step 3: Post-Recording Workflow

### Create Download Script
```bash
cat > scripts/download-audio.sh << 'EOF'
#!/bin/bash

read -p "Session number: " SESSION_NUM
SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "📥 Audio Download Workflow"
echo "========================="
echo
echo "1. Check your Discord DMs for Craig's download link"
echo "2. Download the audio files (usually a .zip)"
echo "3. Extract files to: ${SESSION_DIR}/audio/"
echo "4. Rename main file to: Session_${SESSION_PADDED}_YYYY-MM-DD.flac"
echo
echo "Expected directory structure:"
echo "${SESSION_DIR}/audio/"
echo "├── Session_${SESSION_PADDED}_YYYY-MM-DD.flac  (main mix)"
echo "├── participant1.flac                          (individual tracks)"
echo "├── participant2.flac"
echo "└── ..."
echo
echo "Press Enter when files are downloaded and organized..."
read

# Check if audio files exist
if [ -d "${SESSION_DIR}/audio" ] && [ "$(ls -A ${SESSION_DIR}/audio)" ]; then
    echo "✅ Audio files found in ${SESSION_DIR}/audio/"
    
    # List audio files
    echo "📁 Audio files:"
    ls -la "${SESSION_DIR}/audio/"
    
    # Update session status
    if [ -f "${SESSION_DIR}/session-info.json" ]; then
        jq '.status = "audio_ready" | .audio_downloaded = now' \
           "${SESSION_DIR}/session-info.json" > "${SESSION_DIR}/session-info.json.tmp" && \
           mv "${SESSION_DIR}/session-info.json.tmp" "${SESSION_DIR}/session-info.json"
    fi
    
    echo "✅ Ready for transcription!"
    echo "Next step: Run transcription workflow"
else
    echo "❌ No audio files found. Please check download location."
fi
EOF

chmod +x scripts/download-audio.sh
```

## Step 4: Audio Quality Optimization

### Create Audio Processing Script
```bash
cat > scripts/process-audio.sh << 'EOF'
#!/bin/bash

read -p "Session number: " SESSION_NUM
SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "🔧 Audio Processing for Session ${SESSION_PADDED}"
echo "=============================================="

# Check if FFmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg not found. Please install FFmpeg first."
    exit 1
fi

# Find the main audio file
AUDIO_FILE=$(find "${SESSION_DIR}/audio" -name "Session_${SESSION_PADDED}_*.flac" -o -name "Session_${SESSION_PADDED}_*.wav" | head -n1)

if [ -z "$AUDIO_FILE" ]; then
    echo "❌ No main audio file found. Expected: Session_${SESSION_PADDED}_*.flac"
    exit 1
fi

echo "📁 Processing: $(basename "$AUDIO_FILE")"

# Create processed directory
mkdir -p "${SESSION_DIR}/audio/processed"

# Convert to WAV if needed (Whisper prefers WAV)
if [[ "$AUDIO_FILE" == *.flac ]]; then
    OUTPUT_FILE="${SESSION_DIR}/audio/processed/$(basename "$AUDIO_FILE" .flac).wav"
    echo "🔄 Converting FLAC to WAV..."
    ffmpeg -i "$AUDIO_FILE" -ar 16000 -ac 1 "$OUTPUT_FILE" -y
else
    OUTPUT_FILE="${SESSION_DIR}/audio/processed/$(basename "$AUDIO_FILE")"
    echo "🔄 Optimizing WAV file..."
    ffmpeg -i "$AUDIO_FILE" -ar 16000 -ac 1 "$OUTPUT_FILE" -y
fi

# Apply noise reduction (optional)
read -p "Apply noise reduction? (y/n): " APPLY_NOISE_REDUCTION
if [[ $APPLY_NOISE_REDUCTION == "y" ]]; then
    CLEAN_FILE="${SESSION_DIR}/audio/processed/$(basename "$OUTPUT_FILE" .wav)_clean.wav"
    echo "🧹 Applying noise reduction..."
    ffmpeg -i "$OUTPUT_FILE" -af "highpass=f=200,lowpass=f=3000" "$CLEAN_FILE" -y
    OUTPUT_FILE="$CLEAN_FILE"
fi

# Get audio info
echo "📊 Audio Information:"
ffprobe -v quiet -show_format -show_streams "$OUTPUT_FILE" | grep -E "(duration|sample_rate|channels)"

# Update session info
if [ -f "${SESSION_DIR}/session-info.json" ]; then
    jq --arg file "$(basename "$OUTPUT_FILE")" '.files.audio = $file | .status = "audio_processed"' \
       "${SESSION_DIR}/session-info.json" > "${SESSION_DIR}/session-info.json.tmp" && \
       mv "${SESSION_DIR}/session-info.json.tmp" "${SESSION_DIR}/session-info.json"
fi

echo "✅ Audio processing complete!"
echo "📁 Processed file: $OUTPUT_FILE"
echo "🎯 Ready for transcription with Whisper AI"
EOF

chmod +x scripts/process-audio.sh
```

## Step 5: Recording Best Practices

### Create Best Practices Guide
```bash
cat > docs/recording-best-practices.md << 'EOF'
# Recording Best Practices for D&D Sessions

## Pre-Session Setup

### Technical Checklist
- [ ] Test Craig bot in empty voice channel
- [ ] Verify all players have working microphones
- [ ] Check Discord voice settings (noise suppression OFF)
- [ ] Ensure stable internet connection for all participants
- [ ] Have backup recording method ready

### Communication
- [ ] Inform all players about recording
- [ ] Explain purpose (creating session journals)
- [ ] Get consent from all participants
- [ ] Establish recording start/stop signals

## During Session

### Recording Management
- Start Craig before players join voice channel
- Announce "Recording started" to group
- Note important timestamps in chat or separate document
- Avoid stopping/restarting recording unless necessary

### Audio Quality Tips
- Encourage players to use headphones (reduces echo)
- Ask players to mute when not speaking
- Minimize background noise (fans, typing, etc.)
- Speak clearly and at consistent volume
- Use push-to-talk if background noise is unavoidable

### Important Moments to Note
- Combat encounters (start/end times)
- Major story revelations
- Character development moments
- Funny quotes or memorable interactions
- Rules discussions or clarifications

## Post-Session

### Immediate Actions (within 1 hour)
- Stop Craig recording with ":craig:, leave"
- Download audio files from Craig's DM
- Back up files to multiple locations
- Rename files with session information

### File Organization
- Extract all files to session directory
- Keep individual participant tracks
- Rename main file with session number and date
- Create backup copies before processing

## Troubleshooting

### Common Issues
**Craig doesn't respond to commands:**
- Check bot permissions in server settings
- Ensure Craig has "Use Voice Activity" permission
- Try mentioning Craig directly: @Craig

**Poor audio quality:**
- Check Discord voice settings
- Ask players to test microphones
- Consider using different voice channel
- Verify internet connection stability

**Missing audio tracks:**
- Some participants may not have been recorded
- Check if they joined after recording started
- Verify they weren't muted in Discord

### Emergency Backup Methods
- OBS Studio for local recording
- Discord's built-in recording (limited quality)
- Phone recording as last resort
- Ask players to record locally

## Privacy and Consent

### Legal Considerations
- Always get explicit consent before recording
- Inform participants about intended use
- Respect requests to exclude certain content
- Follow local laws regarding recording consent

### Data Management
- Store recordings securely
- Don't share raw audio without permission
- Delete recordings after journal creation (optional)
- Respect participant privacy in final journals
EOF
```

## Step 6: Testing and Verification

```bash
# Create comprehensive test script
cat > scripts/test-recording-setup.sh << 'EOF'
#!/bin/bash

echo "🧪 Recording Setup Test"
echo "======================"
echo

# Test 1: Check Craig bot presence
echo "Test 1: Craig Bot Verification"
echo "------------------------------"
echo "1. Go to your Discord server"
echo "2. Look for Craig in the member list"
echo "3. Craig should show as online (green dot)"
echo
read -p "Is Craig visible and online? (y/n): " CRAIG_ONLINE

if [[ $CRAIG_ONLINE != "y" ]]; then
    echo "❌ Craig bot not properly set up"
    echo "   - Re-invite Craig to your server"
    echo "   - Check bot permissions"
    exit 1
fi

# Test 2: Command response
echo
echo "Test 2: Command Response"
echo "-----------------------"
echo "1. Join any voice channel"
echo "2. Type in chat: :craig:, join"
echo "3. Craig should join the channel"
echo "4. Type: :craig:, leave"
echo "5. Craig should leave and send download link"
echo
read -p "Did Craig respond to commands? (y/n): " CRAIG_RESPONDS

if [[ $CRAIG_RESPONDS != "y" ]]; then
    echo "❌ Craig not responding to commands"
    echo "   - Check channel permissions"
    echo "   - Try mentioning Craig directly: @Craig"
    exit 1
fi

# Test 3: File structure
echo
echo "Test 3: Project Structure"
echo "-------------------------"
if [ -d "sessions" ] && [ -d "scripts" ] && [ -f "config/settings.json" ]; then
    echo "✅ Project structure verified"
else
    echo "❌ Project structure incomplete"
    echo "   - Run 02-Project-Structure.md setup"
    exit 1
fi

# Test 4: FFmpeg availability
echo
echo "Test 4: Audio Processing Tools"
echo "------------------------------"
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg available: $(ffmpeg -version | head -n1)"
else
    echo "❌ FFmpeg not found"
    echo "   - Install FFmpeg for audio processing"
fi

echo
echo "🎉 Recording setup test complete!"
echo "✅ Ready to record D&D sessions with Craig bot"
echo
echo "Next steps:"
echo "1. Run './scripts/start-recording.sh' before your session"
echo "2. Use Craig commands during session"
echo "3. Run './scripts/download-audio.sh' after session"
EOF

chmod +x scripts/test-recording-setup.sh
```

## Troubleshooting Common Issues

### Craig Bot Issues
```bash
cat > docs/craig-troubleshooting.md << 'EOF'
# Craig Bot Troubleshooting

## Bot Not Responding
1. Check bot permissions in server settings
2. Ensure Craig has "Use Voice Activity" permission
3. Try mentioning Craig directly: @Craig, join
4. Restart Discord client
5. Re-invite Craig if necessary

## Poor Recording Quality
1. Check Discord voice settings
2. Disable noise suppression in Discord
3. Ask players to use headphones
4. Test with smaller group first
5. Consider using FLAC format: :craig:, join --format flac

## Download Issues
1. Check Discord DMs for Craig's message
2. Download links expire after 7 days
3. Large files may take time to process
4. Try downloading individual tracks if main file fails

## Missing Participants
1. Ensure all players joined before recording started
2. Check if participants were muted in Discord
3. Verify voice channel permissions for all users
4. Some participants may need to rejoin channel
EOF
```

## Next Steps

With Craig bot set up for recording:

1. ✅ Craig bot invited and configured
2. ✅ Recording workflow scripts created
3. ✅ Audio processing tools ready
4. ✅ Best practices documented
5. ✅ Testing procedures established

Continue to **[04-Transcription-Setup.md](04-Transcription-Setup.md)** to set up Whisper AI for converting your recordings to text.

## Quick Reference Commands

```bash
# Start new recording session
./scripts/start-recording.sh

# Download and organize audio
./scripts/download-audio.sh

# Process audio for transcription
./scripts/process-audio.sh

# Test recording setup
./scripts/test-recording-setup.sh
```
