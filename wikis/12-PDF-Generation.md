# 12 - PDF Generation

Creating high-quality PDFs optimized for both digital viewing and printing.

## Prerequisites Checklist

- [ ] Document layout completed
- [ ] LaTeX/Pandoc working properly
- [ ] Images processed and ready
- [ ] Content finalized

## Step 1: PDF Optimization Script

```bash
cat > scripts/optimize-pdf.py << 'EOF'
#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path

def optimize_pdf(input_pdf, output_pdf, quality="print"):
    """Optimize PDF for different use cases"""
    
    quality_settings = {
        "print": {
            "dpi": 300,
            "quality": 90,
            "description": "High quality for printing"
        },
        "web": {
            "dpi": 150,
            "quality": 75,
            "description": "Optimized for web sharing"
        },
        "email": {
            "dpi": 100,
            "quality": 60,
            "description": "Compressed for email"
        }
    }
    
    settings = quality_settings.get(quality, quality_settings["print"])
    
    try:
        # Use Ghostscript for PDF optimization
        cmd = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/printer' if quality == "print" else '/ebook',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-dColorImageResolution={settings["dpi"]}',
            f'-dGrayImageResolution={settings["dpi"]}',
            f'-dMonoImageResolution={settings["dpi"]}',
            f'-sOutputFile={output_pdf}',
            str(input_pdf)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PDF optimized for {quality}: {output_pdf}")
            
            # Show file size comparison
            original_size = Path(input_pdf).stat().st_size
            optimized_size = Path(output_pdf).stat().st_size
            reduction = (1 - optimized_size/original_size) * 100
            
            print(f"   Original: {original_size:,} bytes")
            print(f"   Optimized: {optimized_size:,} bytes")
            print(f"   Reduction: {reduction:.1f}%")
            
            return True
        else:
            print(f"❌ PDF optimization failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Ghostscript not found. Install with:")
        print("   macOS: brew install ghostscript")
        print("   Linux: sudo apt install ghostscript")
        return False
    except Exception as e:
        print(f"❌ Error optimizing PDF: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python optimize-pdf.py input.pdf output.pdf [quality]")
        print("Quality options: print, web, email")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    quality = sys.argv[3] if len(sys.argv) > 3 else "print"
    
    optimize_pdf(input_pdf, output_pdf, quality)
EOF

chmod +x scripts/optimize-pdf.py
```

## Step 2: Create Multiple PDF Versions

```bash
cat > scripts/generate-pdf-versions.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "📄 Generating PDF Versions for Session ${SESSION_PADDED}"
echo "=============================================="

# Check if base PDF exists
BASE_PDF="${SESSION_DIR}/output/journal.pdf"
if [ ! -f "$BASE_PDF" ]; then
    echo "❌ Base PDF not found. Run layout creation first."
    exit 1
fi

# Create versions directory
VERSIONS_DIR="${SESSION_DIR}/output/versions"
mkdir -p "$VERSIONS_DIR"

# Get session info for naming
SESSION_DATE=$(jq -r '.session_date' "${SESSION_DIR}/session-info.json" 2>/dev/null || echo "$(date +%Y-%m-%d)")
SESSION_TITLE=$(jq -r '.session_title' "${SESSION_DIR}/session-info.json" 2>/dev/null || echo "Session")

# Clean title for filename
CLEAN_TITLE=$(echo "$SESSION_TITLE" | sed 's/[^a-zA-Z0-9]/_/g' | sed 's/__*/_/g' | sed 's/^_\|_$//g')

# Generate different versions
echo "📄 Creating print version (300 DPI)..."
PRINT_PDF="${VERSIONS_DIR}/Vellynne_Notes_Session_${SESSION_PADDED}_${CLEAN_TITLE}_Print.pdf"
python3 scripts/optimize-pdf.py "$BASE_PDF" "$PRINT_PDF" "print"

echo "🌐 Creating web version (150 DPI)..."
WEB_PDF="${VERSIONS_DIR}/Vellynne_Notes_Session_${SESSION_PADDED}_${CLEAN_TITLE}_Web.pdf"
python3 scripts/optimize-pdf.py "$BASE_PDF" "$WEB_PDF" "web"

echo "📧 Creating email version (100 DPI)..."
EMAIL_PDF="${VERSIONS_DIR}/Vellynne_Notes_Session_${SESSION_PADDED}_${CLEAN_TITLE}_Email.pdf"
python3 scripts/optimize-pdf.py "$BASE_PDF" "$EMAIL_PDF" "email"

# Create version manifest
cat > "${VERSIONS_DIR}/versions_manifest.json" << EOL
{
  "session": ${SESSION_NUM},
  "session_date": "${SESSION_DATE}",
  "session_title": "${SESSION_TITLE}",
  "generated_date": "$(date -Iseconds)",
  "versions": {
    "print": {
      "filename": "$(basename "$PRINT_PDF")",
      "description": "High quality for printing (300 DPI)",
      "recommended_use": "Physical printing, archival"
    },
    "web": {
      "filename": "$(basename "$WEB_PDF")",
      "description": "Optimized for web sharing (150 DPI)",
      "recommended_use": "Discord sharing, online viewing"
    },
    "email": {
      "filename": "$(basename "$EMAIL_PDF")",
      "description": "Compressed for email (100 DPI)",
      "recommended_use": "Email attachments, mobile viewing"
    }
  }
}
EOL

echo "✅ PDF versions generated!"
echo "📁 Files created:"
echo "   - Print: $(basename "$PRINT_PDF")"
echo "   - Web: $(basename "$WEB_PDF")"
echo "   - Email: $(basename "$EMAIL_PDF")"
echo "📋 Manifest: versions_manifest.json"
EOF

chmod +x scripts/generate-pdf-versions.sh
```

