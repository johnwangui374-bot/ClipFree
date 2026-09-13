# 🎬 ClipFree

**100% Free & Open Source Long-Form to Viral Shorts Pipeline**

Automatically convert YouTube videos into optimized viral short-form clips (9:16 vertical format) using state-of-the-art AI:
- **yt-dlp** for high-quality downloads
- **OpenAI Whisper** for accurate transcription
- **Google Gemini 2.0 Flash** for intelligent clip detection
- **FFmpeg** for professional video encoding

## ✨ Features

✅ **Fully Automated** - One command to go from YouTube URL → viral clips
✅ **AI-Powered** - Gemini analyzes transcripts to find the best moments
✅ **Optimized Output** - Professional 1080×1920 vertical MP4s
✅ **Free & Open Source** - MIT Licensed, no costs beyond API calls
✅ **Error Handling** - Robust error recovery and detailed logging
✅ **Configurable** - Adjust clip count, Whisper model, output location

## 📋 Requirements

### System Dependencies

```bash
# macOS
brew install ffmpeg yt-dlp python@3.10

# Ubuntu/Debian
sudo apt-get install ffmpeg python3-pip
pip install yt-dlp

# Windows (using Chocolatey)
choco install ffmpeg yt-dlp python
```

### API Keys

1. **Google Gemini API** (Free tier available)
   - Get key: https://ai.google.dev
   - Set environment variable: `export GEMINI_API_KEY=your_key`

### Python Environment

Python 3.10+ required

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/johnwangui374-bot/ClipFree.git
cd ClipFree
pip install -r requirements.txt
```

### 2. Set API Key

```bash
# Option A: Export environment variable
export GEMINI_API_KEY="your_api_key_here"

# Option B: Create .env file
cp .env.example .env
# Edit .env and add your API key
```

### 3. Run Pipeline

```bash
# Basic usage
python clipfree.py "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

# Advanced options
python clipfree.py "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --max-clips 5 \
  --output-dir ./my_clips \
  --whisper-model medium
```

### 4. Find Your Clips

All clips will be in `./clipfree_output/clips/`:
- `clip_01.mp4`, `clip_02.mp4`, etc. (ready to upload)
- `clips_metadata.json` (metadata with hooks, scores, reasons)
- `transcript.json` (full transcription with timestamps)

## 📖 Usage Examples

### Generate 10 viral clips (default)
```bash
python clipfree.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Generate only 5 clips with smaller Whisper model (faster)
```bash
python clipfree.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --max-clips 5 \
  --whisper-model small
```

### Custom output directory
```bash
python clipfree.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --output-dir ~/Videos/viral_clips
```

### Reuse existing transcript (skip download/transcribe)
```bash
python clipfree.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --skip-transcription
```

### Reuse existing analysis (skip LLM call)
```bash
python clipfree.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --skip-analysis
```

## 🎯 Command-Line Options

```
usage: clipfree.py [-h] [--output-dir OUTPUT_DIR] [--max-clips MAX_CLIPS]
                   [--whisper-model {tiny,base,small,medium,large-v3}]
                   [--skip-transcription] [--skip-analysis]
                   [url]

ClipFree: Convert YouTube videos to viral shorts

positional arguments:
  url                   YouTube video URL

options:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        Output directory (default: ./clipfree_output)
  --max-clips MAX_CLIPS
                        Maximum number of clips (default: 10)
  --whisper-model {tiny,base,small,medium,large-v3}
                        Whisper model size (default: large-v3)
  --skip-transcription  Skip transcription, use existing transcript.json
  --skip-analysis       Skip LLM analysis, use existing clips_metadata.json
```

## ⏱️ Processing Times

*Estimates for typical 10-minute video on standard hardware:*

| Step | Model | Time |
|------|-------|------|
| **Download** | yt-dlp | 1-3 min |
| **Transcribe** | large-v3 | 5-8 min |
| **Transcribe** | medium | 2-3 min |
| **Transcribe** | small | 1-2 min |
| **Analyze** | Gemini Flash | 10-30 sec |
| **Render 10 clips** | FFmpeg | 2-5 min |
| **Total** | — | ~10-20 min |

💡 **Tip**: Use `--whisper-model small` for 5-10x faster transcription with minor accuracy loss.

## 📊 Output Structure

```
clipfree_output/
├── transcript.json           # Full Whisper output (text, timing)
├── clips_metadata.json       # LLM-selected clips + metadata
├── clips/
│   ├── clip_01.mp4          # Vertical short (1080×1920)
│   ├── clip_02.mp4
│   └── ... (up to max-clips)
└── temp/
    └── source_video.mp4     # Downloaded video (can delete)
```

