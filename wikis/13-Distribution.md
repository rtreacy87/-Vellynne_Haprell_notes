# 13 - Distribution

Sharing your completed journal entries with your D&D group and managing the collection.

## Prerequisites Checklist

- [ ] PDF generation completed
- [ ] Distribution packages ready
- [ ] Group communication channels identified
- [ ] File sharing method chosen

## Step 1: Distribution Methods

### Discord Sharing
```bash
cat > scripts/prepare-discord-share.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "💬 Preparing Discord Share for Session ${SESSION_PADDED}"
echo "=============================================="

# Find the web-optimized PDF
WEB_PDF=$(find "${SESSION_DIR}/output/versions" -name "*_Web.pdf" | head -n1)

if [ -z "$WEB_PDF" ]; then
    echo "❌ Web-optimized PDF not found. Generate PDFs first."
    exit 1
fi

# Check file size (Discord limit is 8MB for free users)
FILE_SIZE=$(stat -f%z "$WEB_PDF" 2>/dev/null || stat -c%s "$WEB_PDF" 2>/dev/null)
FILE_SIZE_MB=$((FILE_SIZE / 1024 / 1024))

echo "📄 File: $(basename "$WEB_PDF")"
echo "💾 Size: ${FILE_SIZE_MB}MB"

if [ $FILE_SIZE_MB -gt 8 ]; then
    echo "⚠️  File too large for Discord (>8MB)"
    echo "   Consider using email version or external hosting"
else
    echo "✅ File size OK for Discord"
fi

# Create Discord message template
SESSION_DATE=$(jq -r '.session_date' "${SESSION_DIR}/session-info.json" 2>/dev/null || echo "Recent")
SESSION_TITLE=$(jq -r '.session_title' "${SESSION_DIR}/session-info.json" 2>/dev/null || echo "Adventure")

cat > "${SESSION_DIR}/discord_message.txt" << EOL
📚 **Vellynne Harpell's Research Notes - Session ${SESSION_NUM}**

*${SESSION_DATE} - ${SESSION_TITLE}*

Greetings, fellow adventurers! I've completed my scholarly analysis of our recent expedition. This journal entry documents our encounters, magical phenomena observed, and tactical developments from my perspective as your resident necromancer and researcher.

**Highlights from this session:**
• Detailed creature studies and behavioral analysis
• Magical phenomena documentation
• Party tactical development observations
• Research implications for our ongoing mission

The attached PDF contains the complete research notes in medieval manuscript style, complete with illustrations and scholarly annotations.

*May your blades stay sharp and your spells true,*
*Vellynne Harpell, Tenth Black Staff of Blackstaff Academy*

---
*Generated on $(date +"%B %d, %Y")*
EOL

echo "📝 Discord message template created: discord_message.txt"
echo
echo "📋 Next steps:"
echo "1. Copy the message from discord_message.txt"
echo "2. Upload $(basename "$WEB_PDF") to Discord"
echo "3. Post in your campaign channel"
EOF

chmod +x scripts/prepare-discord-share.sh
```

### Email Distribution
```bash
cat > scripts/prepare-email-share.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "📧 Preparing Email Distribution for Session ${SESSION_PADDED}"
echo "================================================="

# Find the email-optimized PDF
EMAIL_PDF=$(find "${SESSION_DIR}/output/versions" -name "*_Email.pdf" | head -n1)

if [ -z "$EMAIL_PDF" ]; then
    echo "❌ Email-optimized PDF not found. Generate PDFs first."
    exit 1
fi

# Check file size
FILE_SIZE=$(stat -f%z "$EMAIL_PDF" 2>/dev/null || stat -c%s "$EMAIL_PDF" 2>/dev/null)
FILE_SIZE_MB=$((FILE_SIZE / 1024 / 1024))

echo "📄 File: $(basename "$EMAIL_PDF")"
echo "💾 Size: ${FILE_SIZE_MB}MB"

# Create email template
SESSION_DATE=$(jq -r '.session_date' "${SESSION_DIR}/session-info.json" 2>/dev/null || echo "Recent")
SESSION_TITLE=$(jq -r '.session_title' "${SESSION_DIR}/session-info.json" 2>/dev/null || echo "Adventure")

cat > "${SESSION_DIR}/email_template.txt" << EOL
Subject: Vellynne's Research Notes - Session ${SESSION_NUM}: ${SESSION_TITLE}

Dear Fellow Adventurers,

I hope this message finds you well and recovering from our recent expedition to the frozen wastes of Icewind Dale.

I have completed my scholarly analysis of Session ${SESSION_NUM} (${SESSION_DATE}) and am pleased to share my research notes with you. As always, I've documented our encounters from an academic perspective, focusing on the magical phenomena we witnessed, the creatures we studied, and the tactical developments I observed in our group dynamics.

**This session's research highlights:**
• Comprehensive creature behavioral analysis
• Detailed magical phenomena documentation  
• Party coordination and individual growth observations
• Strategic implications for our ongoing mission

The attached PDF contains the complete journal entry in medieval manuscript style, featuring scholarly illustrations and annotations that I believe you'll find both informative and entertaining.

I continue to be impressed by our group's development and look forward to our next expedition. Please don't hesitate to reach out if you have any questions about my observations or if you'd like to discuss any of the magical theories presented.

Stay warm and stay vigilant,

Vellynne Harpell
Tenth Black Staff of Blackstaff Academy
Research Specialist in Necromantic Studies

---
Attachment: $(basename "$EMAIL_PDF") (${FILE_SIZE_MB}MB)
Generated: $(date +"%B %d, %Y")
EOL

echo "📝 Email template created: email_template.txt"
echo "📎 Attachment ready: $(basename "$EMAIL_PDF")"
EOF

chmod +x scripts/prepare-email-share.sh
```

