#!/usr/bin/env python3
"""
ClipFree: 100% Free & Open Source Long-Form to Viral Shorts Pipeline
Stack: yt-dlp -> OpenAI Whisper -> Gemini 2.0 Flash -> FFmpeg

Usage:
    python clipfree.py <youtube_url> [--output-dir ./clipfree_output] [--max-clips 10]
"""

import os
import sys
import json
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime

try:
    import whisper
    from google import genai
    from google.genai import types
except ImportError as e:
    print(f"❌ Missing dependencies. Run: pip install -r requirements.txt")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ClipFreeConfig:
    """Configuration management for ClipFree"""
    def __init__(self, output_dir: Path = None, max_clips: int = 10, whisper_model: str = "large-v3"):
        self.output_dir = Path(output_dir or "./clipfree_output")
        self.max_clips = max_clips
        self.whisper_model = whisper_model
        self.api_key = os.environ.get("GEMINI_API_KEY")
        
        # Create output structure
        self.output_dir.mkdir(exist_ok=True)
        self.clips_dir = self.output_dir / "clips"
        self.clips_dir.mkdir(exist_ok=True)
        self.temp_dir = self.output_dir / "temp"
        self.temp_dir.mkdir(exist_ok=True)
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.api_key:
            logger.error("❌ GEMINI_API_KEY environment variable not set")
            return False
        
        # Check for required CLI tools
        for tool in ["yt-dlp", "ffmpeg"]:
            if subprocess.run(["which", tool], capture_output=True).returncode != 0:
                logger.error(f"❌ {tool} not found. Install it first.")
                return False
        
        return True

def download_video(url: str, config: ClipFreeConfig) -> Optional[Path]:
    """Step 1: Download highest quality stream using yt-dlp"""
    logger.info(f"📥 Downloading: {url}")
    
    try:
        out_template = str(config.temp_dir / "source_video.%(ext)s")
        cmd = [
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", out_template,
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            logger.error(f"❌ Download failed: {result.stderr}")
            return None
        
        video_path = config.temp_dir / "source_video.mp4"
        if not video_path.exists():
            logger.error("❌ Video file not created after download")
            return None
        
        file_size_mb = video_path.stat().st_size / (1024 ** 2)
        logger.info(f"✅ Downloaded: {file_size_mb:.1f}MB")
        return video_path
    
    except Exception as e:
        logger.error(f"❌ Download error: {e}")
        return None

def transcribe_with_whisper(video_path: Path, config: ClipFreeConfig) -> Optional[Dict]:
    """Step 2: Speech-to-text with word-level timestamps via Whisper AI"""
    logger.info(f"🎙️  Transcribing with Whisper ({config.whisper_model})...")
    
    try:
        logger.info("Loading Whisper model (first run may take 5-10 minutes)...")
        model = whisper.load_model(config.whisper_model)
        
        logger.info("Transcribing audio...")
        result = model.transcribe(str(video_path), word_level_timestamps=True, fp16=False)
        
        # Save transcript
        transcript_path = config.output_dir / "transcript.json"
        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        num_segments = len(result.get("segments", []))
        duration = result.get("duration", 0)
        logger.info(f"✅ Transcribed: {num_segments} segments, {duration:.1f}s total")
        
        return result
    
    except Exception as e:
        logger.error(f"❌ Transcription error: {e}")
        return None

def find_viral_clips_with_llm(transcript_data: Dict, config: ClipFreeConfig) -> Optional[List[Dict]]:
    """Step 3: Analyze transcript for top viral segments using Gemini"""
    logger.info(f"✨ Analyzing with Gemini (finding top {config.max_clips} clips)...")
    
    try:
        client = genai.Client(api_key=config.api_key)
        
        # Build segment summary
        segments = transcript_data.get("segments", [])
        segments_summary = [
            {
                "start": round(s["start"], 2),
                "end": round(s["end"], 2),
                "text": s["text"].strip()
            }
            for s in segments[:150]  # Limit to first 150 segments for token efficiency
        ]
        
        if not segments_summary:
            logger.error("❌ No segments found in transcript")
            return None
        
        prompt = f"""You are a viral content expert. Analyze this transcript and find the TOP {config.max_clips} most viral highlight clips.

Each clip should:
- Be 25-60 seconds long
- Have a STRONG hook in the first 0-3 seconds (question, surprise, statement)
- Be self-contained and engaging
- Have high re-watch value (entertainment, education, or shock value)

Return a VALID JSON array with exactly {config.max_clips} objects. Each object must have:
- clipNumber (1-{config.max_clips})
- start_time (in seconds)
- end_time (in seconds)
- title (catchy, max 50 chars)
- hook (the first 0-3s hook text, max 30 chars)
- viralScore (1-100)
- viralReason (why this will go viral, max 50 chars)

Transcript segments:
{json.dumps(segments_summary, ensure_ascii=False)}

Return ONLY valid JSON, no other text."""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.7
            )
        )
        
        # Parse response
        try:
            clips = json.loads(response.text)
            if isinstance(clips, dict) and "clips" in clips:
                clips = clips["clips"]
            
            if not isinstance(clips, list):
                logger.error(f"❌ Invalid response format: {response.text[:200]}")
                return None
            
            # Validate clips
            valid_clips = []
            for clip in clips:
                if all(k in clip for k in ["start_time", "end_time", "title"]):
                    valid_clips.append(clip)
            
            if not valid_clips:
                logger.error(f"❌ No valid clips in response")
                return None
            
            logger.info(f"✅ Found {len(valid_clips)} viral clips")
            
            # Save clips metadata
            clips_metadata_path = config.output_dir / "clips_metadata.json"
            with open(clips_metadata_path, "w", encoding="utf-8") as f:
                json.dump(valid_clips, f, indent=2, ensure_ascii=False)
            
            return valid_clips
        
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse LLM response: {e}")
            logger.debug(f"Response text: {response.text[:500]}")
            return None
    
    except Exception as e:
        logger.error(f"❌ LLM analysis error: {e}")
        return None

