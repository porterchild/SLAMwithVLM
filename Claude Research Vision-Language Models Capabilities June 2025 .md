# Latest Vision-Language Models: Image Context Capabilities (2025)

**Claude 4 leads with 100 images per request, while new unified models like Phi-4 Multimodal process speech, vision, and text simultaneously.**

## Top Models & Image Limits

### Anthropic Claude 4 (May 2025)
- **100 images per API request** (20 via web interface)
- Max: 8,000 x 8,000 pixels, 5MB per image
- 200K token context

### OpenAI GPT-4o/4.1 Series (Jan 2025)
- **10-20 images per request** (Azure supports 20, docs say 10)
- 20MB file size limit, 1M token context
- GPT-4o includes integrated image generation

### Google Gemini 2.5 Pro/Flash (June 2025)
- **~3,000 images estimated** (unconfirmed)
- 1-2M token context, 3,072 x 3,072 pixel limit
- Built-in reasoning with 32K thinking budget

### Meta Llama 4 Scout/Maverick (April 2025)
- **5-8 images** (tested up to 48 in training)
- 10M token context (Scout), 1M (Maverick)
- Requires ~54.5GB VRAM

## Breakthrough Unified Models

### Microsoft Phi-4 Multimodal (Feb 2025)
- **5.6B parameters** processing speech, vision, text simultaneously
- 128K token context, mixture-of-LoRAs architecture
- #1 on HuggingFace OpenASR leaderboard (6.14% word error rate)
- Edge-optimized for on-device deployment

### Qwen2.5-VL (Jan 2025)
- **3B/7B/72B variants**, unlimited images for 1+ hour videos
- Agentic computer/mobile interaction capabilities
- 96.4 DocVQA, 70.2 MMMU scores
- Omnidocument parsing (handwriting, charts, formulas)

## Open-Source Leaders

### Mistral Pixtral Large (Dec 2024)
- **8 images max**, 124B parameters
- 69.4% MathVista (best performance)
- 10MB file size limit

### xAI Grok 3 (Feb 2025)
- **Variable image support**, 131K context
- Spatial reasoning expertise
- "Thinking mode" reveals reasoning steps

### DeepSeek-VL2 & Janus-Pro-7B (Jan 2025)
- **834 OCRBench score** (beats GPT-4o's 736)
- Mixture-of-Experts architecture
- Strong text-to-image generation

## Quick Comparison

| **Model** | **Max Images** | **Context** | **Key Strength** |
|-----------|----------------|-------------|------------------|
| **Claude 4** | 100 | 200K | Highest image count |
| **GPT-4o/4.1** | 10-20 | 1M | Integrated generation |
| **Gemini 2.5** | ~3,000 | 1-2M | Massive context |
| **Llama 4** | 5-8 | 10M | Largest context window |
| **Phi-4 Multimodal** | Multi-frame | 128K | Unified speech/vision/text |
| **Qwen2.5-VL** | Video 1h+ | Dynamic | Agentic capabilities |
| **Pixtral Large** | 8 | 128K | Best open-source |

## Key Takeaways

**Image Capacity Leaders:** Claude 4 (100), Gemini 2.5 (~3,000), GPT-4o (10-20)

**Technical Breakthroughs:** Unified multimodal processing (Phi-4), agentic capabilities (Qwen2.5-VL), massive contexts (Llama 4's 10M tokens)

**Open-Source Excellence:** Qwen2.5-VL matches proprietary performance, Pixtral Large leads frontier benchmarks

**2025 Trend:** Shift from separate vision/text pipelines to unified architectures processing all modalities simultaneously