## Step 2: Cloud Storage Integration

```bash
cat > scripts/upload-to-cloud.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
CLOUD_SERVICE=$2

if [ -z "$SESSION_NUM" ] || [ -z "$CLOUD_SERVICE" ]; then
    echo "Usage: ./upload-to-cloud.sh SESSION_NUM CLOUD_SERVICE"
    echo "Cloud services: gdrive, dropbox, onedrive"
    exit 1
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "☁️  Uploading Session ${SESSION_PADDED} to ${CLOUD_SERVICE}"
echo "=============================================="

# Find distribution files
DIST_DIR="${SESSION_DIR}/distribution"
if [ ! -d "$DIST_DIR" ]; then
    echo "❌ Distribution directory not found. Generate PDFs first."
    exit 1
fi

case $CLOUD_SERVICE in
    "gdrive")
        echo "📤 Uploading to Google Drive..."
        echo "💡 Install gdrive CLI: https://github.com/prasmussen/gdrive"
        echo "📋 Commands to run:"
        for file in "$DIST_DIR"/*.pdf; do
            if [ -f "$file" ]; then
                echo "   gdrive upload \"$file\""
            fi
        done
        ;;
    "dropbox")
        echo "📤 Uploading to Dropbox..."
        echo "💡 Install Dropbox CLI or use web interface"
        echo "📁 Upload these files to your Dropbox:"
        ls -la "$DIST_DIR"/*.pdf
        ;;
    "onedrive")
        echo "📤 Uploading to OneDrive..."
        echo "💡 Use OneDrive web interface or sync folder"
        echo "📁 Copy these files to your OneDrive folder:"
        ls -la "$DIST_DIR"/*.pdf
        ;;
    *)
        echo "❌ Unsupported cloud service: $CLOUD_SERVICE"
        echo "Supported: gdrive, dropbox, onedrive"
        exit 1
        ;;
esac

# Create shareable links template
cat > "${SESSION_DIR}/sharing_links.txt" << EOL
Vellynne's Research Notes - Session ${SESSION_NUM}
===============================================

Cloud Storage Links:
• Web Version (recommended): [Add ${CLOUD_SERVICE} link here]
• Print Version (high quality): [Add ${CLOUD_SERVICE} link here]

Direct Download Instructions:
1. Click the link above
2. Download the PDF file
3. Open with your preferred PDF viewer

File Descriptions:
• Web Version: Optimized for online viewing and sharing
• Print Version: High resolution for physical printing

Generated: $(date +"%B %d, %Y")
EOL

echo "📝 Sharing links template: sharing_links.txt"
echo "✏️  Update with actual cloud storage URLs"
EOF

chmod +x scripts/upload-to-cloud.sh
```

## Step 3: Campaign Archive Management

