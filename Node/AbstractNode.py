"""
Abstract classes that support "publisher-subscriber" communication pattern ZeroMQ

More details can be found on https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pubsub.html

"""

from abc import ABC, abstractmethod
import zmq


# list of byte strings for sending over network
Topics = {
    'IMAGE_RGB': b'sensor_data.image_rgb',
    'IMAGE_RAW': b'sensor_data.image_raw',
    'IMAGE_RECONGNITION_RESULT': b'image_recongition_result',
    'IMAGE_DETECTION': b'image_process_detection_result',
    'IMAGE_SEGEMENTATION': b'image_process_detection_result',
    'LOG_DEBUG': b'log.debug',
    'LOG_INFO': b'log_info',
    'LOG_WARN': b'log.warn',
    'LOG_ERROR': b'log.error',
    'LOG_CRITICAL': b'log_critical'
}

class Publisher(ABC):
    @abstractmethod
    def publish(self, topic: bytes, message: bytes) -> None:
        pass

class Subscriber(ABC):
    @abstractmethod
    def subscribe(self, callback: callable) -> None:
        pass

class ZeroMQPublisher(Publisher):
    def __init__(self, address: str):
        # 
        self._address = address
        # required to initialize zmq 
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.bind(self._address)

    def publish(self, topic: bytes, message: bytes) -> None:
        self._socket.send_multipart([topic, message])

class ZeroMQSubscriber(Subscriber):
    def __init__(self, address: str):
        self._address = address
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.SUB)
        self._socket.connect(self._address)
        

    def subscribe(self, callback: callable, topic: bytes) -> None:
        self._socket.setsockopt(zmq.SUBSCRIBE, topic)
        while True:
            topic, message = self._socket.recv_multipart()
            callback(topic, message)


class Node(ABC):
    def __init__(self, address: str):
        self.publisher = Publisher(address)
        self.subscriber = Subscriber(address)
    
    @abstractmethod
    def run(self):
        pass

