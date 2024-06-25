from AbstractNode import ZeroMQSubscriber
from Logger.Logger import logger

class LoggingNode(ZeroMQSubscriber):
    def __init__(self, address: str):
        super().__init__(address)

        self.topic = b'log' # subscribe to all topics start with 'log'    
    
    def run(self):
        try:
            # Only subscribe to logging message by Topic filtering
            self.subscriber.subscribe(self.callback, topic = b'log')
        except Exception as e:
            logger.exception(f"Exception occurred in LoggingNode run loop")
    
    def callback(self, topic :bytes, serialized_message: bytes):
        self._write_to_log(topic, serialized_message)
        

    def _write_to_log(topic, msg):
        # dummy code, replace it a function extracting log type from the topics
        log_message_type = "INFO"
        match log_message_type:
            case 'INFO': 
                logger.info(msg)
            case 'EXCEPTION':
                logger.exception(msg)
