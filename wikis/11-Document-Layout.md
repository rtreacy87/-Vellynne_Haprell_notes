# 11 - Document Layout

Assembling journal pages with text and images using Pandoc and LaTeX for professional results.

## Prerequisites Checklist

- [ ] Completed journal text content
- [ ] Processed images ready
- [ ] Pandoc and LaTeX installed
- [ ] Medieval fonts available

## Step 1: Install Layout Tools

```bash
# Install LaTeX distribution
# macOS:
brew install --cask mactex

# Linux:
sudo apt install texlive-full

# Windows:
# Download and install MiKTeX from miktex.org

# Verify installation
pandoc --version
pdflatex --version
```

## Step 2: Create LaTeX Template

```bash
cat > templates/journal_layout.tex << 'EOF'
\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{fontspec}
\usepackage{multicol}
\usepackage{wrapfig}
\usepackage{background}

% Set medieval fonts
\setmainfont{EB Garamond}[
    Path = resources/fonts/,
    Extension = .ttf,
    UprightFont = *-Regular,
    BoldFont = *-Bold,
    ItalicFont = *-Italic
]

\newfontfamily\headingfont{Cinzel}[
    Path = resources/fonts/,
    Extension = .ttf,
    UprightFont = *-Regular,
    BoldFont = *-Bold
]

% Colors
\definecolor{parchment}{RGB}{244,228,188}
\definecolor{inkbrown}{RGB}{93,78,55}
\definecolor{sealred}{RGB}{139,69,19}

% Page background
\backgroundsetup{
    scale=1,
    color=black,
    opacity=0.1,
    angle=0,
    contents={%
        \includegraphics[width=\paperwidth,height=\paperheight]{resources/textures/parchment.png}
    }
}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{inkbrown}{Research Notes of Vellynne Harpell}}
\fancyhead[R]{\small\textcolor{inkbrown}{Blackstaff Academy}}
\fancyfoot[C]{\small\textcolor{inkbrown}{\thepage}}

% Section formatting
\titleformat{\section}
    {\headingfont\Large\color{sealred}}
    {}
    {0em}
    {}
    [\color{sealred}\titlerule]

\titleformat{\subsection}
    {\headingfont\large\color{inkbrown}}
    {}
    {0em}
    {}

% Custom commands
\newcommand{\journaltitle}[3]{
    \begin{center}
        {\headingfont\Huge\color{sealred} Research Notes of Vellynne Harpell}\\[0.5em]
        {\headingfont\Large\color{inkbrown} Tenth Black Staff of Blackstaff Academy}\\[1em]
        {\large\color{inkbrown} #1 - Session #2: #3}\\[2em]
        \textcolor{sealred}{\rule{0.8\textwidth}{2pt}}
    \end{center}
}

\newcommand{\illustration}[3]{
    \begin{figure}[h]
        \centering
        \includegraphics[width=#2\textwidth]{#1}
        \caption{\textit{#3}}
    \end{figure}
}

\newcommand{\marginnote}[1]{
    \marginpar{\small\textcolor{inkbrown}{\textit{#1}}}
}

% Document settings
\setlength{\parindent}{1em}
\setlength{\parskip}{0.5em}
\linespread{1.2}

\begin{document}

$body$

\end{document}
EOF
```

## Step 3: Create Pandoc Conversion Script

```bash
cat > scripts/create-layout.py << 'EOF'
#!/usr/bin/env python3
import sys
import json
import re
from pathlib import Path
import subprocess

def prepare_markdown_for_latex(content, images_dir):
    """Convert markdown content to LaTeX-friendly format"""
    
    # Replace image references with LaTeX commands
    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        
        # Find actual image file
        image_file = None
        for ext in ['.png', '.jpg', '.jpeg']:
            candidate = images_dir / f"{image_path}{ext}"
            if candidate.exists():
                image_file = candidate
                break
        
        if not image_file:
            return f"[Image not found: {image_path}]"
        
        # Determine image width based on type
        if "creature" in image_path.lower():
            width = "0.7"
        elif "diagram" in image_path.lower():
            width = "0.6"
        else:
            width = "0.8"
        
        return f"\\illustration{{{image_file}}}{{{width}}}{{{alt_text}}}"
    
    # Replace markdown image syntax
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)
    
    # Add journal title if not present
    if not content.startswith('\\journaltitle'):
        # Extract title information
        title_match = re.search(r'### (.+?) - Session (\d+): (.+)', content)
        if title_match:
            date, session, title = title_match.groups()
            journal_title = f"\\journaltitle{{{date}}}{{{session}}}{{{title}}}\n\n"
            content = journal_title + content
    
    # Convert markdown headers to LaTeX sections
    content = re.sub(r'^## (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
    
    # Add margin notes for emphasis
    content = re.sub(r'\*\*([^*]+)\*\*:', r'\\marginnote{\1}', content)
    
    return content

def create_pdf_layout(session_dir):
    """Create PDF layout from markdown content and images"""
    
    session_path = Path(session_dir)
    
    # Find content file
    content_files = [
        session_path / "content" / "journal_final.md",
        session_path / "content" / "journal_draft.md",
        session_path / "content" / "draft_v1.md"
    ]
    
    content_file = None
    for cf in content_files:
        if cf.exists():
            content_file = cf
            break
    
    if not content_file:
        print("❌ No content file found")
        return False
    
    # Load content
    with open(content_file, 'r') as f:
        content = f.read()
    
    # Prepare content for LaTeX
    images_dir = session_path / "images" / "final"
    latex_content = prepare_markdown_for_latex(content, images_dir)
    
    # Create temporary LaTeX file
    temp_tex = session_path / "temp_journal.tex"
    with open(temp_tex, 'w') as f:
        f.write(latex_content)
    
    # Convert to PDF using Pandoc
    output_pdf = session_path / "output" / "journal.pdf"
    output_pdf.parent.mkdir(exist_ok=True)
    
    try:
        cmd = [
            'pandoc',
            str(temp_tex),
            '--template', 'templates/journal_layout.tex',
            '--pdf-engine', 'xelatex',
            '-o', str(output_pdf)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print(f"✅ PDF created: {output_pdf}")
            temp_tex.unlink()  # Clean up temp file
            return True
        else:
            print(f"❌ PDF creation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create-layout.py session_dir")
        sys.exit(1)
    
    session_dir = sys.argv[1]
    success = create_pdf_layout(session_dir)
    
    if not success:
        sys.exit(1)
EOF

chmod +x scripts/create-layout.py
```

