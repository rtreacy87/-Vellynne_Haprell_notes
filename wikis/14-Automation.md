# 14 - Automation

Streamlining repetitive tasks and creating efficient workflows for journal production.

## Prerequisites Checklist

- [ ] Complete workflow understanding
- [ ] All individual scripts working
- [ ] Consistent project structure
- [ ] Basic shell scripting knowledge

## Step 1: Master Automation Script

```bash
cat > scripts/master-workflow.sh << 'EOF'
#!/bin/bash

# Vellynne Notes Master Workflow Automation
# Handles complete journal creation from audio to distribution

SESSION_NUM=$1
WORKFLOW_TYPE=${2:-"full"}

if [ -z "$SESSION_NUM" ]; then
    echo "🧙‍♀️ Vellynne's Research Notes - Master Workflow"
    echo "=============================================="
    echo
    read -p "Session number: " SESSION_NUM
    echo
    echo "Workflow options:"
    echo "1. full - Complete workflow (audio → PDF)"
    echo "2. content - Content creation only (transcript → PDF)"
    echo "3. layout - Layout and distribution only"
    echo "4. quick - Fast workflow with minimal processing"
    read -p "Choose workflow (1-4): " WORKFLOW_CHOICE
    
    case $WORKFLOW_CHOICE in
        1) WORKFLOW_TYPE="full" ;;
        2) WORKFLOW_TYPE="content" ;;
        3) WORKFLOW_TYPE="layout" ;;
        4) WORKFLOW_TYPE="quick" ;;
        *) WORKFLOW_TYPE="full" ;;
    esac
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "🚀 Starting $WORKFLOW_TYPE workflow for Session ${SESSION_PADDED}"
echo "=================================================="

# Create session if it doesn't exist
if [ ! -d "$SESSION_DIR" ]; then
    echo "📁 Creating new session..."
    ./scripts/new-session.sh
fi

# Workflow execution
case $WORKFLOW_TYPE in
    "full")
        execute_full_workflow
        ;;
    "content")
        execute_content_workflow
        ;;
    "layout")
        execute_layout_workflow
        ;;
    "quick")
        execute_quick_workflow
        ;;
    *)
        echo "❌ Unknown workflow type: $WORKFLOW_TYPE"
        exit 1
        ;;
esac

echo "🎉 Workflow complete for Session ${SESSION_PADDED}!"

# Function definitions
execute_full_workflow() {
    echo "🎯 Full Workflow: Audio → Content → Images → Layout → Distribution"
    
    # Step 1: Audio processing
    if [ -d "${SESSION_DIR}/audio" ] && [ "$(ls -A ${SESSION_DIR}/audio 2>/dev/null)" ]; then
        echo "🎙️  Step 1: Processing audio..."
        ./scripts/full-transcription.sh "$SESSION_NUM" || handle_error "Audio processing failed"
    else
        echo "⚠️  No audio found, skipping transcription"
    fi
    
    # Step 2: Content creation
    echo "✍️  Step 2: Creating content..."
    ./scripts/template-workflow.sh "$SESSION_NUM" || handle_error "Template creation failed"
    
    # Step 3: Image generation
    echo "🎨 Step 3: Generating images..."
    ./scripts/batch-generate.sh "$SESSION_NUM" || handle_error "Image generation failed"
    ./scripts/process-all-images.sh "$SESSION_NUM" || handle_error "Image processing failed"
    
    # Step 4: Layout and PDF
    echo "📄 Step 4: Creating layout..."
    ./scripts/complete-pdf-workflow.sh "$SESSION_NUM" || handle_error "PDF creation failed"
    
    # Step 5: Distribution
    echo "📤 Step 5: Preparing distribution..."
    ./scripts/auto-distribute.sh "$SESSION_NUM" "both" || handle_error "Distribution prep failed"
}

execute_content_workflow() {
    echo "🎯 Content Workflow: Transcript → Content → Layout"
    
    # Check for transcript
    if [ ! -f "${SESSION_DIR}/transcript/cleaned_transcript.txt" ]; then
        echo "❌ No transcript found. Run full workflow or provide transcript."
        exit 1
    fi
    
    echo "📊 Analyzing content..."
    python3 scripts/extract-content.py "${SESSION_DIR}/transcript/cleaned_transcript.txt" "${SESSION_DIR}/transcript/cleaned_transcript_analysis.json"
    
    echo "📝 Creating template..."
    ./scripts/template-workflow.sh "$SESSION_NUM"
    
    echo "📄 Creating PDF..."
    ./scripts/complete-pdf-workflow.sh "$SESSION_NUM"
}

execute_layout_workflow() {
    echo "🎯 Layout Workflow: Content → PDF → Distribution"
    
    # Check for content
    if [ ! -f "${SESSION_DIR}/content/journal_final.md" ] && [ ! -f "${SESSION_DIR}/content/journal_draft.md" ]; then
        echo "❌ No journal content found. Create content first."
        exit 1
    fi
    
    echo "📄 Creating PDF..."
    ./scripts/complete-pdf-workflow.sh "$SESSION_NUM"
    
    echo "📤 Preparing distribution..."
    ./scripts/auto-distribute.sh "$SESSION_NUM" "both"
}

execute_quick_workflow() {
    echo "🎯 Quick Workflow: Minimal processing for fast turnaround"
    
    # Use existing transcript or create basic one
    if [ ! -f "${SESSION_DIR}/transcript/cleaned_transcript.txt" ]; then
        echo "📝 Creating basic transcript..."
        # Simplified transcription
        ./scripts/transcribe.sh "$SESSION_NUM"
    fi
    
    # Skip image generation for speed
    echo "📝 Creating text-only journal..."
    ./scripts/template-workflow.sh "$SESSION_NUM"
    
    # Create simple PDF
    echo "📄 Creating basic PDF..."
    ./scripts/create-final-layout.sh "$SESSION_NUM"
    
    # Quick distribution
    echo "📤 Preparing for Discord..."
    ./scripts/prepare-discord-share.sh "$SESSION_NUM"
}

handle_error() {
    echo "❌ Error: $1"
    echo "🔧 Check logs and fix issues before continuing"
    exit 1
}
EOF

chmod +x scripts/master-workflow.sh
```

