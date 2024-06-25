from typing import Any
from AbstractNode import Node, Topics
from Buffer.RingBuffer import RingBuffer
from Device.Camera import Camera
import pickle
import time


class CameraNode(Node):
    def __init__(self, address: str, camera: Camera, ring_buffer: RingBuffer):

        super().__init__(address)
        self.camera = camera
        self.ring_buffer = ring_buffer
        self.topic = Topics['IMAGE_RGB']

    def run(self):
        try:
            while True:                
                # Binding ring buffer update function to camera new frame arrived call back
                self.camera.set_new_frame_callback(self.ring_buffer.add)
                self.camera.start_streaming()
                
                if self.ring_buffer.is_updated():
                    latest_image = self.ring_buffer.get_latest()
                    if latest_image is not None:
                        camera_info = f"Camera {self.camera.cameratype}"
                        timestamp = time.time()
                        serialized_message = self.serialize_message(latest_image, camera_info, timestamp)
                        self.publisher.publish(self.topic, serialized_message)

                        self.publisher.publish(Topics['LOG_INFO'], b"Published latest image from {camera_info} at {timestamp}")

        except Exception as e:
            self.publisher.publish(Topics['LOG_ERROR'], b"Exception occurred in CameraNode run loop")
            raise

    def serialize_message(self, image: Any, camera_info: str, timestamp: float) -> bytes:
        try:
            message = {
                'camera_info': camera_info,
                'time_stamp': timestamp,
                'image': image
            }
            return pickle.dumps(message)
        except Exception as e:
            self.publisher.publish(Topics['LOG_ERROR'], b"Exception occurred while serializing message")
            raise 


def testing_camera_node():
    # do some testing..
    pass

if __name__ == "__main__":
    testing_camera_node()
