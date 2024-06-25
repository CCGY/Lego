import pickle
from AbstractNode import Node, Topics
from ImageProcessing.AbstractImageProcessing import ImageProcessing
from typing import Any
import numpy as np



class ImageProcessingNode(Node):
    def __init__(self, address: str, processing_algorithm: ImageProcessing):
        """_summary_

        Args:
            address (str): Image process node will subscribe to this url and cache the image
            processing_algorithm (ImageProcessing): The method to handle image processing task
        """

        super().__init__(address)
        self.processing_algorithm = processing_algorithm

    def run(self):
        try:
            # Only subscribe to image data by topic filtering
            self.subscriber.subscribe(self.callback, topic = b'sensor_data.image_rgb')
        except Exception as e:
            self.publisher.publish(Topics['LOG_ERROR'], b"Exception occurred in ImageProcessingNode run loop")

    def callback(self, serialized_message: bytes):
        try:
            message = pickle.loads(serialized_message)
            image = message['image']
            timestamp = message['time_stamp']

            # Process the image
            result = self._process_image(image)
            serialized_processed_message = self._serialize_message(image, result, timestamp)
            
            # Publish the Processing result, eg, can be used by a physical actuator
            self.publisher.publish(Topics['IMAGE_RECONGNITION_RESULT'], serialized_processed_message)

            # Publish information for logging
            self.publisher.publish(Topics['LOG_INFO'], b"Published processed image at {timestamp}")

        except Exception as e:
            self.publisher.publish(Topics['LOG_ERROR'], b"Exception occurred in ImageProcessingNode callback")

    def _process_image(self, image: np.ndarray) -> Any:
        try:
            # Convert image to grayscale as a basic processing step
            return self.processing_algorithm.run(image)
        except Exception as e:
            self.publisher.publish(Topics['LOG_ERROR'], b"Exception occurred while processing image")
            raise

    def _serialize_message(self, image: Any, result: Any, timestamp: float) -> bytes:
        try:
            message = {
                'timestamp': timestamp,
                'image': image,
                'result': result
            }
            return pickle.dumps(message)
        except Exception as e:
            self.publisher.publish(Topics['LOG_ERROR'], b"Exception occurred while serializing processed message")
            raise