## Step 3: PDF Quality Control

```bash
cat > scripts/validate-pdf.py << 'EOF'
#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
import json

def validate_pdf(pdf_path):
    """Validate PDF quality and properties"""
    
    if not Path(pdf_path).exists():
        return {"error": "PDF file not found"}
    
    validation_results = {
        "file_size": Path(pdf_path).stat().st_size,
        "issues": [],
        "properties": {}
    }
    
    try:
        # Use pdfinfo to get PDF properties
        result = subprocess.run(['pdfinfo', str(pdf_path)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            # Parse pdfinfo output
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    validation_results["properties"][key.strip()] = value.strip()
        
        # Check for common issues
        file_size = validation_results["file_size"]
        
        if file_size < 100000:  # Less than 100KB
            validation_results["issues"].append("File size suspiciously small")
        elif file_size > 50000000:  # More than 50MB
            validation_results["issues"].append("File size very large")
        
        # Check if PDF has pages
        pages = validation_results["properties"].get("Pages", "0")
        if pages == "0":
            validation_results["issues"].append("PDF has no pages")
        
        # Check PDF version
        pdf_version = validation_results["properties"].get("PDF version", "")
        if not pdf_version:
            validation_results["issues"].append("Cannot determine PDF version")
        
        return validation_results
        
    except FileNotFoundError:
        return {"error": "pdfinfo not found. Install poppler-utils."}
    except Exception as e:
        return {"error": f"Validation error: {e}"}

def validate_session_pdfs(session_dir):
    """Validate all PDFs for a session"""
    
    session_path = Path(session_dir)
    output_dir = session_path / "output"
    
    if not output_dir.exists():
        print("❌ No output directory found")
        return
    
    # Find PDF files
    pdf_files = list(output_dir.glob("**/*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    print(f"🔍 Validating {len(pdf_files)} PDF files...")
    
    all_results = {}
    total_issues = 0
    
    for pdf_file in pdf_files:
        print(f"\n📄 {pdf_file.name}")
        
        results = validate_pdf(pdf_file)
        all_results[pdf_file.name] = results
        
        if "error" in results:
            print(f"   ❌ Error: {results['error']}")
            continue
        
        # Display results
        file_size = results["file_size"]
        print(f"   💾 Size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
        
        properties = results["properties"]
        if "Pages" in properties:
            print(f"   📄 Pages: {properties['Pages']}")
        if "PDF version" in properties:
            print(f"   📋 Version: {properties['PDF version']}")
        
        issues = results["issues"]
        if issues:
            print(f"   ⚠️  Issues: {len(issues)}")
            for issue in issues:
                print(f"      - {issue}")
            total_issues += len(issues)
        else:
            print("   ✅ Quality: Good")
    
    # Save validation report
    report_file = output_dir / "pdf_validation_report.json"
    with open(report_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n📊 Validation Summary")
    print(f"====================")
    print(f"PDFs validated: {len(pdf_files)}")
    print(f"Total issues: {total_issues}")
    print(f"Report saved: {report_file}")
    
    if total_issues == 0:
        print("✅ All PDFs pass validation")
    else:
        print("⚠️  Some PDFs have issues")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        validate_session_pdfs(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == "--single":
        results = validate_pdf(sys.argv[2])
        print(json.dumps(results, indent=2))
    else:
        print("Usage: python validate-pdf.py session_dir")
        print("       python validate-pdf.py --single pdf_file")
        sys.exit(1)
EOF

chmod +x scripts/validate-pdf.py
```

## Step 4: Complete PDF Workflow