## Step 2: Batch Processing Automation

```bash
cat > scripts/batch-automation.sh << 'EOF'
#!/bin/bash

echo "🔄 Batch Processing Automation"
echo "============================="

# Configuration
BATCH_TYPE=${1:-"pending"}
MAX_PARALLEL=${2:-2}

case $BATCH_TYPE in
    "pending")
        echo "🔍 Processing all pending sessions..."
        SESSIONS=$(find sessions -name "session-*" -type d | while read session; do
            if [ -f "$session/audio/"*.wav ] || [ -f "$session/audio/"*.flac ]; then
                if [ ! -f "$session/output/journal.pdf" ]; then
                    echo "$session"
                fi
            fi
        done)
        ;;
    "incomplete")
        echo "🔍 Processing incomplete sessions..."
        SESSIONS=$(find sessions -name "session-*" -type d | while read session; do
            if [ -f "$session/transcript/cleaned_transcript.txt" ]; then
                if [ ! -f "$session/output/journal.pdf" ]; then
                    echo "$session"
                fi
            fi
        done)
        ;;
    "all")
        echo "🔍 Reprocessing all sessions..."
        SESSIONS=$(find sessions -name "session-*" -type d)
        ;;
    *)
        echo "❌ Unknown batch type: $BATCH_TYPE"
        echo "Options: pending, incomplete, all"
        exit 1
        ;;
esac

if [ -z "$SESSIONS" ]; then
    echo "✅ No sessions to process"
    exit 0
fi

echo "📋 Sessions to process:"
echo "$SESSIONS" | while read session; do
    session_num=$(basename "$session" | sed 's/session-0*//')
    echo "   - Session $session_num"
done

read -p "Continue with batch processing? (y/n): " CONFIRM
if [[ $CONFIRM != "y" ]]; then
    echo "Cancelled"
    exit 0
fi

# Process sessions with parallel limit
echo "$SESSIONS" | xargs -n1 -P$MAX_PARALLEL -I{} bash -c '
    session_num=$(basename "{}" | sed "s/session-0*//")
    echo "🔄 Processing Session $session_num..."
    ./scripts/master-workflow.sh "$session_num" "content" > "logs/batch_session_${session_num}.log" 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Session $session_num complete"
    else
        echo "❌ Session $session_num failed (check logs/batch_session_${session_num}.log)"
    fi
'

echo "🏁 Batch processing complete!"
EOF

chmod +x scripts/batch-automation.sh
```