def render_vertical_clip(source_video: Path, clip_info: Dict, output_path: Path) -> bool:
    """Step 4: Crop to 9:16 vertical and export 1080x1920 MP4 via FFmpeg"""
    try:
        start = clip_info["start_time"]
        end = clip_info["end_time"]
        duration = end - start
        
        # Safety checks
        if duration <= 0:
            logger.warning(f"⚠️  Skipping clip {clip_info.get('clipNumber', '?')}: invalid duration")
            return False
        
        if duration > 120:
            logger.warning(f"⚠️  Clip {clip_info.get('clipNumber', '?')} exceeds 2 min, trimming...")
            duration = 120
        
        # FFmpeg filter: crop center to 9:16, scale to 1080x1920
        vf_filter = "crop=ih*(9/16):ih:(iw-(ih*(9/16)))/2:0,scale=1080:1920:flags=lanczos"
        
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-t", str(duration),
            "-i", str(source_video),
            "-vf", vf_filter,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",  # Slightly higher CRF for faster encoding
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode == 0 and output_path.exists():
            file_size_mb = output_path.stat().st_size / (1024 ** 2)
            title = clip_info.get("title", "Unknown")
            logger.info(f"✅ Rendered: {output_path.name} ({file_size_mb:.1f}MB) - {title}")
            return True
        else:
            logger.error(f"❌ FFmpeg failed for {output_path.name}: {result.stderr}")
            return False
    
    except Exception as e:
        logger.error(f"❌ Rendering error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="ClipFree: Convert YouTube videos to viral shorts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python clipfree.py 'https://www.youtube.com/watch?v=...' 
  python clipfree.py 'https://www.youtube.com/watch?v=...' --max-clips 5 --output-dir ./my_clips

Requirements:
  - ffmpeg
  - yt-dlp
  - GEMINI_API_KEY environment variable set
        """
    )
    
    parser.add_argument("url", nargs="?", help="YouTube video URL")
    parser.add_argument("--output-dir", default="./clipfree_output", help="Output directory (default: ./clipfree_output)")
    parser.add_argument("--max-clips", type=int, default=10, help="Maximum number of clips to generate (default: 10)")
    parser.add_argument("--whisper-model", default="large-v3", choices=["tiny", "base", "small", "medium", "large-v3"], help="Whisper model size")
    parser.add_argument("--skip-transcription", action="store_true", help="Skip transcription (use existing transcript.json)")
    parser.add_argument("--skip-analysis", action="store_true", help="Skip LLM analysis (use existing clips_metadata.json)")
    
    args = parser.parse_args()
    
    if not args.url:
        parser.print_help()
        print("\n❌ YouTube URL required")
        sys.exit(1)
    
    # Initialize config
    config = ClipFreeConfig(
        output_dir=args.output_dir,
        max_clips=args.max_clips,
        whisper_model=args.whisper_model
    )
    
    if not config.validate():
        sys.exit(1)
    
    logger.info("🚀 ClipFree Pipeline Starting...")
    logger.info(f"Output directory: {config.output_dir}")
    
    start_time = datetime.now()
    
    # Step 1: Download
    video_path = download_video(args.url, config)
    if not video_path:
        logger.error("\n❌ Pipeline failed at download step")
        sys.exit(1)
    
    # Step 2: Transcribe
    transcript_data = None
    if args.skip_transcription:
        transcript_path = config.output_dir / "transcript.json"
        if transcript_path.exists():
            logger.info("📖 Using existing transcript.json")
            with open(transcript_path) as f:
                transcript_data = json.load(f)
        else:
            logger.error("❌ transcript.json not found")
            sys.exit(1)
    else:
        transcript_data = transcribe_with_whisper(video_path, config)
    
    if not transcript_data:
        logger.error("\n❌ Pipeline failed at transcription step")
        sys.exit(1)
    
    # Step 3: Analyze with LLM
    clips = None
    if args.skip_analysis:
        clips_metadata_path = config.output_dir / "clips_metadata.json"
        if clips_metadata_path.exists():
            logger.info("📋 Using existing clips_metadata.json")
            with open(clips_metadata_path) as f:
                clips = json.load(f)
        else:
            logger.error("❌ clips_metadata.json not found")
            sys.exit(1)
    else:
        clips = find_viral_clips_with_llm(transcript_data, config)
    
    if not clips:
        logger.error("\n❌ Pipeline failed at analysis step")
        sys.exit(1)
    
    # Step 4: Render clips
    logger.info(f"\n🎬 Rendering {len(clips)} clips...")
    success_count = 0
    
    for i, clip in enumerate(clips, 1):
        clip_num = clip.get("clipNumber", i)
        output_path = config.clips_dir / f"clip_{clip_num:02d}.mp4"
        
        if render_vertical_clip(video_path, clip, output_path):
            success_count += 1
    
    # Summary
    elapsed = datetime.now() - start_time
    logger.info(f"\n" + "="*60)
    logger.info(f"✅ Pipeline Complete!")
    logger.info(f"   Clips rendered: {success_count}/{len(clips)}")
    logger.info(f"   Time elapsed: {elapsed}")
    logger.info(f"   Output: {config.clips_dir}")
    logger.info(f"\n   Metadata: {config.output_dir / 'clips_metadata.json'}")
    logger.info(f"   Transcript: {config.output_dir / 'transcript.json'}")
    logger.info(f"="*60)

if __name__ == "__main__":
    main()
