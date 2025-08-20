"""Pet Diet Tracker - A Raspberry Pi pet food monitoring system."""

__version__ = "0.1.0"
__author__ = "Pet Diet Tracker"
__description__ = "A system to monitor pet food bowls using camera and AI analysis"

from .pet_monitor import PetMonitor
from .bowl_analyzer import BowlAnalyzer
from .camera_capture import CameraCapture
from .notifier import Notifier
from .config import Config
from .monitor_history import MonitorHistory

__all__ = [
    "PetMonitor",
    "BowlAnalyzer", 
    "CameraCapture",
    "Notifier",
    "Config",
    "MonitorHistory",
]