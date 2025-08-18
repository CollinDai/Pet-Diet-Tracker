import numpy as np
import cv2

class MockCamera:
    def __init__(self, frames):
        self.frames = frames
        self.frame_index = 0

    def isOpened(self):
        return True

    def read(self):
        if self.frame_index < len(self.frames):
            frame = self.frames[self.frame_index]
            self.frame_index += 1
            return True, frame
        else:
            return False, None

    def release(self):
        pass

def generate_blank_frame(width=640, height=480, color=(0, 0, 0)):
    """
    Generates a blank frame of a given color.
    """
    frame = np.zeros((height, width, 3), np.uint8)
    frame[:] = color
    return frame

def generate_frame_with_contours(num_contours, color=(24, 180, 180)):
    """
    Generates a frame with a specified number of contours.
    The default color is within the HSV range of the event detector.
    """
    frame = np.zeros((480, 640, 3), np.uint8)
    if num_contours > 0:
        # Draw contours in the ROI
        for i in range(num_contours):
            # These contours are small and spaced out to ensure they are detected as separate contours
            x = 110 + (i * 10)
            y = 110
            cv2.circle(frame, (x, y), 2, color, -1)
    return frame
