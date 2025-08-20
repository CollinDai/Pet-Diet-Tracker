# Pet Diet Tracker
This project uses a camera to monitor a pet's food bowl and sends notifications when the bowl is emptied or refilled.

The project is designed to run on raspberry pi. It will use raspberry pi's camera module to capture picture of the bowl. Then it will use google gemini api to analyze the image to tell if it is empty or full, or partially empty.

## Setup

1. **Create Virtual Environment:**
   ```bash
   python -m venv venv --system-site-packages
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -e .
   ```

3. **Configure Environment:**
   Copy the example environment file and add your Gemini API key:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```properties
   GEMINI_API_KEY="your_api_key_here"
   ```

4. **Hardware Setup:**
   - Ensure Raspberry Pi camera module is properly connected
   - Position camera to have clear view of pet food bowl

## Running the Monitor

**Start continuous monitoring:**
```bash
pet-diet-tracker
```

**Run with custom check interval (in seconds):**
```bash
pet-diet-tracker --interval 180
```

**Run a single test check:**
```bash
pet-diet-tracker --test
```

**Alternative - run directly with Python:**
```bash
python -m pet_diet_tracker.main
```

The monitor will:
- Check bowl status every 5 minutes by default
- Send notifications when bowl status changes (EMPTY → PARTIAL → FULL)
- Display current status and timestamp for each check