## Step 3: Scheduled Automation

```bash
cat > scripts/setup-automation.sh << 'EOF'
#!/bin/bash

echo "⏰ Setting up Scheduled Automation"
echo "================================="

# Create automation directory
mkdir -p automation/{cron,logs,config}

# Create monitoring script
cat > automation/monitor-sessions.sh << 'MONITOR_EOF'
#!/bin/bash

# Monitor for new audio files and trigger processing
WATCH_DIR="sessions"
LOG_FILE="automation/logs/monitor.log"

echo "$(date): Starting session monitor..." >> "$LOG_FILE"

# Check for new audio files
find "$WATCH_DIR" -name "*.wav" -o -name "*.flac" | while read audio_file; do
    session_dir=$(dirname "$(dirname "$audio_file")")
    session_num=$(basename "$session_dir" | sed 's/session-0*//')
    
    # Check if already processed
    if [ ! -f "$session_dir/output/journal.pdf" ]; then
        echo "$(date): New audio detected for Session $session_num" >> "$LOG_FILE"
        
        # Trigger processing
        ./scripts/master-workflow.sh "$session_num" "full" >> "$LOG_FILE" 2>&1
        
        if [ $? -eq 0 ]; then
            echo "$(date): Session $session_num processed successfully" >> "$LOG_FILE"
        else
            echo "$(date): Session $session_num processing failed" >> "$LOG_FILE"
        fi
    fi
done
MONITOR_EOF

chmod +x automation/monitor-sessions.sh

# Create daily summary script
cat > automation/daily-summary.sh << 'SUMMARY_EOF'
#!/bin/bash

# Generate daily summary of journal status
SUMMARY_FILE="automation/logs/daily-summary-$(date +%Y%m%d).log"

echo "📊 Daily Summary - $(date)" > "$SUMMARY_FILE"
echo "=========================" >> "$SUMMARY_FILE"

# Count sessions by status
TOTAL_SESSIONS=$(find sessions -name "session-*" -type d | wc -l)
COMPLETED_SESSIONS=$(find sessions -name "journal.pdf" | wc -l)
PENDING_SESSIONS=$((TOTAL_SESSIONS - COMPLETED_SESSIONS))

echo "Total Sessions: $TOTAL_SESSIONS" >> "$SUMMARY_FILE"
echo "Completed: $COMPLETED_SESSIONS" >> "$SUMMARY_FILE"
echo "Pending: $PENDING_SESSIONS" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

# List pending sessions
if [ $PENDING_SESSIONS -gt 0 ]; then
    echo "Pending Sessions:" >> "$SUMMARY_FILE"
    find sessions -name "session-*" -type d | while read session; do
        if [ ! -f "$session/output/journal.pdf" ]; then
            session_num=$(basename "$session" | sed 's/session-0*//')
            echo "  - Session $session_num" >> "$SUMMARY_FILE"
        fi
    done
fi

# Recent activity
echo "" >> "$SUMMARY_FILE"
echo "Recent PDFs (last 7 days):" >> "$SUMMARY_FILE"
find sessions -name "journal.pdf" -mtime -7 -exec dirname {} \; | while read session; do
    session_num=$(basename "$session" | sed 's/session-0*//')
    echo "  - Session $session_num" >> "$SUMMARY_FILE"
done

echo "Summary saved to: $SUMMARY_FILE"
SUMMARY_EOF

chmod +x automation/daily-summary.sh

# Create cron job templates
cat > automation/cron/crontab-template << 'CRON_EOF'
# Vellynne Notes Automation Cron Jobs
# Edit times as needed for your schedule

# Monitor for new sessions every hour
0 * * * * cd /path/to/vellynne-notes && ./automation/monitor-sessions.sh

# Daily summary at 9 AM
0 9 * * * cd /path/to/vellynne-notes && ./automation/daily-summary.sh

# Weekly batch processing on Sundays at 2 AM
0 2 * * 0 cd /path/to/vellynne-notes && ./scripts/batch-automation.sh pending

# Monthly archive creation on 1st at 3 AM
0 3 1 * * cd /path/to/vellynne-notes && ./scripts/create-campaign-archive.sh
CRON_EOF

echo "📋 Automation setup complete!"
echo "📁 Files created in automation/ directory"
echo "⏰ To enable cron jobs:"
echo "   1. Edit automation/cron/crontab-template"
echo "   2. Update paths to your project directory"
echo "   3. Install with: crontab automation/cron/crontab-template"
EOF

chmod +x scripts/setup-automation.sh
```

