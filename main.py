from Device.Camera import Camera
from Buffer.RingBuffer import RingBuffer
from ImageProcessing.LegoRecognition import LegoBrickRecognition
from ImageProcessing.LegoSorting import LegoBrickSorting
from Node.ImageProcessingNode import ImageProcessingNode
from Node.CameraNode import CameraNode
from Node.SystemLogingNode import LoggingNode

import threading


def main():
    # Define address
    url = "tcp://127.0.0.1:5555"

    # Create a camera node
    camera = Camera()
    buffer = RingBuffer()
    camera_node = CameraNode(address=url, camera=camera, ring_buffer=buffer)

    # Start the camera node in a separate thread to simulate continuous operation
    camera_thread = threading.Thread(target=camera_node.run)
    camera_thread.start()

    # Create a image processing node with specified method and subscribe to a url where the image data is posted
    brick_recognition_method = LegoBrickRecognition()
    brick_recognition_node = ImageProcessingNode(url, brick_recognition_method)    

    # Start recognition node in a separate thread
    processing_thread = threading.Thread(target=brick_recognition_node.run)
    processing_thread.start()

    # Easy to switch to another method for different vision inspection task such as sorting
    brick_sorting_method = LegoBrickSorting()
    brick_sorting_node = ImageProcessingNode(url, brick_sorting_method)    

    # Start sorting node in a separate thread
    processing_thread = threading.Thread(target=brick_sorting_node.run)
    processing_thread.start()

    # Start logging node in a separate thread
    logging_node = LoggingNode(url)
    logging_thread = threading.Thread(target=logging_node.run)
    logging_thread.start()



if __name__ == "__main__":
    main()
