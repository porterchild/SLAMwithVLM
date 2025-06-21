# VLM-SLAM Loop

**Purpose:** This project is to explore whether VLMs can conceptually do SLAM like a human (coarse, approximate, and good enough for most navigation purposes), without any actual SLAM algorithms. Just the VLM.

## Model Compatibility Notes

Based on testing for multi-image performance:
*   Gemini Models (flash, pro): Can currently seamlessly handle a lot of images.
*   Claude looks like it can handle ~100
*   Other Models (e.g., Llama4, Gemma3): May have limitations such as strict image attachment limits (Llama) or specific instruction format requirements (Gemma). Gemma3-27b starts giving me api errors after ~5 images, llama4-scout after ~9. So those could be used with some context optimiztion, but this project is about exploring the viability of VLMs for SLAM, not optimality (yet).