## Step 4: Configuration Management

```bash
cat > scripts/manage-config.py << 'EOF'
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def load_config():
    """Load automation configuration"""
    config_file = Path("automation/config/automation.json")
    
    if config_file.exists():
        with open(config_file) as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "automation": {
                "enabled": False,
                "auto_transcribe": True,
                "auto_generate_images": True,
                "auto_create_pdf": True,
                "auto_distribute": False
            },
            "quality": {
                "transcription_model": "medium",
                "image_count_max": 4,
                "pdf_quality": "web"
            },
            "distribution": {
                "default_method": "discord",
                "auto_share": False,
                "notification_webhook": ""
            },
            "monitoring": {
                "check_interval_minutes": 60,
                "log_retention_days": 30,
                "alert_on_failure": True
            }
        }

def save_config(config):
    """Save automation configuration"""
    config_file = Path("automation/config/automation.json")
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def configure_automation():
    """Interactive configuration setup"""
    config = load_config()
    
    print("🔧 Automation Configuration")
    print("===========================")
    
    # Automation settings
    print("\n📋 Automation Settings:")
    config["automation"]["enabled"] = input("Enable automation? (y/n): ").lower() == 'y'
    config["automation"]["auto_transcribe"] = input("Auto-transcribe audio? (y/n): ").lower() == 'y'
    config["automation"]["auto_generate_images"] = input("Auto-generate images? (y/n): ").lower() == 'y'
    config["automation"]["auto_create_pdf"] = input("Auto-create PDFs? (y/n): ").lower() == 'y'
    config["automation"]["auto_distribute"] = input("Auto-distribute? (y/n): ").lower() == 'y'
    
    # Quality settings
    print("\n🎯 Quality Settings:")
    models = ["tiny", "base", "small", "medium", "large"]
    print(f"Transcription models: {', '.join(models)}")
    model = input(f"Transcription model [{config['quality']['transcription_model']}]: ").strip()
    if model in models:
        config["quality"]["transcription_model"] = model
    
    max_images = input(f"Max images per session [{config['quality']['image_count_max']}]: ").strip()
    if max_images.isdigit():
        config["quality"]["image_count_max"] = int(max_images)
    
    # Distribution settings
    if config["automation"]["auto_distribute"]:
        print("\n📤 Distribution Settings:")
        methods = ["discord", "email", "both"]
        print(f"Distribution methods: {', '.join(methods)}")
        method = input(f"Default method [{config['distribution']['default_method']}]: ").strip()
        if method in methods:
            config["distribution"]["default_method"] = method
    
    save_config(config)
    print("\n✅ Configuration saved!")
    return config

def show_config():
    """Display current configuration"""
    config = load_config()
    print("📋 Current Automation Configuration:")
    print("===================================")
    print(json.dumps(config, indent=2))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "show":
        show_config()
    else:
        configure_automation()
EOF

chmod +x scripts/manage-config.py
```

