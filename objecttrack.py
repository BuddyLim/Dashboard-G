class objecttrack:
    def __init__(self):
        self.counter = 0
        self.detections = []

    def register(self, detections):
        self.counter += 1
        self.detections = detections
    
    def returncounter(self):
        return self.counter