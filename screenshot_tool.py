import mss
import mss.tools
from PIL import Image
import time
import sys
import os

def start_screenshot_capture(interval_seconds: int, output_dir: str):
    """
    Captures screenshots of the primary monitor at a specified interval and saves them
    to the given output directory.

    Args:
        interval_seconds (int): The interval in seconds between screenshots.
        output_dir (str): The directory where screenshots will be saved.
    """
    if not isinstance(interval_seconds, int) or interval_seconds <= 0:
        raise ValueError("Interval must be a positive integer.")
    
    os.makedirs(output_dir, exist_ok=True) # Create output directory if it doesn't exist

    sct = mss.mss()
    monitor = sct.monitors[0]  # Capture the primary monitor

    print(f"Starting screenshot capture every {interval_seconds} seconds. Screenshots will be saved to '{output_dir}'. Press Ctrl+C to stop.")

    try:
        while True:
            # Grab the screenshot
            sct_img = sct.grab(monitor)
            
            # Define filename with timestamp
            timestamp = int(time.time())
            filename = os.path.join(output_dir, f"screenshot_{timestamp}.png")

            # Save to the specified directory
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)

            print(f"Screenshot saved: {filename}")

            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nScreenshot capture stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python screenshot_tool.py <interval_seconds> <output_directory>")
        sys.exit(1)
    try:
        capture_interval = int(sys.argv[1])
        output_directory = sys.argv[2]
        start_screenshot_capture(capture_interval, output_directory)
    except ValueError: # Catch for capture_interval
        print("Error: Interval must be a positive integer.")
        sys.exit(1)