## 🎬 Clip Metadata Format

Each clip in `clips_metadata.json`:

```json
{
  "clipNumber": 1,
  "start_time": 45.2,
  "end_time": 72.5,
  "title": "Mind-blowing reveal",
  "hook": "Wait for the twist...",
  "viralScore": 92,
  "viralReason": "Shock value + curiosity"
}
```

## 🔧 Troubleshooting

### `GEMINI_API_KEY not found`
```bash
# Check if set
echo $GEMINI_API_KEY

# Set it
export GEMINI_API_KEY="your_key"

# Or create .env
cp .env.example .env
# Edit .env with your key
```

### `yt-dlp not found`
```bash
# Install yt-dlp
pip install yt-dlp
# or
brew install yt-dlp  # macOS
sudo apt-get install yt-dlp  # Ubuntu
```

### `ffmpeg not found`
```bash
brew install ffmpeg      # macOS
sudo apt-get install ffmpeg  # Ubuntu
choco install ffmpeg     # Windows
```

### `Whisper model download fails`
- First run downloads ~3GB (large-v3)
- Ensure stable internet connection
- Models cached locally after first download
- Use smaller model if disk space is limited

### `API quota exceeded`
- Gemini free tier: 15 requests/minute
- Check usage: https://ai.google.dev
- Wait or upgrade for higher limits

### `FFmpeg encoding too slow`
- Use `-preset ultrafast` instead of `fast` (lower quality)
- Use smaller Whisper model (`--whisper-model small`)
- Reduce video resolution at source

## 📝 Example Output Log

```
2024-09-13 14:23:45 - INFO - 🚀 ClipFree Pipeline Starting...
2024-09-13 14:23:45 - INFO - Output directory: ./clipfree_output
2024-09-13 14:23:45 - INFO - 📥 Downloading: https://www.youtube.com/watch?v=dQw4w9WgXcQ
2024-09-13 14:26:12 - INFO - ✅ Downloaded: 285.3MB
2024-09-13 14:26:12 - INFO - 🎙️  Transcribing with Whisper (large-v3)...
2024-09-13 14:26:13 - INFO - Loading Whisper model (first run may take 5-10 minutes)...
2024-09-13 14:32:45 - INFO - ✅ Transcribed: 124 segments, 615.3s total
2024-09-13 14:32:46 - INFO - ✨ Analyzing with Gemini (finding top 10 clips)...
2024-09-13 14:32:52 - INFO - ✅ Found 10 viral clips
2024-09-13 14:32:53 - INFO - 🎬 Rendering 10 clips...
2024-09-13 14:38:15 - INFO - ✅ Rendered: clip_01.mp4 (28.5MB) - Mind-blowing reveal
... (9 more clips)
2024-09-13 14:46:30 - INFO - ✅ Pipeline Complete!
2024-09-13 14:46:30 - INFO -    Clips rendered: 10/10
2024-09-13 14:46:30 - INFO -    Time elapsed: 0:23:45
2024-09-13 14:46:30 - INFO -    Output: ./clipfree_output/clips
```

## 🎯 Pro Tips for Viral Clips

1. **Hook is Everything** - First 3 seconds determine if viewer watches
   - Questions: "Did you know...?"
   - Surprises: "Wait, what?!"
   - Statements: "This changes everything"

2. **Optimal Length** - 25-60 seconds on TikTok/Shorts/Reels
   - 25-35s: Quick takeaways (trending, news)
   - 35-50s: Stories, tutorials, reactions
   - 50-60s: Full narratives, debates

3. **Vertical Format** - 9:16 aspect ratio performs best
   - ClipFree crops to center automatically
   - Ensure subjects centered in original video

4. **Captions Boost Engagement** - Consider adding:
   - AI captions via CapCut, Adobe, or manual
   - Highlight the hook text
   - Track trending audio/sounds

## 📜 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Open issues or PRs for:
- Bug fixes
- Performance improvements
- New LLM backends (Claude, GPT-4, etc.)
- Better vertical video cropping
- Automated caption generation

## ⚠️ Disclaimer

- Always respect video copyrights and platform terms of service
- Only process videos you own or have permission to use
- API calls may incur costs (though Gemini offers free tier)
- This tool is for educational purposes

## 🙋 Support

Running into issues?
1. Check troubleshooting section above
2. Review logs for error messages
3. Open a GitHub issue with:
   - Command you ran
   - Full error message/log
   - System info (OS, Python version, FFmpeg version)

---

**Made with ❤️ for creators everywhere**

Give us a ⭐ if ClipFree helps you go viral!