## Step 4: Alternative HTML Layout

```bash
cat > scripts/create-html-layout.py << 'EOF'
#!/usr/bin/env python3
import sys
import re
from pathlib import Path

def create_html_layout(session_dir):
    """Create HTML version for web viewing"""
    
    session_path = Path(session_dir)
    
    # Find content file
    content_files = [
        session_path / "content" / "journal_final.md",
        session_path / "content" / "journal_draft.md"
    ]
    
    content_file = None
    for cf in content_files:
        if cf.exists():
            content_file = cf
            break
    
    if not content_file:
        print("❌ No content file found")
        return False
    
    # Load content
    with open(content_file, 'r') as f:
        content = f.read()
    
    # Create HTML template
    html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vellynne Harpell's Research Notes</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap');
        
        body {
            font-family: 'EB Garamond', serif;
            background: linear-gradient(45deg, #f4e4bc, #e8d5a3);
            color: #5d4e37;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="1" fill="%23d4c4a8" opacity="0.3"/><circle cx="80" cy="40" r="1" fill="%23d4c4a8" opacity="0.3"/><circle cx="40" cy="80" r="1" fill="%23d4c4a8" opacity="0.3"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        }
        
        .journal-header {
            text-align: center;
            border-bottom: 3px solid #8b4513;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .journal-title {
            font-family: 'Cinzel', serif;
            font-size: 2.5em;
            color: #8b4513;
            margin: 0;
        }
        
        .journal-subtitle {
            font-family: 'Cinzel', serif;
            font-size: 1.2em;
            color: #5d4e37;
            margin: 10px 0;
        }
        
        .session-info {
            font-size: 1.1em;
            color: #5d4e37;
            margin-top: 15px;
        }
        
        h2 {
            font-family: 'Cinzel', serif;
            color: #8b4513;
            border-bottom: 2px solid #8b4513;
            padding-bottom: 5px;
        }
        
        h3 {
            font-family: 'Cinzel', serif;
            color: #5d4e37;
        }
        
        .illustration {
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background: rgba(255,255,255,0.3);
            border: 2px solid #8b4513;
            border-radius: 10px;
        }
        
        .illustration img {
            max-width: 100%;
            height: auto;
            border: 1px solid #5d4e37;
        }
        
        .illustration-caption {
            font-style: italic;
            color: #5d4e37;
            margin-top: 10px;
        }
        
        .margin-note {
            float: right;
            width: 200px;
            margin: 0 0 10px 20px;
            padding: 10px;
            background: rgba(255,255,255,0.5);
            border-left: 3px solid #8b4513;
            font-size: 0.9em;
            font-style: italic;
        }
        
        @media (max-width: 600px) {
            .margin-note {
                float: none;
                width: auto;
                margin: 10px 0;
            }
        }
    </style>
</head>
<body>
    <div class="journal-header">
        <h1 class="journal-title">Research Notes of Vellynne Harpell</h1>
        <p class="journal-subtitle">Tenth Black Staff of Blackstaff Academy</p>
        <p class="session-info">{session_info}</p>
    </div>
    
    <div class="journal-content">
        {content}
    </div>
</body>
</html>
'''
    
    # Extract session info
    session_match = re.search(r'### (.+?) - Session (\d+): (.+)', content)
    if session_match:
        date, session, title = session_match.groups()
        session_info = f"{date} - Session {session}: {title}"
    else:
        session_info = "Research Session"
    
    # Convert markdown to HTML
    content = re.sub(r'^### .+$', '', content, flags=re.MULTILINE)  # Remove title line
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*([^*]+)\*\*:', r'<div class="margin-note">\1</div>', content, flags=re.MULTILINE)
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', content)
    
    # Convert images
    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        return f'''
        <div class="illustration">
            <img src="images/final/{image_path}.png" alt="{alt_text}">
            <div class="illustration-caption">{alt_text}</div>
        </div>
        '''
    
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)
    
    # Convert paragraphs
    paragraphs = content.split('\n\n')
    html_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if para and not para.startswith('<'):
            html_paragraphs.append(f'<p>{para}</p>')
        elif para:
            html_paragraphs.append(para)
    
    content = '\n\n'.join(html_paragraphs)
    
    # Create final HTML
    html_content = html_template.format(
        session_info=session_info,
        content=content
    )
    
    # Save HTML file
    output_html = session_path / "output" / "journal.html"
    output_html.parent.mkdir(exist_ok=True)
    
    with open(output_html, 'w') as f:
        f.write(html_content)
    
    print(f"✅ HTML created: {output_html}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create-html-layout.py session_dir")
        sys.exit(1)
    
    session_dir = sys.argv[1]
    create_html_layout(session_dir)
EOF

chmod +x scripts/create-html-layout.py
```

