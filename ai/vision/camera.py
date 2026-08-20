import cv2
import time

class CameraStream:
    """
    OpenCV Webcam Stream Wrapper with graceful camera index fallback and FPS calculation.
    """
    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None
        self.prev_time = time.time()
        self.fps = 0.0

        self._init_camera()

    def _init_camera(self):
        for index in [self.camera_index, 0, 1, 2]:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    self.cap = cap
                    self.camera_index = index
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    print(f"[CameraStream] Successfully initialized webcam at index {self.camera_index}")
                    return
                cap.release()
        raise RuntimeError("[CameraStream] Error: Unable to access any video camera device (indices 0, 1, 2 failed).")

    def read(self):
        if not self.cap or not self.cap.isOpened():
            return False, None

        ret, frame = self.cap.read()
        if not ret:
            return False, None

        # Calculate FPS
        curr_time = time.time()
        time_diff = curr_time - self.prev_time
        if time_diff > 0:
            self.fps = 0.9 * self.fps + 0.1 * (1.0 / time_diff)
        self.prev_time = curr_time

        return True, frame

    def release(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print("[CameraStream] Camera device released.")
