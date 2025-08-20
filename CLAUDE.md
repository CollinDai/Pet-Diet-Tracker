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

This appears to be a new/empty project with only a README.md file currently present. The codebase will likely be developed in Python given the project description mentions python-dotenv library and Raspberry Pi compatibility.

## Development Notes

- Target platform: Raspberry Pi with camera module
- Image analysis: Google Gemini API integration
- Environment management: python-dotenv for configuration
- Hardware dependency: Raspberry Pi camera module for bowl monitoring

## Coding Notes

- Keep the class and function small. Should follow Single Responsibility Principle. A function should do just one thing.
- Starting with the Gemini 2.0 release in late 2024, Google introduced a new set of libraries called the Google GenAI SDK. 
   - google-generativeai -> google-genai