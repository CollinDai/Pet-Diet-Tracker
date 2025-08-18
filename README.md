# Pet Food Consumption Monitor

This project uses a camera to monitor a pet's food bowl and sends notifications when the bowl is empty or refilled.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd pet-food-consumption-monitor
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
    **Note for Raspberry Pi users:**
    The `picamera2` library relies on the `libcamera` system library, which cannot be installed via pip. You must install it using your system's package manager. On a Raspberry Pi, you can do this with:
    ```bash
    sudo apt-get update
    sudo apt-get install -y python3-libcamera
    ```

4.  **Set the Gemini API Key:**
    You need to set the `GEMINI_API_KEY` environment variable to use the image analysis service.
    ```bash
    export GEMINI_API_KEY="your_gemini_api_key_here"
    ```

## Running the application

```bash
python3 src/main.py
```

## Running tests

To test the image analysis service with a specific image:
```bash
python3 test_gemini.py /path/to/your/image.jpg
```