```bash
cat > scripts/complete-pdf-workflow.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "📄 Complete PDF Generation Workflow"
echo "===================================="

# Step 1: Ensure layout is complete
if [ ! -f "${SESSION_DIR}/output/journal.pdf" ]; then
    echo "🏗️  Creating initial layout..."
    ./scripts/create-final-layout.sh "$SESSION_NUM"
fi

# Step 2: Generate optimized versions
echo "🔧 Generating optimized PDF versions..."
./scripts/generate-pdf-versions.sh "$SESSION_NUM"

# Step 3: Validate all PDFs
echo "🔍 Validating PDF quality..."
python3 scripts/validate-pdf.py "${SESSION_DIR}"

# Step 4: Create distribution package
echo "📦 Creating distribution package..."
DIST_DIR="${SESSION_DIR}/distribution"
mkdir -p "$DIST_DIR"

# Copy recommended versions
cp "${SESSION_DIR}/output/versions/"*_Web.pdf "$DIST_DIR/" 2>/dev/null || true
cp "${SESSION_DIR}/output/versions/"*_Print.pdf "$DIST_DIR/" 2>/dev/null || true

# Create README for distribution
cat > "${DIST_DIR}/README.txt" << EOL
Vellynne Harpell's Research Notes - Session ${SESSION_NUM}
========================================================

This package contains the journal entry for D&D Session ${SESSION_NUM}.

Files included:
- *_Web.pdf: Optimized for online sharing and Discord (recommended)
- *_Print.pdf: High quality for printing (300 DPI)

The journal is written from the perspective of Vellynne Harpell,
Tenth Black Staff of Blackstaff Academy, documenting her observations
of the party's adventures in Icewind Dale.

Generated on: $(date)
EOL

# Update session status
if [ -f "${SESSION_DIR}/session-info.json" ]; then
    jq '.status = "pdf_complete" | .pdf_generated = now | .ready_for_distribution = true' \
       "${SESSION_DIR}/session-info.json" > "${SESSION_DIR}/session-info.json.tmp" && \
       mv "${SESSION_DIR}/session-info.json.tmp" "${SESSION_DIR}/session-info.json"
fi

echo "✅ PDF workflow complete!"
echo "📁 Distribution package: ${DIST_DIR}"
echo "📄 Files ready for sharing:"
ls -la "$DIST_DIR"/*.pdf 2>/dev/null || echo "   No PDF files found"
EOF

chmod +x scripts/complete-pdf-workflow.sh
```

## Step 5: Batch Processing for Multiple Sessions

```bash
cat > scripts/batch-pdf-generation.sh << 'EOF'
#!/bin/bash

echo "📄 Batch PDF Generation"
echo "======================"

# Find all sessions with completed layouts
SESSIONS=$(find sessions -name "session-*" -type d | sort)

if [ -z "$SESSIONS" ]; then
    echo "❌ No sessions found"
    exit 1
fi

echo "Found sessions:"
for session in $SESSIONS; do
    session_num=$(basename "$session" | sed 's/session-0*//')
    echo "  - Session $session_num: $session"
done

read -p "Generate PDFs for all sessions? (y/n): " CONFIRM

if [[ $CONFIRM != "y" ]]; then
    echo "Cancelled"
    exit 0
fi

# Process each session
for session_dir in $SESSIONS; do
    session_num=$(basename "$session_dir" | sed 's/session-0*//')
    
    echo
    echo "🔄 Processing Session $session_num..."
    
    # Check if content exists
    if [ ! -f "$session_dir/content/journal_final.md" ] && [ ! -f "$session_dir/content/journal_draft.md" ]; then
        echo "   ⚠️  Skipping - no content found"
        continue
    fi
    
    # Run PDF workflow
    ./scripts/complete-pdf-workflow.sh "$session_num"
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Session $session_num complete"
    else
        echo "   ❌ Session $session_num failed"
    fi
done

echo
echo "🏁 Batch processing complete!"
echo "📊 Summary:"
find sessions -name "distribution" -type d | wc -l | xargs echo "   Sessions with PDFs:"
find sessions -path "*/distribution/*.pdf" | wc -l | xargs echo "   Total PDF files:"
EOF

chmod +x scripts/batch-pdf-generation.sh
```

## Troubleshooting

### Common PDF Issues

**Large file sizes:**
```bash
# Use more aggressive compression
python3 scripts/optimize-pdf.py input.pdf output.pdf email
```

**Missing fonts:**
```bash
# Embed fonts in LaTeX
\usepackage{fontspec}
\setmainfont{EB Garamond}[Path=./resources/fonts/]
```

**Image quality problems:**
```bash
# Check image resolution before layout
identify images/final/*.png
```

**Ghostscript errors:**
```bash
# Install Ghostscript
# macOS: brew install ghostscript
# Linux: sudo apt install ghostscript
```

### Quality Standards

- **Print version**: 300 DPI, <20MB file size
- **Web version**: 150 DPI, <10MB file size  
- **Email version**: 100 DPI, <5MB file size
- **Page count**: Typically 3-6 pages per session
- **Font embedding**: All fonts should be embedded

## Next Steps

With PDF generation complete:

1. ✅ High-quality PDFs created for multiple use cases
2. ✅ Optimization and compression configured
3. ✅ Quality validation implemented
4. ✅ Distribution packages ready

Continue to **[13-Distribution.md](13-Distribution.md)** to learn how to share your journals with your D&D group.

## Quick Commands

```bash
# Complete PDF workflow
./scripts/complete-pdf-workflow.sh 01

# Generate all versions
./scripts/generate-pdf-versions.sh 01

# Validate PDFs
python3 scripts/validate-pdf.py sessions/session-01

# Batch process all sessions
./scripts/batch-pdf-generation.sh
```
