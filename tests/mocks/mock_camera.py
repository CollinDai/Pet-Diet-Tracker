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
