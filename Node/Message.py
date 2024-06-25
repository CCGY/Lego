# todo: All messages should be handled by a class

class ImageMessage():
    def __init__(self, msg: dict):
        self._message = msg

    @property
    def content(self):
        return self._message


class CameraMessage():
    def __init__(self, msg: dict):
        self._message = msg

    @property
    def content(self):
        return self._message


class MessageProcessingResult():
    def __init__(self, msg: dict):
        self._message = msg
        pass
    
    @property
    def content(self):
        return self._message
