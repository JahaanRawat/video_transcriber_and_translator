#!/usr/bin/env python3
import os
import sys
import tempfile
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
import google.generativeai as genai
from video_transcriber import VideoTranscriber

console = Console()

def get_user_inputs():
    console.print(Panel.fit(
        "[bold cyan]Video Transcriber & Translator[/bold cyan]\n"
        "Transcribe and translate videos using Google Gemini AI",
        border_style="cyan"
    ))
    console.print()
    
    # Get API key
    api_key = Prompt.ask(
        "[yellow]Enter your Gemini API key[/yellow]",
        password=True
    )
    
    # Get video URL
    video_url = Prompt.ask(
        "\n[yellow]Enter the video URL[/yellow]",
        default=""
    )
    
    # Get output directory
    output_dir = Prompt.ask(
        "\n[yellow]Enter output directory[/yellow]",
        default="./output"
    )
    
    # Ask about translation
    translate = Confirm.ask("\n[yellow]Do you want to translate the transcription?[/yellow]")
    target_language = None
    if translate:
        target_language = Prompt.ask(
            "[yellow]Enter target language[/yellow]",
            default="Spanish"
        )
    
    # Ask about keeping files
    keep_files = Confirm.ask("\n[yellow]Keep downloaded video and audio files?[/yellow]")
    
    return {
        'api_key': api_key,
        'video_url': video_url,
        'output_dir': output_dir,
        'target_language': target_language,
        'keep_files': keep_files
    }

def main():
    try:
        # Get user inputs
        inputs = get_user_inputs()
        
        # Create output directory if it doesn't exist
        output_dir = Path(inputs['output_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        console.print(f"\n[bold]Processing:[/bold] {inputs['video_url']}\n")
        
        # Initialize transcriber
        transcriber = VideoTranscriber(inputs['api_key'])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            video_path = os.path.join(temp_dir, "video.mp4")
            
            # Download and process video
            console.print("[yellow]Step 1:[/yellow] Downloading video and extracting audio...")
            video_path, audio_path = transcriber.download_video(inputs['video_url'], video_path)
            console.print("[green]✓[/green] Video downloaded and audio extracted successfully\n")
            
            # Transcribe audio
            console.print("[yellow]Step 2:[/yellow] Transcribing audio...")
            transcription = transcriber.transcribe_audio(audio_path)
            console.print("[green]✓[/green] Transcription completed\n")
            
            # Save transcription
            transcription_file = output_dir / "transcription.txt"
            transcription_file.write_text(f"=== TRANSCRIPTION ===\n\n{transcription}\n", encoding='utf-8')
            console.print(f"[green]Transcription saved to:[/green] {transcription_file}")
            
            # Translate if requested
            if inputs['target_language']:
                console.print(f"\n[yellow]Step 3:[/yellow] Translating to {inputs['target_language']}...")
                translation = transcriber.translate_text(transcription, inputs['target_language'])
                console.print(f"[green]✓[/green] Translation completed\n")
                
                # Save translation
                translation_file = output_dir / f"translation_{inputs['target_language'].lower()}.txt"
                translation_file.write_text(
                    f"=== TRANSLATION ({inputs['target_language'].upper()}) ===\n\n{translation}\n", 
                    encoding='utf-8'
                )
                console.print(f"[green]Translation saved to:[/green] {translation_file}")
            
            # Keep files if requested
            if inputs['keep_files']:
                import shutil
                video_output = output_dir / "downloaded_video.mp4"
                audio_output = output_dir / "extracted_audio.mp3"
                shutil.copy(video_path, video_output)
                shutil.copy(audio_path, audio_output)
                console.print(f"\n[green]Video saved to:[/green] {video_output}")
                console.print(f"[green]Audio saved to:[/green] {audio_output}")
            
            console.print("\n[bold green]✓ All tasks completed successfully![/bold green]")
            console.print(f"[dim]Check the output directory: {output_dir}[/dim]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
