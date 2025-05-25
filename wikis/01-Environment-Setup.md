# 01 - Environment Setup

Setting up your development environment for creating Vellynne Harpell's research notes.

## Prerequisites Checklist

- [ ] Computer with macOS, Linux, or Windows 10/11
- [ ] Administrator/sudo access
- [ ] Stable internet connection
- [ ] At least 5GB free disk space

## Overview

We'll install the essential tools needed for the entire journal creation workflow:
- Python (for Whisper AI transcription)
- Node.js (for automation scripts)
- Git (for version control)
- ImageMagick (for image processing)
- Pandoc (for document conversion)

## Step 1: Install Package Manager

### macOS
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Verify installation
brew --version
```

### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install essential build tools
sudo apt install -y curl wget git build-essential
```

### Windows
```powershell
# Install Chocolatey (run as Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Verify installation
choco --version
```

## Step 2: Install Python

### macOS
```bash
# Install Python 3.11
brew install python@3.11

# Verify installation
python3 --version
pip3 --version
```

### Linux
```bash
# Install Python 3.11
sudo apt install -y python3.11 python3.11-pip python3.11-venv

# Verify installation
python3.11 --version
pip3 --version
```

### Windows
```powershell
# Install Python
choco install python311 -y

# Verify installation (restart terminal first)
python --version
pip --version
```

## Step 3: Install Node.js

### macOS
```bash
# Install Node.js
brew install node

# Verify installation
node --version
npm --version
```

### Linux
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

### Windows
```powershell
# Install Node.js
choco install nodejs -y

# Verify installation (restart terminal first)
node --version
npm --version
```

## Step 4: Install Additional Tools

### macOS
```bash
# Install ImageMagick for image processing
brew install imagemagick

# Install Pandoc for document conversion
brew install pandoc

# Install FFmpeg for audio processing
brew install ffmpeg

# Verify installations
magick --version
pandoc --version
ffmpeg -version
```

### Linux
```bash
# Install ImageMagick
sudo apt install -y imagemagick

# Install Pandoc
sudo apt install -y pandoc

# Install FFmpeg
sudo apt install -y ffmpeg

# Verify installations
convert --version
pandoc --version
ffmpeg -version
```

### Windows
```powershell
# Install ImageMagick
choco install imagemagick -y

# Install Pandoc
choco install pandoc -y

# Install FFmpeg
choco install ffmpeg -y

# Verify installations (restart terminal first)
convert --version
pandoc --version
ffmpeg -version
```

## Step 5: Install Whisper AI

```bash
# Create a virtual environment for Python packages
python3 -m venv vellynne-env

# Activate the virtual environment
# macOS/Linux:
source vellynne-env/bin/activate
# Windows:
# vellynne-env\Scripts\activate

# Install Whisper AI
pip install openai-whisper

# Verify installation
whisper --help
```

## Step 6: Set Up Project Directory

```bash
# Create main project directory
mkdir vellynne-notes
cd vellynne-notes

# Create subdirectories
mkdir -p {audio,transcripts,content,images,templates,output,scripts}

# Create a .gitignore file
cat > .gitignore << 'EOF'
# Audio files (large)
audio/*.wav
audio/*.mp3
audio/*.m4a

# Virtual environment
vellynne-env/

# API keys
.env
config/secrets.json

# Temporary files
*.tmp
*.temp
.DS_Store
Thumbs.db

# Output files (can be regenerated)
output/*.pdf
EOF

# Initialize git repository
git init
git add .gitignore
git commit -m "Initial project setup"
```

## Step 7: Create Environment Configuration

```bash
# Create environment file for API keys
cat > .env << 'EOF'
# OpenAI API Key (for image generation)
OPENAI_API_KEY=your_openai_api_key_here

# Stability AI API Key (alternative for image generation)
STABILITY_API_KEY=your_stability_api_key_here

# Discord Bot Token (for Craig bot integration)
DISCORD_BOT_TOKEN=your_discord_bot_token_here
EOF

echo "⚠️  Remember to add your actual API keys to the .env file!"
```

## Step 8: Verify Complete Setup

```bash
# Run verification script
cat > verify-setup.sh << 'EOF'
#!/bin/bash

echo "🔍 Verifying Vellynne Notes Environment Setup..."
echo

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python: $(python3 --version)"
else
    echo "❌ Python not found"
fi

# Check Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js: $(node --version)"
else
    echo "❌ Node.js not found"
fi

# Check ImageMagick
if command -v convert &> /dev/null; then
    echo "✅ ImageMagick: $(convert --version | head -n1)"
else
    echo "❌ ImageMagick not found"
fi

# Check Pandoc
if command -v pandoc &> /dev/null; then
    echo "✅ Pandoc: $(pandoc --version | head -n1)"
else
    echo "❌ Pandoc not found"
fi

# Check FFmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg: $(ffmpeg -version | head -n1)"
else
    echo "❌ FFmpeg not found"
fi

# Check Whisper (in virtual environment)
if [ -f "vellynne-env/bin/activate" ]; then
    source vellynne-env/bin/activate
    if command -v whisper &> /dev/null; then
        echo "✅ Whisper AI: Installed"
    else
        echo "❌ Whisper AI not found"
    fi
    deactivate
else
    echo "❌ Virtual environment not found"
fi

echo
echo "🏁 Setup verification complete!"
EOF

chmod +x verify-setup.sh
./verify-setup.sh
```

## Troubleshooting

### Common Issues

**Python not found:**
- Make sure you're using `python3` not `python`
- On Windows, try `py` instead of `python3`

**Permission denied:**
- Use `sudo` on Linux/macOS for system-wide installations
- Run PowerShell as Administrator on Windows

**Virtual environment activation fails:**
- Check the path: `vellynne-env/bin/activate` (Unix) or `vellynne-env\Scripts\activate` (Windows)
- Make sure you're in the project directory

**ImageMagick security policy errors:**
- Edit `/etc/ImageMagick-6/policy.xml` (Linux) or similar on other systems
- Change PDF policy from "none" to "read|write"

## Next Steps

Once your environment is set up:

1. ✅ All tools installed and verified
2. ✅ Project directory structure created
3. ✅ Virtual environment configured
4. ✅ Git repository initialized

Continue to **[02-Project-Structure.md](02-Project-Structure.md)** to set up the detailed project organization.

## Additional Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [Homebrew Documentation](https://docs.brew.sh/)
- [Chocolatey Documentation](https://docs.chocolatey.org/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
