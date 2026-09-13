# Installation Guide for ClipFree

## System Requirements

- **Python**: 3.10 or higher
- **Operating System**: macOS, Linux, or Windows
- **RAM**: 8GB minimum (16GB recommended for large videos)
- **Disk Space**: 20GB free (for models + temp files)
- **Internet**: Stable connection for API calls and downloads

## Step-by-Step Installation

### Step 1: Install System Dependencies

#### macOS (with Homebrew)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install ffmpeg yt-dlp python@3.10

# Verify installations
ffmpeg -version
yt-dlp --version
python3 --version
```

#### Ubuntu/Debian

```bash
# Update package manager
sudo apt-get update

# Install dependencies
sudo apt-get install -y ffmpeg python3.10 python3-pip

# Install yt-dlp
pip install yt-dlp

# Verify installations
ffmpeg -version
yt-dlp --version
python3 --version
```

#### Windows (with Chocolatey)

```powershell
# Install Chocolatey if not already installed (run as Admin)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install dependencies (run as Admin)
choco install ffmpeg yt-dlp python

# Verify installations
ffmpeg -version
yt-dlp --version
python --version
```

#### Windows (Manual)

1. **FFmpeg**:
   - Download from: https://ffmpeg.org/download.html
   - Extract to `C:\ffmpeg`
   - Add to PATH: System Properties → Environment Variables

2. **yt-dlp**:
   - Download from: https://github.com/yt-dlp/yt-dlp/releases
   - Save to `C:\Program Files\yt-dlp`
   - Add to PATH

3. **Python**:
   - Download from: https://www.python.org/downloads/
   - Run installer, **check "Add to PATH"**

### Step 2: Clone ClipFree Repository

```bash
# Clone the repo
git clone https://github.com/johnwangui374-bot/ClipFree.git
cd ClipFree

# Or download as ZIP and extract
# wget https://github.com/johnwangui374-bot/ClipFree/archive/refs/heads/main.zip
# unzip main.zip && cd ClipFree-main
```

### Step 3: Create Python Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 4: Install Python Dependencies

```bash
# Install from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# This installs:
# - yt-dlp
# - openai-whisper
# - google-genai
# - python-dotenv
```

### Step 5: Get Gemini API Key

1. **Visit**: https://ai.google.dev
2. **Click**: "Get API Key"
3. **Create** new API key
4. **Copy** the key

### Step 6: Configure API Key

#### Option A: Environment Variable (Recommended)

```bash
# macOS/Linux
export GEMINI_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# Make permanent (Linux/macOS) - add to ~/.bashrc or ~/.zshrc
echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

#### Option B: .env File

```bash
# Copy example file
cp .env.example .env

# Edit .env (use your favorite editor)
# Add your API key:
# GEMINI_API_KEY=your_api_key_here
```

### Step 7: Verify Installation

```bash
# Check Python version
python --version  # Should be 3.10+

# Check dependencies
python -c "import whisper; print('✅ Whisper OK')"
python -c "import google.genai; print('✅ Gemini OK')"

# Check CLI tools
ffmpeg -version | head -n 1
yt-dlp --version

# Test ClipFree
python clipfree.py --help
```

Expected output:
```
usage: clipfree.py [-h] [--output-dir OUTPUT_DIR] ...
ClipFree: Convert YouTube videos to viral shorts
...
✅ Whisper OK
✅ Gemini OK
ffmpeg version ...
yt-dlp version ...
```

## First-Time Setup Notes

### Whisper Model Download

On first run, Whisper downloads its model (~3GB for large-v3):

```bash
# This will download ~3GB on first run
python clipfree.py "https://www.youtube.com/watch?v=..."
```

**Models cached in**: `~/.cache/whisper/`
- Disable cache: `export WHISPER_CACHE_DIR=/dev/null`
- Use smaller model first: `--whisper-model small`

### Storage Requirements

```
Total disk space needed:
- Whisper model: 3GB (large-v3) / 1GB (medium) / 140MB (small)
- Temp video files: 300MB - 2GB (depends on video)
- Output clips: 20-200MB (depends on number/quality)
- Total: ~5-20GB recommended
```

## Troubleshooting Installation

### Python Version Error

```
error: Python 3.10+ required
```

Solution:
```bash
# Check version
python --version

# macOS: Use python3.10
python3.10 -m venv venv

# Ubuntu: Install python3.10
sudo apt-get install python3.10 python3.10-venv
python3.10 -m venv venv
```

### FFmpeg Not Found

```
Error: FFmpeg not found
```

Solution:
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg

# Windows: Add to PATH after manual install
# Or use: choco install ffmpeg

# Verify
ffmpeg -version
```

### yt-dlp Not Found

```
Error: yt-dlp not found
```

Solution:
```bash
# Install via pip
pip install yt-dlp

# Or system package
brew install yt-dlp  # macOS
sudo apt-get install yt-dlp  # Ubuntu
choco install yt-dlp  # Windows

# Verify
yt-dlp --version
```

### Module Import Errors

```
ModuleNotFoundError: No module named 'whisper'
```

Solution:
```bash
# Ensure venv is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### API Key Not Recognized

```
Error: GEMINI_API_KEY environment variable not set
```

Solution:
```bash
# Verify key is set
echo $GEMINI_API_KEY  # macOS/Linux
echo %GEMINI_API_KEY%  # Windows

# If empty, set it again
export GEMINI_API_KEY="your_key"

# Test
python clipfree.py --help  # Should work
```

### Virtual Environment Issues

```
Command 'python3' not found
```

Solution:
```bash
# Recreate venv
rm -rf venv  # or rmdir venv /s /q on Windows
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

Once installation is complete:

1. **Read the README**: `cat README.md`
2. **Run your first clip**: `python clipfree.py "https://www.youtube.com/watch?v=YOUR_VIDEO"`
3. **Check output**: `ls -la ./clipfree_output/clips/`
4. **Explore options**: `python clipfree.py --help`

## Getting Help

- **Issues**: Open a GitHub issue with installation details
- **Logs**: Check full error output in terminal
- **API Help**: https://ai.google.dev/docs
- **Whisper Docs**: https://github.com/openai/whisper
- **yt-dlp Help**: `yt-dlp --help`
- **FFmpeg Help**: `ffmpeg -h`

---

**You're all set! 🚀 Run ClipFree and start creating viral content!**
