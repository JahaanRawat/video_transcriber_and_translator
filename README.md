# Video Transcriber and Translator

A simple tool that downloads videos, transcribes what's being said, and translates it to any language using Google's AI. Perfect for understanding videos in foreign languages!

## What This Tool Does

- Downloads videos from YouTube and other platforms
- Extracts the audio from videos
- Converts speech to text (transcription)
- Translates the text to any language you want
- Saves everything neatly in folders

## Complete Setup Guide for Mac (Apple Silicon M1/M2/M3)

### Step 1: Install Python

Mac comes with Python, but we need to make sure you have the right version:

1. Open Terminal (press `Cmd + Space`, type "Terminal", press Enter)
2. Check if Python 3 is installed by typing:
   ```
   python3 --version
   ```
3. If you see "Python 3.8" or higher, skip to Step 2
4. If not, install Python:
   - Go to https://www.python.org/downloads/macos/
   - Download the latest macOS installer (make sure it says "universal2" for Apple Silicon)
   - Run the installer

### Step 2: Install Homebrew (if not already installed)

Homebrew is a package manager that makes installing software easy on Mac.

1. Open Terminal
2. Check if Homebrew is installed:
   ```
   brew --version
   ```
3. If you see a version number, skip to Step 3
4. If not, install Homebrew by pasting this entire command:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
5. Follow the instructions on screen (it may ask for your Mac password)
6. After installation, you might see instructions to run commands starting with `echo`. Run those commands.

### Step 3: Install FFmpeg

1. In Terminal, type:
   ```
   brew install ffmpeg
   ```
2. Wait for installation to complete (this may take a few minutes)
3. Verify installation:
   ```
   ffmpeg -version
   ```

### Step 4: Get a Google Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key (looks like: AIzaSy...)
5. Save it somewhere safe - you'll need it every time you use the tool

### Step 5: Download This Tool

**Option A: Download as ZIP (Easiest)**
1. Go to https://github.com/JahaanRawat/video_transcriber_and_translator
2. Click the green "Code" button
3. Click "Download ZIP"
4. The file will download to your Downloads folder
5. Double-click the ZIP file to extract it
6. Move the extracted folder to your Desktop for easy access

**Option B: Using Git (if you have it)**
1. Open Terminal
2. Navigate to Desktop:
   ```
   cd ~/Desktop
   ```
3. Clone the repository:
   ```
   git clone https://github.com/JahaanRawat/video_transcriber_and_translator.git
   ```

### Step 6: Install Required Python Packages

1. Open Terminal
2. Navigate to the tool's folder:
   ```
   cd ~/Desktop/video_transcriber_and_translator
   ```
   (If you put it somewhere else, adjust the path accordingly)
3. Install the required packages:
   ```
   pip3 install -r requirements.txt
   ```
   If that doesn't work, try:
   ```
   python3 -m pip install -r requirements.txt
   ```

## How to Use

1. Open Terminal
2. Navigate to the tool's folder:
   ```
   cd ~/Desktop/video_transcriber_and_translator
   ```
3. Run the program:
   ```
   python3 main.py
   ```
4. Follow the prompts:
   - **Paste your API key** when asked (it will be hidden as you type)
   - **Paste the video URL** (copy from YouTube or other video sites)
   - **Choose where to save** (press Enter for default "./output")
   - **Choose if you want translation** (type 'y' for yes or 'n' for no)
   - **Pick a language** if translating (e.g., Spanish, French, Japanese)
   - **Choose to keep video files** (type 'y' or 'n')

### Example Run

```
Video Transcriber & Translator
Transcribe and translate videos using Google Gemini AI

Enter your Gemini API key: [your key is hidden as you type]

Enter the video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Enter output directory [./output]: my_videos

Do you want to translate the transcription? [y/N]: y
Enter target language [Spanish]: Japanese

Keep downloaded video and audio files? [y/N]: n

Processing: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Step 1: Downloading video and extracting audio...
✓ Video downloaded and audio extracted successfully

Step 2: Transcribing audio...
✓ Transcription completed

Transcription saved to: my_videos/transcription.txt

Step 3: Translating to Japanese...
✓ Translation completed

Translation saved to: my_videos/translation_japanese.txt

✓ All tasks completed successfully!
Check the output directory: my_videos
```

## Where to Find Your Files

After running, your files will be in the output folder you specified:
1. Open Finder
2. Navigate to the tool's folder
3. Look for your output folder (e.g., "my_videos" or "output")
4. Inside you'll find:
   - `transcription.txt` - The original text from the video
   - `translation_[language].txt` - The translated version (if you chose to translate)
   - Video and audio files (if you chose to keep them)

## Common Problems and Solutions (Mac Specific)

**"python3: command not found":**
- Install Python from https://www.python.org/downloads/macos/
- Make sure to download the "universal2" installer for Apple Silicon

**"pip3: command not found":**
- Try: `python3 -m pip install -r requirements.txt`
- Or install pip: `python3 -m ensurepip --upgrade`

**"brew: command not found":**
- Homebrew isn't installed. Follow Step 2 carefully
- After installing, close and reopen Terminal

**Permission denied errors:**
- Add `sudo` before the command: `sudo pip3 install -r requirements.txt`
- Enter your Mac password when prompted

**SSL Certificate errors:**
- Common on Mac. Try: `pip3 install --upgrade certifi`
- Or use: `python3 -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt`

## Tips for Mac Users

- Use `Cmd + Space` to quickly open Terminal
- Drag and drop folders into Terminal to get their path
- Use `Cmd + K` in Terminal to clear the screen
- Your API key is personal - don't share it with others
- Videos are temporarily stored in `/var/folders/` and automatically cleaned up

## Quick Start (After Setup)

Once everything is installed, you just need to:
1. Open Terminal (`Cmd + Space`, type "Terminal")
2. Type: `cd ~/Desktop/video_transcriber_and_translator`
3. Type: `python3 main.py`
4. Follow the prompts!

## Need More Help?

If you're still having issues:
1. Make sure you're using Terminal, not the Python app
2. Check that you're in the right folder (`pwd` shows current folder)
3. Try with a short YouTube video first
4. Make sure your Mac is updated (Apple menu > About This Mac > Software Update)

## Privacy Note

- Your API key is only used to connect to Google's AI service
- Videos are temporarily downloaded and deleted after processing (unless you choose to keep them)
- All files stay on your Mac - nothing is uploaded elsewhere

---

Made with ❤️ for easy video understanding on Mac