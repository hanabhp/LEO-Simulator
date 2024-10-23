class Packet:
    def __init__(self, size, creation_time):
        self.size = size
        self.creation_time = creation_time
        self.queue_entry_time = None
        self.processing_start_time = None
        self.completion_time = None
        
    @property
    def total_latency(self):
        if self.completion_time and self.creation_time:
            return self.completion_time - self.creation_time
        return None