```bash
cat > scripts/create-campaign-archive.sh << 'EOF'
#!/bin/bash

echo "📚 Creating Campaign Archive"
echo "============================"

# Create archive directory
ARCHIVE_DIR="campaign_archive"
mkdir -p "$ARCHIVE_DIR"/{sessions,resources,master_files}

echo "📁 Organizing campaign files..."

# Copy all completed sessions
for session_dir in sessions/session-*; do
    if [ -d "$session_dir" ]; then
        session_num=$(basename "$session_dir" | sed 's/session-0*//')
        
        # Check if session has final PDFs
        if [ -d "$session_dir/distribution" ]; then
            echo "   📄 Adding Session $session_num"
            
            # Copy distribution files
            cp -r "$session_dir/distribution" "$ARCHIVE_DIR/sessions/session_$session_num"
            
            # Copy session info
            if [ -f "$session_dir/session-info.json" ]; then
                cp "$session_dir/session-info.json" "$ARCHIVE_DIR/sessions/session_$session_num/"
            fi
        fi
    fi
done

# Copy resources
echo "📦 Copying resources..."
cp -r templates "$ARCHIVE_DIR/resources/" 2>/dev/null || true
cp -r resources "$ARCHIVE_DIR/resources/" 2>/dev/null || true

# Create master index
cat > "$ARCHIVE_DIR/README.md" << 'EOL'
# Vellynne Harpell's Research Notes - Campaign Archive

This archive contains the complete collection of research notes from our Icewind Dale campaign, written from the perspective of Vellynne Harpell, Tenth Black Staff of Blackstaff Academy.

## Sessions Included

EOL

# Add session list to README
for session_dir in "$ARCHIVE_DIR/sessions"/*; do
    if [ -d "$session_dir" ]; then
        session_name=$(basename "$session_dir")
        session_num=$(echo "$session_name" | sed 's/session_//')
        
        # Get session info if available
        if [ -f "$session_dir/session-info.json" ]; then
            session_date=$(jq -r '.session_date' "$session_dir/session-info.json" 2>/dev/null || echo "Unknown")
            session_title=$(jq -r '.session_title' "$session_dir/session-info.json" 2>/dev/null || echo "Unknown")
            echo "- **Session $session_num** ($session_date): $session_title" >> "$ARCHIVE_DIR/README.md"
        else
            echo "- **Session $session_num**: Available" >> "$ARCHIVE_DIR/README.md"
        fi
    fi
done

cat >> "$ARCHIVE_DIR/README.md" << 'EOL'

## File Organization

- `sessions/`: Individual session journals
  - `session_XX/`: Each session's files
    - `*_Web.pdf`: Optimized for online viewing
    - `*_Print.pdf`: High quality for printing
    - `session-info.json`: Session metadata
- `resources/`: Templates and assets used
- `master_files/`: Source templates and configurations

## Usage

Each session folder contains PDF versions optimized for different uses:
- **Web version**: Best for Discord sharing and online viewing
- **Print version**: High resolution for physical printing

## About

These journals document our D&D campaign from Vellynne Harpell's scholarly perspective, combining session recaps with in-character academic analysis, medieval manuscript styling, and AI-generated illustrations.

Generated: $(date +"%B %d, %Y")
EOL

# Create campaign statistics
TOTAL_SESSIONS=$(find "$ARCHIVE_DIR/sessions" -name "session_*" -type d | wc -l)
TOTAL_PDFS=$(find "$ARCHIVE_DIR/sessions" -name "*.pdf" | wc -l)
ARCHIVE_SIZE=$(du -sh "$ARCHIVE_DIR" | cut -f1)

cat > "$ARCHIVE_DIR/campaign_stats.json" << EOL
{
  "campaign_name": "Icewind Dale - Vellynne's Research Notes",
  "total_sessions": $TOTAL_SESSIONS,
  "total_pdfs": $TOTAL_PDFS,
  "archive_size": "$ARCHIVE_SIZE",
  "created_date": "$(date -Iseconds)",
  "character_perspective": "Vellynne Harpell",
  "style": "Medieval manuscript with scholarly analysis"
}
EOL

echo "✅ Campaign archive created!"
echo "📁 Location: $ARCHIVE_DIR"
echo "📊 Statistics:"
echo "   Sessions: $TOTAL_SESSIONS"
echo "   PDF files: $TOTAL_PDFS"
echo "   Total size: $ARCHIVE_SIZE"
EOF

chmod +x scripts/create-campaign-archive.sh
```

## Step 4: Distribution Automation

```bash
cat > scripts/auto-distribute.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
DISTRIBUTION_METHOD=$2

if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

if [ -z "$DISTRIBUTION_METHOD" ]; then
    echo "Select distribution method:"
    echo "1. Discord only"
    echo "2. Email only"
    echo "3. Both Discord and Email"
    echo "4. Cloud storage"
    read -p "Choice (1-4): " CHOICE
    
    case $CHOICE in
        1) DISTRIBUTION_METHOD="discord" ;;
        2) DISTRIBUTION_METHOD="email" ;;
        3) DISTRIBUTION_METHOD="both" ;;
        4) DISTRIBUTION_METHOD="cloud" ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)

echo "📤 Auto-Distribution for Session ${SESSION_PADDED}"
echo "========================================"

case $DISTRIBUTION_METHOD in
    "discord")
        ./scripts/prepare-discord-share.sh "$SESSION_NUM"
        echo "💬 Discord package ready!"
        ;;
    "email")
        ./scripts/prepare-email-share.sh "$SESSION_NUM"
        echo "📧 Email package ready!"
        ;;
    "both")
        ./scripts/prepare-discord-share.sh "$SESSION_NUM"
        ./scripts/prepare-email-share.sh "$SESSION_NUM"
        echo "💬📧 Both packages ready!"
        ;;
    "cloud")
        read -p "Cloud service (gdrive/dropbox/onedrive): " CLOUD_SERVICE
        ./scripts/upload-to-cloud.sh "$SESSION_NUM" "$CLOUD_SERVICE"
        echo "☁️  Cloud upload instructions ready!"
        ;;
    *)
        echo "❌ Unknown distribution method: $DISTRIBUTION_METHOD"
        exit 1
        ;;
esac

echo
echo "📋 Distribution Summary:"
echo "   Session: $SESSION_NUM"
echo "   Method: $DISTRIBUTION_METHOD"
echo "   Files ready in: sessions/session-${SESSION_PADDED}/"
EOF

chmod +x scripts/auto-distribute.sh
```