## Step 5: Complete Layout Workflow

```bash
cat > scripts/create-final-layout.sh << 'EOF'
#!/bin/bash

SESSION_NUM=$1
if [ -z "$SESSION_NUM" ]; then
    read -p "Session number: " SESSION_NUM
fi

SESSION_PADDED=$(printf "%02d" $SESSION_NUM)
SESSION_DIR="sessions/session-${SESSION_PADDED}"

echo "📄 Creating Final Layout for Session ${SESSION_PADDED}"
echo "=============================================="

# Check prerequisites
if [ ! -f "${SESSION_DIR}/content/journal_final.md" ] && [ ! -f "${SESSION_DIR}/content/journal_draft.md" ]; then
    echo "❌ No journal content found. Complete writing first."
    exit 1
fi

if [ ! -d "${SESSION_DIR}/images/final" ]; then
    echo "❌ No processed images found. Complete image processing first."
    exit 1
fi

# Create output directory
mkdir -p "${SESSION_DIR}/output"

echo "📄 Creating PDF layout..."
python3 scripts/create-layout.py "${SESSION_DIR}"

echo "🌐 Creating HTML layout..."
python3 scripts/create-html-layout.py "${SESSION_DIR}"

# Create layout summary
cat > "${SESSION_DIR}/output/layout_info.json" << EOL
{
  "session": ${SESSION_NUM},
  "created_date": "$(date -Iseconds)",
  "formats": {
    "pdf": "journal.pdf",
    "html": "journal.html"
  },
  "layout_style": "medieval_manuscript",
  "template": "journal_layout.tex",
  "images_included": $(find "${SESSION_DIR}/images/final" -name "*.png" | wc -l),
  "ready_for_distribution": true
}
EOL

echo "✅ Layout creation complete!"
echo "📁 Output files:"
echo "   - PDF: ${SESSION_DIR}/output/journal.pdf"
echo "   - HTML: ${SESSION_DIR}/output/journal.html"
echo "   - Info: ${SESSION_DIR}/output/layout_info.json"

# Update session status
if [ -f "${SESSION_DIR}/session-info.json" ]; then
    jq '.status = "layout_complete" | .layout_created = now' \
       "${SESSION_DIR}/session-info.json" > "${SESSION_DIR}/session-info.json.tmp" && \
       mv "${SESSION_DIR}/session-info.json.tmp" "${SESSION_DIR}/session-info.json"
fi
EOF

chmod +x scripts/create-final-layout.sh
```

## Troubleshooting

### LaTeX Issues
- **Missing fonts**: Install medieval fonts system-wide
- **Package errors**: Install full LaTeX distribution
- **Memory issues**: Use smaller images or reduce quality

### Pandoc Problems
- **Template not found**: Check template path
- **Conversion errors**: Verify markdown syntax
- **Image paths**: Ensure images exist in specified locations

### Layout Problems
- **Images not appearing**: Check file paths and extensions
- **Text overflow**: Adjust margins or font size
- **Style inconsistency**: Verify CSS/LaTeX styling

## Next Steps

With document layout complete:

1. ✅ LaTeX template created for professional formatting
2. ✅ HTML alternative for web viewing
3. ✅ Automated layout generation workflow
4. ✅ Quality control and troubleshooting guides

Continue to **[12-PDF-Generation.md](12-PDF-Generation.md)** to create high-quality PDFs for distribution.

## Quick Commands

```bash
# Create complete layout
./scripts/create-final-layout.sh 01

# PDF only
python3 scripts/create-layout.py sessions/session-01

# HTML only
python3 scripts/create-html-layout.py sessions/session-01
```
