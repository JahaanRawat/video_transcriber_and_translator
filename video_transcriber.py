#!/usr/bin/env python3
import os
import tempfile
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import google.generativeai as genai
import yt_dlp
import subprocess
from pathlib import Path

console = Console()

class VideoTranscriber:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def download_video(self, url: str, output_path: str) -> tuple[str, str]:
        video_path = output_path
        audio_path = output_path.replace('.mp4', '.mp3')
        
        # Download video
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': video_path,
            'quiet': True,
            'no_warnings': True,
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Downloading video...", total=None)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        
        # Extract audio using yt-dlp
        audio_opts = {
            'format': 'bestaudio/best',
            'outtmpl': audio_path.replace('.mp3', ''),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Extracting audio...", total=None)
            
            with yt_dlp.YoutubeDL(audio_opts) as ydl:
                ydl.download([url])
                
        return video_path, audio_path
    
    def extract_audio(self, video_path: str) -> str:
        audio_path = video_path.replace('.mp4', '.mp3')
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Extracting audio...", total=None)
            
            # Use ffmpeg to extract audio
            cmd = [
                'ffmpeg', '-i', video_path,
                '-vn', '-acodec', 'mp3',
                '-y', audio_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            
        return audio_path
    
    def transcribe_audio(self, audio_path: str) -> str:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Transcribing audio...", total=None)
            
            audio_file = genai.upload_file(audio_path)
            
            prompt = """Please transcribe this audio file. 
            Provide a clean, accurate transcription with proper punctuation and paragraphs.
            Include timestamps for major sections if the audio is long."""
            
            response = self.model.generate_content([prompt, audio_file])
            
            genai.delete_file(audio_file.name)
            
        return response.text
    
    def translate_text(self, text: str, target_language: str) -> str:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(f"Translating to {target_language}...", total=None)
            
            prompt = f"""Please translate the following text to {target_language}.
            Maintain the original meaning and tone while ensuring the translation is natural and fluent.
            
            Text to translate:
            {text}"""
            
            response = self.model.generate_content(prompt)
            
        return response.text

@click.command()
@click.option('--url', '-u', required=True, help='Video URL to process')
@click.option('--api-key', '-k', envvar='GEMINI_API_KEY', required=True, help='Gemini API key')
@click.option('--translate', '-t', help='Target language for translation (e.g., Spanish, French)')
@click.option('--output', '-o', help='Output file path for results')
@click.option('--keep-files', is_flag=True, help='Keep downloaded video and audio files')
def main(url, api_key, translate, output, keep_files):
    """Video Transcriber and Translator using Google Gemini AI"""
    
    console.print("[bold cyan]Video Transcriber & Translator[/bold cyan]")
    console.print(f"Processing: {url}\n")
    
    transcriber = VideoTranscriber(api_key)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        video_path = os.path.join(temp_dir, "video.mp4")
        
        try:
            console.print("[yellow]Step 1:[/yellow] Downloading video and extracting audio...")
            video_path, audio_path = transcriber.download_video(url, video_path)
            console.print("[green]✓[/green] Video downloaded and audio extracted successfully\n")
            
            console.print("[yellow]Step 2:[/yellow] Transcribing audio...")
            transcription = transcriber.transcribe_audio(audio_path)
            console.print("[green]✓[/green] Transcription completed\n")
            
            result = f"=== TRANSCRIPTION ===\n\n{transcription}\n\n"
            
            if translate:
                console.print(f"[yellow]Step 3:[/yellow] Translating to {translate}...")
                translation = transcriber.translate_text(transcription, translate)
                console.print(f"[green]✓[/green] Translation completed\n")
                result += f"=== TRANSLATION ({translate.upper()}) ===\n\n{translation}\n"
            
            if output:
                Path(output).write_text(result, encoding='utf-8')
                console.print(f"[green]Results saved to:[/green] {output}")
            else:
                console.print("[bold]Results:[/bold]\n")
                console.print(result)
                
            if keep_files:
                import shutil
                shutil.copy(video_path, "downloaded_video.mp4")
                shutil.copy(audio_path, "extracted_audio.mp3")
                console.print("\n[green]Files saved:[/green] downloaded_video.mp4, extracted_audio.mp3")
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
            raise

if __name__ == "__main__":
    main()