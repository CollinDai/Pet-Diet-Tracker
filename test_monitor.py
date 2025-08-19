import argparse
import os
import time
from src.services.monitoring_service import MonitoringService
from src.services.camera_service import CameraService
from src.services.notification_service import NotificationService
from src.services.event_history_service import EventHistoryService

# Try to load dotenv, but continue if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Make sure GEMINI_API_KEY is set in environment.")
    print("Install with: pip install python-dotenv")

def test_monitoring_service(num_cycles: int = 3, debounce_time: float = 10):
    """
    Tests the MonitoringService with real camera input.
    
    Args:
        num_cycles: Number of monitoring cycles to run
        debounce_time: Debounce time in seconds (default 10 for testing)
    """
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.")
        return

    print("Initializing Pet Food Monitoring Service...")
    
    try:
        # Initialize services
        notification_service = NotificationService()
        event_history_service = EventHistoryService()
        monitoring_service = MonitoringService(
            notification_service, 
            event_history_service, 
            debounce_time=debounce_time
        )
        
        print("Initializing camera...")
        camera = CameraService()
        
        if not camera.isOpened():
            print("Error: Camera failed to initialize.")
            print("Make sure you're running on a system with a camera available.")
            return
            
        print(f"Camera initialized successfully!")
        print(f"Running {num_cycles} monitoring cycles with {debounce_time}s debounce time...")
        print("=" * 60)
        
        results = []
        for i in range(num_cycles):
            print(f"\n--- Monitoring Cycle {i+1}/{num_cycles} ---")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Run a monitoring cycle
            result = monitoring_service.run_monitoring_cycle(camera)
            results.append(result)
            
            # Display results
            print(f"Frame captured: {'✓' if result.frame_captured else '✗'}")
            
            if result.error:
                print(f"❌ Error: {result.error}")
            elif result.event_detected:
                print(f"🎯 Event detected: {result.event_detected}")
                if monitoring_service.last_event == result.event_detected:
                    print(f"📝 Event logged and notification sent")
                else:
                    print(f"⏰ Event debounced (too recent)")
            else:
                print("😴 No event detected")
            
            # Wait between cycles for demo purposes
            if i < num_cycles - 1:
                print("Waiting 2 seconds before next cycle...")
                time.sleep(2)
        
        # Display summary
        print("\n" + "=" * 60)
        print("📊 MONITORING SESSION SUMMARY")
        print("=" * 60)
        
        successful_cycles = sum(1 for r in results if r.frame_captured and not r.error)
        events_detected = [r.event_detected for r in results if r.event_detected]
        errors = [r.error for r in results if r.error]
        
        print(f"Total cycles run: {len(results)}")
        print(f"Successful cycles: {successful_cycles}")
        print(f"Failed cycles: {len(results) - successful_cycles}")
        
        if events_detected:
            print(f"Events detected: {len(events_detected)}")
            for i, event in enumerate(events_detected, 1):
                print(f"  {i}. {event}")
        else:
            print("No events detected")
            
        if errors:
            print(f"Errors encountered: {len(errors)}")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
        
        # Show service state
        print(f"\nMonitoring Service State:")
        print(f"  Last event: {monitoring_service.last_event}")
        print(f"  Last event time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(monitoring_service.last_event_time)) if monitoring_service.last_event_time else 'Never'}")
        print(f"  Debounce time: {monitoring_service.debounce_time}s")
        
    except RuntimeError as e:
        print(f"❌ Camera initialization failed: {e}")
        print("Make sure you're running on a Raspberry Pi with camera module enabled")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        try:
            camera.release()
            print("\n✓ Camera released successfully")
        except:
            pass

def test_single_cycle():
    """
    Tests a single monitoring cycle for quick validation.
    """
    print("Running single monitoring cycle test...")
    test_monitoring_service(num_cycles=1, debounce_time=1)

def test_debouncing():
    """
    Tests event debouncing by running multiple rapid cycles.
    """
    print("Testing event debouncing with rapid cycles...")
    test_monitoring_service(num_cycles=5, debounce_time=30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Pet Food Monitoring Service.")
    parser.add_argument("--cycles", type=int, default=3, help="Number of monitoring cycles to run (default: 3)")
    parser.add_argument("--debounce", type=float, default=10, help="Debounce time in seconds (default: 10)")
    parser.add_argument("--mode", choices=["normal", "single", "debounce"], default="normal", 
                       help="Test mode: normal (default), single cycle, or debounce test")
    
    args = parser.parse_args()
    
    if args.mode == "single":
        test_single_cycle()
    elif args.mode == "debounce":
        test_debouncing()
    else:
        test_monitoring_service(args.cycles, args.debounce)