## Step 5: Feedback and Iteration

```bash
cat > scripts/collect-feedback.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "📝 Collecting Feedback for Session ${SESSION_PADDED}"
echo "=========================================="

# Create feedback template
cat > "${SESSION_DIR}/feedback_form.md" << 'EOL'
# Feedback Form - Vellynne's Research Notes

## Session Information
- Session Number: 
- Date Reviewed: 
- Reviewer Name: 

## Content Accuracy (1-5 scale)
- [ ] Session events accurately captured
- [ ] Character actions correctly described  
- [ ] Combat encounters detailed appropriately
- [ ] Story beats included

**Comments:**

## Vellynne's Voice (1-5 scale)
- [ ] Academic tone consistent
- [ ] Character personality authentic
- [ ] Scholarly analysis appropriate
- [ ] Protective feelings toward party evident

**Comments:**

## Visual Elements (1-5 scale)
- [ ] Illustrations match content
- [ ] Medieval manuscript style effective
- [ ] Image quality satisfactory
- [ ] Layout and formatting appealing

**Comments:**

## Overall Experience (1-5 scale)
- [ ] Enjoyable to read
- [ ] Adds value to campaign
- [ ] Would recommend to others
- [ ] Enhances session memories

**Comments:**

## Suggestions for Improvement
- Content:
- Style:
- Technical:
- Other:

## Favorite Elements
- Best illustration:
- Favorite Vellynne observation:
- Most accurate moment:
- Overall highlight:

## Additional Comments

EOL

echo "📝 Feedback form created: feedback_form.md"
echo "📤 Share this form with your D&D group"
echo "📊 Use responses to improve future journals"

# Create feedback tracking
cat > "${SESSION_DIR}/feedback_tracker.json" << EOL
{
  "session": $SESSION_NUM,
  "feedback_requested": "$(date -Iseconds)",
  "responses_received": 0,
  "average_ratings": {
    "content_accuracy": null,
    "voice_authenticity": null,
    "visual_elements": null,
    "overall_experience": null
  },
  "common_suggestions": [],
  "improvements_implemented": []
}
EOL

echo "📋 Feedback tracker initialized"
EOF

chmod +x scripts/collect-feedback.sh
```

## Distribution Best Practices

### File Size Guidelines
- **Discord**: <8MB (use Web version)
- **Email**: <5MB (use Email version)  
- **Cloud storage**: Any size (use Print version for archival)

### Timing Recommendations
- **Immediate**: Share within 24-48 hours of session
- **Weekly**: For regular campaign rhythm
- **Batch**: For catch-up or archive sharing

### Group Communication
- **Announce**: Let group know journals are coming
- **Context**: Explain Vellynne's perspective
- **Feedback**: Ask for input and suggestions

## Troubleshooting

### File Size Issues
```bash
# Check file sizes
find sessions -name "*.pdf" -exec ls -lh {} \;

# Re-optimize if needed
python3 scripts/optimize-pdf.py input.pdf output.pdf email
```

### Upload Problems
- **Discord**: Use web version, check 8MB limit
- **Email**: Use email version, check provider limits
- **Cloud**: Verify authentication and permissions

## Next Steps

With distribution complete:

1. ✅ Multiple sharing methods configured
2. ✅ Cloud storage integration ready
3. ✅ Campaign archive system established
4. ✅ Feedback collection implemented

Continue to **[14-Automation.md](14-Automation.md)** to streamline repetitive tasks and **[15-Quality-Control.md](15-Quality-Control.md)** for maintaining consistency.

## Quick Commands

```bash
# Auto-distribute session
./scripts/auto-distribute.sh 01

# Create campaign archive
./scripts/create-campaign-archive.sh

# Collect feedback
./scripts/collect-feedback.sh 01
```
