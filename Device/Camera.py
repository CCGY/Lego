from enum import Enum
import numpy as np
import time
import threading


class CameraType(Enum):
    MONO = 0
    Color = 1
    MONO_NIR = 2
    Color_NIR = 3
    SWIR = 4
    UV = 5
    Laser3D = 6
    TOF3D = 7



class Camera:
    def __init__(self, cameratype: CameraType, resolution=(1920, 1080), framerate=30):
        """A camera object that is used to capture frame, start streaming etc..

        Args:
            cameratype (CameraType): detailed information of this camera
            resolution (tuple, optional): basic camera setting. Defaults to (1920, 1080).
            framerate (int, optional): basic camera setting. Defaults to 30.
        """
        self._resolution = resolution
        self._framerate = framerate
        self._is_opened = False
        self._streaming = False
        self._new_frame_callback = None
        self._cameratype = cameratype

    # Property for resolution
    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError("Resolution must be a tuple with width and height.")
        self._resolution = value

    # Property for framerate
    @property
    def framerate(self):
        return self._framerate

    @framerate.setter
    def framerate(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Framerate must be a positive integer.")
        self._framerate = value
    
    @property
    def cameratype(self, value):
        if not isinstance(value, CameraType):
            raise ValueError("Camera Type invalid")
        self._cameratype = value
    
    @cameratype.setter
    def cameratype(self, value):
        self._cameratype = value

    @property
    def is_opened(self):
        return self._is_opened

    # Method to start streaming
    def start_streaming(self):
        self._streaming = True
        self._is_opened = True
        print(f"Streaming started with resolution {self._resolution} at {self._framerate} FPS.")
        self._streaming_thread = threading.Thread(target=self._stream)
        self._streaming_thread.start()

    # Method to stop streaming
    def stop_streaming(self):
        self._streaming = False
        if self._streaming_thread.is_alive():
            self._streaming_thread.join()

    def is_opened(self):
        # check if camera is opened
        self.is_opened = True
        return self

    # Method to capture a new frame
    def capture_new_frame(self):
        if not self._streaming:
            print("Streaming is not started.")
            return
        # Simulate capturing a frame
        frame = np.ones(self.resolution)
        if self._new_frame_callback:
            self._new_frame_callback(frame)
        else:
            return frame

    # Internal method to simulate streaming
    def _stream(self):
        while self._streaming:
            self.capture_new_frame()
            time.sleep(1 / self._framerate)

    # Method to set a callback function for new frame arrival
    def set_new_frame_callback(self, callback):
        if not callable(callback):
            raise ValueError("Callback must be a callable function.")
        self._new_frame_callback = callback

