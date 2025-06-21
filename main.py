import argparse
import base64
import json
import os
import time
import logging
from pathlib import Path
from typing import List

import requests
import re
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging for urllib3 to show retry messages
logging.basicConfig(level=logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)

###############################################################################
# VLM‑SLAM Loop                                                              #
# ---------------------------------------------------------------------------#
# Streams a sequence of images to **any** OpenRouter‑hosted vision model      #
#                                                                             #
# The script keeps a single conversation going, printing each assistant reply #
# so you can eyeball whether the model succeeds.                              #
###############################################################################

OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
INITIAL_PROMPT = (
    "I'm going to have you 'do SLAM' as a vision LLM, with no algorithmic help. "
    "I just give you a series of pictures, and you make your own map and localize yourself within it. \n"
    "Assume that each new image is at maximum a few steps away from the last one, never a long distance."
    "Be concise. Make your map conceptual instead of exact. i.e. \"the bush is a few steps north of the stone\" "
    "is just fine, no need for exact measurements or directions. Think of yourself as a human orienting themself."
    "Use distictive and descriptive names for things, because you might later see more that are very similar. "
    "and have to name them as well."
    "For each picture I give you, respond with: \n"
    "1. interesting new observations\n"
    "2. your latest map (however you choose to represent it), and \n"
    "3. your current pose within the map. \n"
    "Continue until I tell you we're finished.\n"
)

def b64_data_uri(path: Path) -> str:
    """Return a `data:image/png;base64,...` string from a PNG/JPG file."""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    with path.open("rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"

# Hoisted session for connection pooling and transport-level retries
SESSION = requests.Session()
SESSION.mount("https://", HTTPAdapter(max_retries=Retry(total=3, backoff_factor=0.5))) # Fast retries for transport errors

RETRYABLE_STATUSES = {500, 502, 503, 504}
RETRYABLE_API_CODES = {524, 529} # As identified from prior runs

def send_messages(api_key: str, model: str, messages: List[dict], attempts=5) -> str | None:
    """
    Sends messages to the OpenRouter API with robust, application-level retry logic.
    """
    for i in range(1, attempts + 1):
        try:
            r = SESSION.post(
                OPENROUTER_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={"model": model, "messages": messages, "stream": False},
                timeout=30,
            )

            # Fail fast on non-retryable client errors (4xx)
            if 400 <= r.status_code < 500:
                logging.error(f"Client error {r.status_code}: {r.text}")
                r.raise_for_status() # This will raise an HTTPError to be caught outside

            # Explicitly check for retryable 5xx server errors
            if r.status_code in RETRYABLE_STATUSES:
                raise RuntimeError(f"Retryable HTTP {r.status_code} status")

            data = r.json()

            # Check for retryable API provider errors within the JSON response
            if "error" in data and data.get("error", {}).get("code") in RETRYABLE_API_CODES:
                raise RuntimeError(f"Retryable provider code {data['error']['code']}")
            
            # Check for other API errors and fail fast.
            if "error" in data:
                 logging.error(f"Non-retryable API error: {data['error']}")
                 return None # Or raise a custom non-retryable error

            # Robust message extraction
            return data["choices"][0]["message"]["content"]

        except (requests.RequestException, RuntimeError, KeyError, ValueError, json.JSONDecodeError) as e:
            logging.warning(f"Attempt {i}/{attempts} failed: {e}")
            if i == attempts:
                logging.error(f"All {attempts} attempts failed. Last error: {e}")
                return None # Return None after all retries are exhausted
            time.sleep(2 ** i * 0.5)  # Exponential back-off

def main():
    p = argparse.ArgumentParser(description="Stream images to a VLM for SLAM test")
    p.add_argument("--dir", required=True, help="directory of images, ordered by name")
    p.add_argument("--model", default="google/gemini-2.5-flash-preview-05-20", help="OpenRouter model id")
    p.add_argument("--out", help="write JSON transcript here")
    args = p.parse_args()

    load_dotenv(override=True) # Load environment variables from .env file
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENROUTER_API_KEY in env")

    frames = sorted(Path(args.dir).glob("*.[pj][np]g"), key=lambda path: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', path.name)])
    if not frames:
        raise RuntimeError("No .png/.jpg images found in directory")

    convo = [
        {"role": "system", "content": "You are a vision language model being used for algorithm-free conceptual SLAM (Simultaneous Localization and Mapping)."}
    ]

    print("Prompt sent. Waiting for model's mapping responses...\n")

    for idx, img_path in enumerate(frames, 1):
        # For the first image, include the initial prompt text along with the image
        if idx == 1:
            user_content = [
                {"type": "text", "text": INITIAL_PROMPT},
                {"type": "image_url", "image_url": {"url": b64_data_uri(img_path)}}
            ]
        else:
            # For subsequent images, just send the image
            user_content = [{"type": "image_url", "image_url": {"url": b64_data_uri(img_path)}}]

        convo.append({"role": "user", "content": user_content})
        reply = send_messages(api_key, args.model, convo)
        if not reply:
            print(f"\nFailed to get a response for frame {idx} ({img_path.name}). Halting.")
            break
        # Append assistant response to full transcript
        convo.append({"role": "assistant", "content": reply})

        print(f"--- Frame {idx}: {img_path.name} ---\n{reply}\n")
        # Rate limiting logic is now implicitly handled by the retry backoff

    # After all images are processed, ask the model for a bird's eye view plot
    BIRDS_EYE_VIEW_PROMPT = "Now that you have processed all images, please provide a comprehensive birds-eye view map of the entire environment you explored, clearly indicating the path taken, key landmarks, and your final localized position. Represent this map in a way that is easy to visualize as a plot."
    # For the final bird's eye view prompt, send the full current conversation history
    # as context, so the model has all the information to summarize.
    convo.append({"role": "user", "content": BIRDS_EYE_VIEW_PROMPT})
    birds_eye_reply = send_messages(api_key, args.model, convo)

    if birds_eye_reply:
        convo.append({"role": "assistant", "content": birds_eye_reply}) # Append this final reply to the transcript
        print("\n--- Bird's Eye View Map ---\n")
        print(birds_eye_reply)
    else:
        print("\n--- Failed to get Bird's Eye View Map ---\n")

    if args.out:
        with open(args.out, "w") as f:
            json.dump(convo, f, indent=2)
        print(f"Full transcript written to {args.out}")

if __name__ == "__main__":
    main()