## Step 5: Error Handling and Recovery

```bash
cat > scripts/error-recovery.sh << 'EOF'
#!/bin/bash

echo "🔧 Error Recovery and Diagnostics"
echo "================================="

SESSION_NUM=$1
RECOVERY_TYPE=${2:-"auto"}

if [ -z "$SESSION_NUM" ]; then
    echo "Usage: ./error-recovery.sh SESSION_NUM [recovery_type]"
    echo "Recovery types: auto, manual, reset"
    exit 1
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

if [ ! -d "$SESSION_DIR" ]; then
    echo "❌ Session directory not found: $SESSION_DIR"
    exit 1
fi

echo "🔍 Diagnosing Session ${SESSION_PADDED}..."

# Check session status
check_session_status() {
    echo "📊 Session Status Check:"
    
    # Audio files
    if [ -d "$SESSION_DIR/audio" ] && [ "$(ls -A $SESSION_DIR/audio 2>/dev/null)" ]; then
        echo "   ✅ Audio files present"
        AUDIO_OK=true
    else
        echo "   ❌ No audio files found"
        AUDIO_OK=false
    fi
    
    # Transcript
    if [ -f "$SESSION_DIR/transcript/cleaned_transcript.txt" ]; then
        echo "   ✅ Transcript available"
        TRANSCRIPT_OK=true
    else
        echo "   ❌ No transcript found"
        TRANSCRIPT_OK=false
    fi
    
    # Content
    if [ -f "$SESSION_DIR/content/journal_final.md" ] || [ -f "$SESSION_DIR/content/journal_draft.md" ]; then
        echo "   ✅ Journal content exists"
        CONTENT_OK=true
    else
        echo "   ❌ No journal content found"
        CONTENT_OK=false
    fi
    
    # Images
    if [ -d "$SESSION_DIR/images/final" ] && [ "$(ls -A $SESSION_DIR/images/final 2>/dev/null)" ]; then
        echo "   ✅ Processed images available"
        IMAGES_OK=true
    else
        echo "   ❌ No processed images found"
        IMAGES_OK=false
    fi
    
    # PDF
    if [ -f "$SESSION_DIR/output/journal.pdf" ]; then
        echo "   ✅ PDF generated"
        PDF_OK=true
    else
        echo "   ❌ No PDF found"
        PDF_OK=false
    fi
}

# Recovery strategies
auto_recovery() {
    echo "🔄 Attempting automatic recovery..."
    
    if [ "$AUDIO_OK" = true ] && [ "$TRANSCRIPT_OK" = false ]; then
        echo "🎙️  Regenerating transcript..."
        ./scripts/full-transcription.sh "$SESSION_NUM"
    fi
    
    if [ "$TRANSCRIPT_OK" = true ] && [ "$CONTENT_OK" = false ]; then
        echo "📝 Regenerating content..."
        ./scripts/template-workflow.sh "$SESSION_NUM"
    fi
    
    if [ "$CONTENT_OK" = true ] && [ "$IMAGES_OK" = false ]; then
        echo "🎨 Regenerating images..."
        ./scripts/batch-generate.sh "$SESSION_NUM"
        ./scripts/process-all-images.sh "$SESSION_NUM"
    fi
    
    if [ "$CONTENT_OK" = true ] && [ "$PDF_OK" = false ]; then
        echo "📄 Regenerating PDF..."
        ./scripts/complete-pdf-workflow.sh "$SESSION_NUM"
    fi
}

manual_recovery() {
    echo "🛠️  Manual recovery mode..."
    echo "Choose recovery action:"
    echo "1. Regenerate transcript"
    echo "2. Regenerate content"
    echo "3. Regenerate images"
    echo "4. Regenerate PDF"
    echo "5. Full regeneration"
    
    read -p "Choice (1-5): " CHOICE
    
    case $CHOICE in
        1) ./scripts/full-transcription.sh "$SESSION_NUM" ;;
        2) ./scripts/template-workflow.sh "$SESSION_NUM" ;;
        3) ./scripts/batch-generate.sh "$SESSION_NUM"; ./scripts/process-all-images.sh "$SESSION_NUM" ;;
        4) ./scripts/complete-pdf-workflow.sh "$SESSION_NUM" ;;
        5) ./scripts/master-workflow.sh "$SESSION_NUM" "full" ;;
        *) echo "Invalid choice" ;;
    esac
}

reset_session() {
    echo "⚠️  Resetting session (will delete generated files)..."
    read -p "Are you sure? This will delete all generated content (y/n): " CONFIRM
    
    if [[ $CONFIRM == "y" ]]; then
        # Keep audio and session info, delete everything else
        find "$SESSION_DIR" -type f ! -path "*/audio/*" ! -name "session-info.json" -delete
        find "$SESSION_DIR" -type d -empty -delete
        echo "✅ Session reset complete"
    else
        echo "Reset cancelled"
    fi
}

# Main execution
check_session_status

case $RECOVERY_TYPE in
    "auto")
        auto_recovery
        ;;
    "manual")
        manual_recovery
        ;;
    "reset")
        reset_session
        ;;
    *)
        echo "❌ Unknown recovery type: $RECOVERY_TYPE"
        exit 1
        ;;
esac

echo "🔧 Recovery complete for Session ${SESSION_PADDED}"
EOF

chmod +x scripts/error-recovery.sh
```

