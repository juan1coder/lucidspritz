import os
import random
import time
import pygame
from threading import Thread
from datetime import datetime


# Example: Decrease likelihood of playing the entire file over time, random less to play entire files.
def get_weights(files_played):
    base_weight_entire = max(0.01, 0.03 - 0.1 * files_played)  # Reduce by 10% each time
    base_weight_partial = 0.07 - base_weight_entire
    return [base_weight_entire, base_weight_partial]

# Example usage
files_played = 3
weights = get_weights(files_played)

actions = ["play_entire_file", "play_partial_file"]
action = random.choices(actions, weights=weights, k=1)[0]

print(f"After {files_played} files, weights are {weights}. Selected action: {action}")


def get_random_interval(base_minutes=186, variance_minutes=15):
    """Get a randomized interval in seconds."""
    random_minutes = random.randint(-variance_minutes, variance_minutes)
    return (base_minutes + random_minutes) * 60

def get_random_playback_duration(file_path):
    """Get a random playback duration in seconds or decide to play the full file."""
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    file_length = sound.get_length()
    pygame.mixer.quit()  # Release the mixer after retrieving the file length

    #if file_length <= 60:
        #return file_length  # If the file is short, play the entire file
    return random.choice([random.randint(35, 90), file_length])

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

    while True:
        random_file = random.choice(audio_files)

        # Get user input or randomize playback duration
        print(f"Selected file: {os.path.basename(random_file)}")
        user_duration = prompt_user_for_duration()

        # Get playback duration
        if user_duration is not None:
            playback_duration = min(user_duration, get_random_playback_duration(random_file))
        else:
            playback_duration = get_random_playback_duration(random_file)

        print(f"Playing {os.path.basename(random_file)} for {playback_duration if playback_duration else 'full length'} seconds...")
        play_audio(random_file, duration=playback_duration)

        # Fine-tuned intervals with bias
        def get_random_interval():
    # Example: Make shorter intervals more likely
#intervals = [5 * 60, 10 * 60, 20 * 60, 30 * 60, 60 * 60]  # Up to 1 hour
#weights = [0.05, 0.05, 0.3, 0.4, 0.2]  # Higher weights for longer intervals
            intervals = [46 * 60, 81 * 60, 116 * 60, 151 * 60, 186 * 60]  # In 60 seconds
            weights = [0.03, 0.05, 0.12, 0.14, 0.66,]  # Higher weight for shorter intervals
            return random.choices(intervals, weights=weights, k=1)[0]

        # Wait for the next interval
        wait_time = get_random_interval()
        current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S%p")
        print(f"Current time: {current_time} | Waiting for {wait_time // 60} minutes before the next playback...")
        time.sleep(wait_time)
     
if __name__ == "__main__":
    main()
