# A dummy ringbuffer, demo purpose


# Correct implementation should use shared memory based ring buffer in multiprocessing concept
# See example at: https://github.com/bslatkin/ringbuffer/blob/master/ringbuffer.py
# Quick overview: Allows multiple child Python processes started via the multiprocessing module
# to read from a shared ring buffer in the parent process. For each child, a
# pointer is maintained for the purpose of reading. One pointer is maintained by
# for the purpose of writing. 


class RingBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.counter = 0
        self.current_index = 0

    def add(self, item):
        self.counter += 1
        self.current_index = (self.counter) % self.size
        self.buffer[self.current_index] = item

    def get_by_index(self, index):
        return self.buffer[index]

    def get_latest(self):
        return self.buffer[self.current_index]
    
    def is_updated(self):
        # dummy code: check if ring buffer is updated with newest frame
        ring_buffer_updated = True
        return ring_buffer_updated

