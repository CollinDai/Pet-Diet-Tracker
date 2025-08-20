#!/usr/bin/env python3

from pet_monitor import PetMonitor
import argparse

def main():
    parser = argparse.ArgumentParser(description='Pet Food Bowl Monitor')
    parser.add_argument('--interval', type=int, default=300, 
                       help='Check interval in seconds (default: 300)')
    parser.add_argument('--test', action='store_true',
                       help='Run a single test check')
    
    args = parser.parse_args()
    
    monitor = PetMonitor(check_interval=args.interval)
    
    if args.test:
        print("Running test check...")
        status = monitor.check_bowl_status()
        print(f"Test result: {status}")
    else:
        monitor.start_monitoring()

if __name__ == "__main__":
    main()