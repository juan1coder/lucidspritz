import os
import random
import time
import pygame
from threading import Thread
from datetime import datetime

# Function to play audio for a specific duration
def play_audio(file_path, duration=None):
    """Play the audio file for a specific duration using pygame."""
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    if duration:
        time.sleep(duration)
        pygame.mixer.music.stop()
    else:
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    pygame.mixer.quit()

# Function to get playback durations for 3 files
def play_three_files(audio_files):
    """Play 3 files consecutively for predefined durations."""
    durations = [35, 35, 45]  # Fixed durations for the 3 files
    print("Playing 3 files with predefined durations:")
    for i, duration in enumerate(durations):
        file = random.choice(audio_files)
        print(f"Playing {os.path.basename(file)} for {duration} seconds...")
        play_audio(file, duration=duration)
        time.sleep(15)  # Optional pause between files

# Function to prompt the user for playback duration with timeout
def prompt_user_for_duration():
    """Prompt the user for a playback duration with a timeout."""
    duration = None

    def get_input():
        nonlocal duration
        try:
            duration = input("Enter playback duration in seconds (or press Enter to skip): ").strip()
            duration = int(duration) if duration.isdigit() else None
        except ValueError:
            duration = None

    thread = Thread(target=get_input)
    thread.daemon = True
    thread.start()
    thread.join(timeout=15)  # Wait for up to 15 seconds for user input

    return duration

# Function to calculate a random interval
def get_random_interval():
    """Get a randomized interval based on weighted choices."""
    intervals = [176 * 60, 191 * 60, 206 * 60, 221 * 60, 236 * 60]  # In seconds
    weights = [0.03, 0.05, 0.12, 0.14, 0.66]  # Weights for intervals
    return random.choices(intervals, weights=weights, k=1)[0]

# Main script logic
def main():
    folder_path = input("Enter the path to the folder with audio files: ").strip()

    if not os.path.isdir(folder_path):
        print("Invalid folder path. Exiting...")
        return

    audio_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith((".mp3", ".wav"))]

    if not audio_files:
        print("No audio files found in the folder. Exiting...")
        return

    print("Starting random music player...")

    # Play the 3 predefined files at startup
    play_three_files(audio_files)

    while True:
        # Select a random file for additional playback
        random_file = random.choice(audio_files)
        print(f"Selected file: {os.path.basename(random_file)}")

        # Get user-defined or random playback duration
        user_duration = prompt_user_for_duration()
        if user_duration is not None:
            playback_duration = min(user_duration, 60)  # Cap playback duration at 60 seconds
        else:
            playback_duration = random.randint(45, 90)  # Random playback between 15 and 60 seconds

        print(f"Playing {os.path.basename(random_file)} for {playback_duration if playback_duration else 'full length'} seconds...")
        play_audio(random_file, duration=playback_duration)

        play_three_files(audio_files)
    
        # Wait for the next interval
        wait_time = get_random_interval()
        current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S%p")
        print(f"Current time: {current_time} | Waiting for {wait_time // 60} minutes before the next playback...")
        time.sleep(wait_time)

if __name__ == "__main__":
    main()
