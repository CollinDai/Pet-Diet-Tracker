# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Pet Food Consumption Monitor designed to run on Raspberry Pi. The system uses a camera module to capture images of a pet's food bowl and leverages Google Gemini API to analyze whether the bowl is empty, full, or partially empty, sending notifications accordingly.

## Environment Setup

The project requires a `.env` file with the following configuration:
```
GEMINI_API_KEY="your_api_key"
```

## Project Status

The project is now implemented with the following Python modules:
- `main.py` - Entry point with CLI interface
- `pet_monitor.py` - Core monitoring logic
- `camera_capture.py` - Raspberry Pi camera integration
- `bowl_analyzer.py` - Google Gemini API integration for image analysis
- `notifier.py` - Notification system
- `config.py` - Environment configuration management

## Development Notes

- Target platform: Raspberry Pi with camera module
- Image analysis: Google Gemini API integration
- Environment management: python-dotenv for configuration
- Hardware dependency: Raspberry Pi camera module for bowl monitoring

## Coding Notes

- Keep the class and function small. Should follow Single Responsibility Principle. A function should do just one thing. And a class also should just do one thing.
- Starting with the Gemini 2.0 release in late 2024, Google introduced a new set of libraries called the Google GenAI SDK. 
   - google-generativeai -> google-genai
- When passing images to Google GenAI API, use `genai.types.Part.from_bytes()` with raw image bytes and proper mime_type