#!/usr/bin/env python3
"""
Camera diagnostic script for Raspberry Pi
"""

import sys
import os

def check_raspberry_pi():
    """Check if we're running on a Raspberry Pi."""
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip('\x00')
            print(f"✅ Device model: {model}")
            return 'Raspberry Pi' in model
    except FileNotFoundError:
        print("❌ Not running on Raspberry Pi (no device tree)")
        return False

def check_camera_hardware():
    """Check camera hardware detection."""
    print("\n--- Camera Hardware Check ---")
    
    # Check if camera is detected
    try:
        result = os.popen('libcamera-hello --list-cameras').read()
        print("Camera detection output:")
        print(result)
        return 'Available cameras' in result
    except Exception as e:
        print(f"❌ Camera detection failed: {e}")
        return False

def check_picamera2_import():
    """Test picamera2 import."""
    print("\n--- Picamera2 Import Test ---")
    
    try:
        import picamera2
        print(f"✅ picamera2 imported successfully")
        print(f"   Version: {getattr(picamera2, '__version__', 'unknown')}")
        
        # Try to create Picamera2 instance
        try:
            from picamera2 import Picamera2
            cam = Picamera2()
            print("✅ Picamera2 instance created successfully")
            cam.close()
            return True
        except Exception as e:
            print(f"❌ Failed to create Picamera2 instance: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import picamera2: {e}")
        print("Try installing: sudo apt install python3-picamera2")
        return False

def check_permissions():
    """Check camera permissions."""
    print("\n--- Permission Check ---")
    
    # Check if user is in video group
    groups = os.popen('groups').read().strip()
    print(f"User groups: {groups}")
    
    if 'video' in groups:
        print("✅ User is in video group")
    else:
        print("⚠️  User not in video group. Try: sudo usermod -a -G video $USER")
    
    # Check camera device files
    camera_devices = ['/dev/video0', '/dev/video1']
    for device in camera_devices:
        if os.path.exists(device):
            print(f"✅ Camera device found: {device}")
        else:
            print(f"❌ Camera device not found: {device}")

def main():
    print("Raspberry Pi Camera Diagnostic")
    print("=" * 40)
    
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if on Raspberry Pi
    if check_raspberry_pi():
        print("✅ Running on Raspberry Pi")
    else:
        print("❌ Not running on Raspberry Pi")
        return
    
    # Check camera hardware
    camera_detected = check_camera_hardware()
    
    # Check permissions
    check_permissions()
    
    # Check picamera2 import
    picamera2_works = check_picamera2_import()
    
    print("\n" + "=" * 40)
    print("SUMMARY:")
    print(f"Camera hardware detected: {'✅' if camera_detected else '❌'}")
    print(f"Picamera2 working: {'✅' if picamera2_works else '❌'}")
    
    if not camera_detected:
        print("\n📋 Camera hardware troubleshooting:")
        print("1. Check camera cable connection")
        print("2. Enable camera: sudo raspi-config -> Interface Options -> Camera")
        print("3. Reboot after enabling camera")
    
    if not picamera2_works:
        print("\n📋 Picamera2 troubleshooting:")
        print("1. Install: sudo apt install python3-picamera2")
        print("2. Update system: sudo apt update && sudo apt upgrade")
        print("3. Add user to video group: sudo usermod -a -G video $USER")
        print("4. Log out and log back in")

if __name__ == "__main__":
    main()