## Usage Examples

### Complete Automation
```bash
# Set up automation
./scripts/setup-automation.sh

# Configure settings
python3 scripts/manage-config.py

# Process single session automatically
./scripts/master-workflow.sh 01 full

# Batch process all pending
./scripts/batch-automation.sh pending
```

### Error Recovery
```bash
# Auto-recover failed session
./scripts/error-recovery.sh 01 auto

# Manual recovery with choices
./scripts/error-recovery.sh 01 manual

# Reset and start over
./scripts/error-recovery.sh 01 reset
```

## Troubleshooting

### Common Automation Issues
- **Permissions**: Ensure scripts are executable (`chmod +x`)
- **Dependencies**: Verify all tools installed and accessible
- **Paths**: Check file paths in cron jobs and scripts
- **Resources**: Monitor CPU/memory usage during batch processing

### Performance Optimization
- **Parallel processing**: Limit concurrent sessions to avoid overload
- **Resource monitoring**: Use `htop` or `top` to monitor system usage
- **Disk space**: Regularly clean up intermediate files
- **Network**: Consider API rate limits for image generation

## Next Steps

With automation complete:

1. ✅ Master workflow automation implemented
2. ✅ Batch processing capabilities added
3. ✅ Scheduled automation configured
4. ✅ Error recovery and diagnostics ready

Continue to **[15-Quality-Control.md](15-Quality-Control.md)** for maintaining consistency and quality across all journal entries.

## Quick Commands

```bash
# Full automation for session
./scripts/master-workflow.sh 01 full

# Batch process pending sessions
./scripts/batch-automation.sh pending

# Set up scheduled automation
./scripts/setup-automation.sh

# Recover failed session
./scripts/error-recovery.sh 01 auto
```
