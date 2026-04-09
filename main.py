import os
import sys

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from audio_tools import AudioLoader, AudioProcessor

def main():
    # Setup base path 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_folder = os.path.join(base_dir, "audio_data")

    # Initialize Loader
    loader = AudioLoader(audio_folder)
    processor = AudioProcessor()

    print("=== DrumLogs Utility Test ===")
    
    # List Categories
    categories = loader.list_categories()
    print(f"Categories found: {categories}")

    if not categories:
        print("\n[!] No audio categories found. Please create folders in 'audio_data/'")
        return

    # Scan Category 
    first_cat = categories[0]
    samples = loader.get_sample(first_cat)

    print(f"\nSamples in '{first_cat}':")
    for name, path in samples.items():
        duration = processor.get_duration(path)
        print(f"- {name}")
        print(f"  Path: {path}")
        print(f"  Duration: {duration:.2f} seconds")

if __name__ == "__main__":
    main()
