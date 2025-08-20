#!/usr/bin/env python3

from pet_monitor import PetMonitor
import argparse
from logger_config import get_logger

def main():
    logger = get_logger(__name__)
    logger.info("Pet Food Bowl Monitor starting up")
    
    parser = argparse.ArgumentParser(description='Pet Food Bowl Monitor')
    parser.add_argument('--interval', type=int, default=300, 
                       help='Check interval in seconds (default: 300)')
    parser.add_argument('--test', action='store_true',
                       help='Run a single test check')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Debug logging enabled")
    
    logger.info(f"Parsed arguments: interval={args.interval}, test={args.test}, debug={args.debug}")
    
    try:
        monitor = PetMonitor(check_interval=args.interval)
        
        if args.test:
            logger.info("Running single test check")
            status = monitor.check_bowl_status()
            logger.info(f"Test completed with result: {status}")
        else:
            monitor.start_monitoring()
            
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()